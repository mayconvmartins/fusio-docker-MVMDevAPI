#!/usr/bin/env python
"""
corrige.py – Script avançado para corrigir arquivos CSV problemáticos com IA e processamento paralelo

Este script processa arquivos CSV grandes que possuem problemas comuns como:
 - Número incorreto de colunas
 - Caracteres inválidos
 - Quebras de linha dentro de campos
 
Funcionalidades:
 - Usa inteligência para corrigir linhas com número errado de colunas
 - Processamento paralelo usando multiprocessing (otimizado para 20 núcleos)
 - Otimizado para máquinas com muita RAM (128GB)
 - Gravação incremental dos resultados
 - Barra de progresso em tempo real
 - Log detalhado de operações
"""

import argparse
import concurrent.futures
import csv
import gc
import json
import logging
import multiprocessing
import os
import re
import sys
import time
from collections import defaultdict
from functools import partial
from tqdm import tqdm
import numpy as np
import pandas as pd

# Aumenta o limite máximo de campo para campos muito grandes
csv.field_size_limit(sys.maxsize)

# Configurações para máquinas de alto desempenho
NUM_WORKERS = min(20, multiprocessing.cpu_count())  # Usa até 20 núcleos
CHUNK_SIZE = 1000000  # 1 milhão de linhas por chunk (ajustado para 128GB de RAM)
MAX_MEMORY_PERCENT = 70  # Usa até 70% da RAM disponível

def limpar_valor(valor):
    """Limpa um valor, removendo caracteres problemáticos."""
    if valor is None:
        return ""
    
    valor = str(valor)
    valor = re.sub(r'[\r\n]+', ' ', valor)  # remove quebras de linha
    valor = re.sub(r'\s+', ' ', valor).strip()  # normaliza espaços
    valor = re.sub(r'[^\x20-\x7E]', '', valor)  # remove caracteres não-imprimíveis
    
    # Se contém vírgula e não está entre aspas, adiciona aspas
    if "," in valor and not (valor.startswith('"') and valor.endswith('"')):
        valor = f'"{valor}"'
    
    return valor

def inferir_estrutura(file_path, sample_size=50000):
    """
    Infere a estrutura do CSV lendo uma amostra do arquivo.
    Retorna o cabeçalho, a lista de índices de colunas que parecem ser texto,
    padrões de campo para cada coluna, e o delimitador.
    """
    logging.info(f"Inferindo estrutura do arquivo {file_path} com amostra de {sample_size} linhas...")
    
    # Detecta o delimitador
    delimiters = [',', ';', '\t', '|']
    delimiter = ','
    with open(file_path, 'r', encoding='latin1', errors='replace') as f:
        header_line = f.readline().strip()
        for delim in delimiters:
            if header_line.count(delim) > header_line.count(delimiter):
                delimiter = delim
    
    header = None
    text_indices = []
    expected_columns = 0
    all_rows = []
    column_patterns = defaultdict(list)
    
    with open(file_path, 'r', encoding='latin1', errors='replace') as f:
        try:
            # Processa a primeira linha como cabeçalho
            header_line = f.readline().strip()
            header = header_line.split(delimiter)
            expected_columns = len(header)
            numeric_flags = [True] * expected_columns
            
            # Analisa as próximas linhas para identificar tipos de coluna
            count = 0
            for line in f:
                if count >= sample_size:
                    break
                
                try:
                    fields = line.strip().split(delimiter)
                    all_rows.append(fields)
                    
                    # Só considera linhas com o número correto de colunas para inferência
                    if len(fields) == expected_columns:
                        for i, field in enumerate(fields):
                            if i < expected_columns:
                                # Armazena exemplos para aprender padrões
                                column_patterns[i].append(field)
                                
                                # Se contém letra ou espaço, não é numérico
                                if re.search(r'[A-Za-z]', field) or ' ' in field:
                                    numeric_flags[i] = False
                    
                    count += 1
                except Exception as e:
                    continue
        except Exception as e:
            logging.error(f"Erro ao inferir estrutura: {str(e)}")
    
    # Colunas que não são numéricas são consideradas texto
    text_indices = [i for i, flag in enumerate(numeric_flags) if not flag]
    
    # Cria padrões de expressão regular para cada coluna baseado nos exemplos
    pattern_dict = {}
    for col_idx, examples in column_patterns.items():
        # Limita a 100 exemplos para não sobrecarregar
        samples = examples[:100]
        if col_idx in text_indices:
            # Para colunas de texto, criamos um padrão mais flexível
            pattern_dict[col_idx] = r'.*'
        else:
            # Para colunas numéricas, verificamos o formato
            has_decimal = any('.' in sample for sample in samples)
            has_negative = any(sample.startswith('-') for sample in samples)
            if has_decimal:
                if has_negative:
                    pattern_dict[col_idx] = r'-?\d+\.\d+'
                else:
                    pattern_dict[col_idx] = r'\d+\.\d+'
            else:
                if has_negative:
                    pattern_dict[col_idx] = r'-?\d+'
                else:
                    pattern_dict[col_idx] = r'\d+'
    
    logging.info(f"Estrutura inferida: {expected_columns} colunas, {len(text_indices)} colunas de texto")
    logging.info(f"Colunas de texto: {text_indices}")
    
    return header, expected_columns, text_indices, pattern_dict, delimiter

def corrigir_linha_com_ia(line, expected_columns, text_indices, pattern_dict, delimiter):
    """
    Função "IA" avançada para corrigir linhas com base nos padrões aprendidos.
    """
    # Divide a linha usando o delimitador
    fields = line.strip().split(delimiter)
    
    # Se já tem o número correto, apenas limpa
    if len(fields) == expected_columns:
        return [limpar_valor(field) for field in fields]
    
    # Se tem mais campos que o esperado, tenta corrigir
    if len(fields) > expected_columns:
        # Estratégia 1: Procura por campos de texto onde podemos mesclar
        for idx in sorted(text_indices, reverse=True):
            if idx >= len(fields) - 1:
                continue
                
            # Calcula quantos campos precisam ser mesclados
            extra_fields = len(fields) - expected_columns
            fields_to_check = min(extra_fields + 1, len(fields) - idx)
            
            # Tenta mesclar campos consecutivos
            for join_count in range(1, fields_to_check + 1):
                merged_field = delimiter.join(fields[idx:idx+join_count])
                new_fields = fields[:idx] + [merged_field] + fields[idx+join_count:]
                
                # Se agora temos o número correto, retorna
                if len(new_fields) == expected_columns:
                    return [limpar_valor(field) for field in new_fields]
        
        # Estratégia 2: Baseada nos padrões, identifica campos que parecem ter sido divididos incorretamente
        candidate_merges = []
        
        # Procura por campos adjacentes que, quando mesclados, correspondem ao padrão esperado
        for i in range(len(fields) - 1):
            if i < expected_columns:
                expected_pattern = pattern_dict.get(i, r'.*')
                merged = delimiter.join([fields[i], fields[i+1]])
                
                # Se o campo mesclado corresponde ao padrão da coluna, é um candidato para mesclagem
                if re.match(expected_pattern, merged):
                    candidate_merges.append(i)
        
        # Tenta aplicar as mesclagens candidatas na ordem
        if candidate_merges:
            working_fields = fields.copy()
            merged_count = 0
            
            for idx in candidate_merges:
                adj_idx = idx - merged_count  # Ajusta pelo número de mesclagens já feitas
                
                # Verifica se ainda podemos mesclar
                if adj_idx < len(working_fields) - 1:
                    merged_field = delimiter.join([working_fields[adj_idx], working_fields[adj_idx+1]])
                    working_fields = working_fields[:adj_idx] + [merged_field] + working_fields[adj_idx+2:]
                    merged_count += 1
                    
                    # Se chegamos ao número correto de campos, retornamos
                    if len(working_fields) == expected_columns:
                        return [limpar_valor(field) for field in working_fields]
    
    # Se tem menos campos que o esperado, tenta adicionar campos vazios no final
    elif len(fields) < expected_columns:
        fields.extend([''] * (expected_columns - len(fields)))
        return [limpar_valor(field) for field in fields]
    
    # Se não conseguimos corrigir, retorna None
    return None

def processar_chunk(chunk_lines, expected_columns, text_indices, pattern_dict, delimiter):
    """
    Processa um chunk de linhas e retorna as linhas corrigidas e as linhas com erro.
    Esta função é otimizada para processamento paralelo.
    """
    corrected_lines = []
    error_lines = []
    
    for line in chunk_lines:
        try:
            fields = corrigir_linha_com_ia(line, expected_columns, text_indices, pattern_dict, delimiter)
            
            if fields:
                corrected_lines.append(delimiter.join(fields))
            else:
                error_lines.append(line)
        except Exception as e:
            error_lines.append(line)
    
    return corrected_lines, error_lines

def ler_chunks(file_path, start_position=0, chunk_size=CHUNK_SIZE):
    """
    Gerador que lê chunks de linhas do arquivo.
    Retorna o chunk de linhas e a posição atual no arquivo.
    """
    with open(file_path, 'r', encoding='latin1', errors='replace') as f:
        # Posiciona no início correto
        if start_position > 0:
            f.seek(start_position)
        else:
            # Pula a linha de cabeçalho se estiver no início
            f.readline()
        
        while True:
            chunk = []
            chunk_start_position = f.tell()
            
            # Lê um chunk de linhas
            for _ in range(chunk_size):
                line = f.readline()
                if not line:
                    break
                chunk.append(line)
            
            if not chunk:
                break
                
            yield chunk, chunk_start_position, f.tell()

def salvar_progresso(progress_path, position, processed_lines, corrected_lines, error_lines):
    """Salva o progresso atual no arquivo de progresso."""
    with open(progress_path, 'w') as p_file:
        json.dump({
            'position': position,
            'processed_lines': processed_lines,
            'corrected_lines': corrected_lines,
            'error_lines': error_lines,
            'last_update': time.time()
        }, p_file)

def processar_arquivo(input_path, output_dir, config_dir):
    """
    Processa o arquivo CSV em chunks paralelizados.
    """
    file_basename = os.path.splitext(os.path.basename(input_path))[0]
    output_path = os.path.join(output_dir, f"{file_basename}.csv")
    error_path = os.path.join(config_dir, f"{file_basename}_linhascomerro.csv")
    progress_path = os.path.join(config_dir, f"{file_basename}.progress.json")
    
    # Infere a estrutura do arquivo
    header, expected_columns, text_indices, pattern_dict, delimiter = inferir_estrutura(input_path)
    
    # Determina o tamanho total do arquivo para a barra de progresso
    file_size = os.path.getsize(input_path)
    
    # Verifica se há progresso anterior
    start_position = 0
    processed_lines_count = 0
    corrected_lines_count = 0
    error_lines_count = 0
    
    if os.path.exists(progress_path):
        with open(progress_path, 'r') as f:
            progress_data = json.load(f)
            start_position = progress_data.get('position', 0)
            processed_lines_count = progress_data.get('processed_lines', 0)
            corrected_lines_count = progress_data.get('corrected_lines', 0)
            error_lines_count = progress_data.get('error_lines', 0)
            logging.info(f"Retomando a partir da posição {start_position} ({processed_lines_count} linhas processadas)")
    
    # Prepara arquivos de saída
    mode = 'a' if start_position > 0 else 'w'
    with open(output_path, mode, encoding='utf-8', errors='replace') as out_file, \
         open(error_path, mode, encoding='utf-8', errors='replace') as error_file:
        
        # Escreve o cabeçalho se estamos começando do início
        if start_position == 0:
            out_file.write(delimiter.join(header) + '\n')
        
        # Define a função de processamento parcial com os parâmetros fixos
        process_func = partial(
            processar_chunk,
            expected_columns=expected_columns,
            text_indices=text_indices,
            pattern_dict=pattern_dict,
            delimiter=delimiter
        )
        
        # Inicializa a barra de progresso
        with tqdm(total=file_size, initial=start_position, unit='B', unit_scale=True, desc="Processando") as pbar:
            
            # Cria um executor de process pool para processamento paralelo
            with concurrent.futures.ProcessPoolExecutor(max_workers=NUM_WORKERS) as executor:
                
                # Lista para armazenar os futures em andamento
                futures = []
                
                # Processa os chunks em paralelo
                for chunk, chunk_start, chunk_end in ler_chunks(input_path, start_position, CHUNK_SIZE):
                    # Envia o chunk para processamento
                    future = executor.submit(process_func, chunk)
                    futures.append((future, chunk_start, chunk_end, len(chunk)))
                    
                    # Verifica os chunks concluídos e escreve os resultados
                    # Só mantém até NUM_WORKERS*2 futures ativos para controlar uso de memória
                    while len(futures) >= NUM_WORKERS * 2:
                        # Procura por futures completos
                        completed = []
                        for i, (future, c_
