# MVMDEV API Platform

## Visão Geral

Este projeto utiliza Docker para configurar e gerenciar o ambiente de desenvolvimento e produção do Fusio. O Fusio é uma plataforma de gerenciamento de APIs que permite criar, gerenciar e monitorar APIs de forma eficiente.

## Estrutura do Projeto

- **Dockerfile**: Define a imagem Docker personalizada para o Fusio.
- **docker-compose.yml**: Define e gerencia os serviços Docker, incluindo o Fusio, banco de dados MySQL e workers.
- **.env**: Arquivo de variáveis de ambiente para configurar o Fusio e outros serviços.
- **apache/fusio.conf**: Configuração do Apache para o Fusio.
- **supervisor/fusio.conf**: Configuração do Supervisor para gerenciar processos do Fusio.
- **php/fusio.ini**: Configuração do PHP para o Fusio.
- **oracle/Dockerfile**: Dockerfile para configurar o cliente Oracle.
- **LICENSE**: Licença Apache 2.0 para o projeto.

## Pré-requisitos

- Docker
- Docker Compose

## Instalação

1. Clone o repositório:

   ```bash
   git clone https://github.com/seu-usuario/fusio-docker-MVMDevAPI.git
   cd fusio-docker-MVMDevAPI
   ```

2. Crie e configure o arquivo `.env` com as variáveis de ambiente necessárias:

   ```plaintext
   FUSIO_PROJECT_KEY="42eec18ffdbffc9fda6110dcc705d6ce"
   FUSIO_URL="http://api.mvmdev.com"
   FUSIO_APPS_URL="http://app.mvmdev.com"
   FUSIO_ENV="prod"
   FUSIO_DEBUG="false"
   FUSIO_CONNECTION="pdo-mysql://fusio:61ad6c6A5999@mysql-fusio/fusio"
   FUSIO_BACKEND_USER="test"
   FUSIO_BACKEND_EMAIL="demo@fusio-project.org"
   FUSIO_BACKEND_PW="test1234"
   FUSIO_MAILER="native://default"
   FUSIO_MESSENGER="doctrine://default"
   FUSIO_MAIL_SENDER="info@api.fusio.cloud"
   FUSIO_MARKETPLACE="off"
   FUSIO_WORKER_JAVA=""
   FUSIO_WORKER_JAVASCRIPT=""
   FUSIO_WORKER_PHP=""
   FUSIO_WORKER_PYTHON=""
   ```

## Inicialização

Para iniciar os serviços, execute o comando:

```bash
docker-compose up -d
```

Isso irá construir as imagens Docker e iniciar os contêineres definidos no `docker-compose.yml`.

## Parada

Para parar os serviços, execute o comando:

```bash
docker-compose down
```

Isso irá parar e remover os contêineres, redes e volumes definidos no `docker-compose.yml`.

## Reinicialização

Para reiniciar os serviços, execute o comando:

```bash
docker-compose restart
```

## Ver Logs

Para ver os logs dos contêineres, execute o comando:

```bash
docker-compose logs -f
```

## Acesso

- API: [http://api.mvmdev.com](http://api.mvmdev.com)
- Apps: [http://app.mvmdev.com](http://app.mvmdev.com)

## Estrutura de Diretórios

- **fusio**: Diretório principal do Fusio.
- **logs**: Diretório para logs.
- **cache**: Diretório para cache.
- **db**: Diretório para o banco de dados.
- **worker/java**: Diretório para ações do worker Java.
- **worker/javascript**: Diretório para ações do worker JavaScript.
- **worker/php**: Diretório para ações do worker PHP.
- **worker/python**: Diretório para ações do worker Python.
- **/mvm/Bancos_de_Dados**: Diretório para bancos de dados.

## Licença

Este projeto está licenciado sob a Licença Apache 2.0. Veja o arquivo [LICENSE](./LICENSE) para mais detalhes.
