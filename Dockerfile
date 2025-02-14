FROM php:8.3-apache
MAINTAINER Christoph Kappestein <christoph.kappestein@apioo.de>
LABEL version="5.1.6"
LABEL description="MVMDEV API Platform"

ARG FUSIO_VERSION="5.1.6"
ARG FUSIO_APP_BACKEND="5.1.4"
ARG FUSIO_APP_DEVELOPER="5.1.0"
ARG FUSIO_APP_ACCOUNT="1.0.4"
ARG FUSIO_APP_REDOC="1.0.2"

ARG COMPOSER_VERSION="2.7.5"
ARG COMPOSER_SHA256="0dc1f6bcb7a26ee165206010213c6069a537bf8e6533528739a864f154549b77"

# install default packages
RUN apt-get update && apt-get -y install \
    wget \
    git \
    unzip \
    cron \
    sudo \
    supervisor \
    default-mysql-client \
    libpq-dev \
    libxml2-dev \
    libcurl3-dev \
    libzip-dev \
    libonig-dev \
    libpng-dev \
    libmemcached-dev \
    openssl \
    libssl-dev \
    libcurl4-openssl-dev \
    sqlite3 \
    libsqlite3-dev \
    autoconf \
    build-essential

# install php extensions
RUN docker-php-ext-install pgsql
RUN docker-php-ext-install mysqli
RUN docker-php-ext-install pdo_mysql
RUN docker-php-ext-install pdo_pgsql
RUN docker-php-ext-install simplexml
RUN docker-php-ext-install dom
RUN docker-php-ext-install bcmath
RUN docker-php-ext-install curl
RUN docker-php-ext-install zip
RUN docker-php-ext-install mbstring
RUN docker-php-ext-install opcache
RUN docker-php-ext-install intl
RUN docker-php-ext-install xml
RUN docker-php-ext-install gd
RUN docker-php-ext-install soap
RUN docker-php-ext-install sockets

# install sqlite3 extension
RUN apt-get install -y libsqlite3-dev
RUN docker-php-source extract
RUN cd /usr/src/php/ext/sqlite3 && phpize && docker-php-ext-install sqlite3
RUN docker-php-source delete

# install pecl
RUN pecl install memcache-8.2 \
    && pecl install mongodb-1.18.1

RUN docker-php-ext-enable \
    memcache \
    mongodb

# install composer
RUN wget -O /usr/bin/composer https://getcomposer.org/download/${COMPOSER_VERSION}/composer.phar
RUN echo "${COMPOSER_SHA256} */usr/bin/composer" | sha256sum -c -
RUN chmod +x /usr/bin/composer

# install fusio
RUN mkdir /var/www/html/fusio
RUN wget -O /var/www/html/fusio/fusio.zip "https://github.com/apioo/fusio/releases/download/v${FUSIO_VERSION}/fusio.zip"
RUN cd /var/www/html/fusio && unzip fusio.zip
RUN rm /var/www/html/fusio/fusio.zip
RUN cd /var/www/html/fusio && /usr/bin/composer install --no-dev
RUN cd /var/www/html/fusio && /usr/bin/composer dump-autoload --no-dev --classmap-authoritative
COPY ./fusio /var/www/html/fusio
RUN chmod +x /var/www/html/fusio/bin/fusio

# create necessary directories
RUN mkdir -p /var/www/html/fusio/cache \
    /var/www/html/fusio/log \
    /var/www/html/fusio/public/apps \
    /var/www/html/fusio/public/apps/fusio \
    /var/www/html/fusio/public/apps/developer \
    /var/www/html/fusio/public/apps/account \
    /var/www/html/fusio/public/apps/redoc \
    /worker/java \
    /worker/javascript \
    /worker/php \
    /worker/python

# apache config
RUN rm /etc/apache2/sites-available/*.conf
RUN rm /etc/apache2/sites-enabled/*.conf
COPY ./apache/fusio.conf /etc/apache2/sites-available/fusio.conf
RUN a2enmod rewrite
RUN a2ensite fusio

# supervisor config
COPY supervisor/fusio.conf /etc/supervisor/conf.d/fusio.conf

# php config
RUN mv "${PHP_INI_DIR}/php.ini-production" "${PHP_INI_DIR}/php.ini"
COPY ./php/fusio.ini "${PHP_INI_DIR}/conf.d/fusio.ini"

# install additional connectors
RUN cd /var/www/html/fusio && \
    /usr/bin/composer require fusio/adapter-elasticsearch ^6.0 && \
    /usr/bin/composer require fusio/adapter-memcache ^6.0 && \
    /usr/bin/composer require fusio/adapter-mongodb ^6.0 && \
    /usr/bin/composer require symfony/sendgrid-mailer ^6.0 && \
    /usr/bin/composer require symfony/http-client ^6.0

# install apps
RUN mkdir /var/www/html/fusio/public/apps/fusio
RUN wget -O /var/www/html/fusio/public/apps/fusio/fusio.zip "https://github.com/apioo/fusio-apps-backend/releases/download/v${FUSIO_APP_BACKEND}/fusio.zip"
RUN cd /var/www/html/fusio/public/apps/fusio && unzip fusio.zip
RUN rm /var/www/html/fusio/public/apps/fusio/fusio.zip

RUN mkdir /var/www/html/fusio/public/apps/developer
RUN wget -O /var/www/html/fusio/public/apps/developer/developer.zip "https://github.com/apioo/fusio-apps-developer/releases/download/v${FUSIO_APP_DEVELOPER}/developer.zip"
RUN cd /var/www/html/fusio/public/apps/developer && unzip developer.zip
RUN rm /var/www/html/fusio/public/apps/developer/developer.zip

RUN mkdir /var/www/html/fusio/public/apps/account
RUN wget -O /var/www/html/fusio/public/apps/account/account.zip "https://github.com/apioo/fusio-apps-account/releases/download/v${FUSIO_APP_ACCOUNT}/account.zip"
RUN cd /var/www/html/fusio/public/apps/account && unzip account.zip
RUN rm /var/www/html/fusio/public/apps/account/account.zip

RUN wget -O /var/www/html/fusio/public/apps/redoc.zip "https://github.com/apioo/fusio-apps-redoc/archive/refs/tags/v${FUSIO_APP_REDOC}.zip"
RUN cd /var/www/html/fusio/public/apps && unzip redoc.zip
RUN rm /var/www/html/fusio/public/apps/redoc.zip
RUN cd /var/www/html/fusio/public/apps && mv fusio-apps-redoc-${FUSIO_APP_REDOC} redoc

# clean up files
RUN rm /var/www/html/fusio/public/install.php
RUN rm -r /tmp/pear

# chown
RUN chown -R www-data: /var/www/html/fusio

# create cron
RUN echo "" > /etc/cron.d/fusio
RUN echo "* * * * * www-data /var/www/html/fusio/run_cron.sh cronjob" >> /etc/cron.d/fusio
RUN echo "0 0 1 * * www-data /var/www/html/fusio/run_cron.sh log_rotate" >> /etc/cron.d/fusio
RUN echo "0 0 1 * * www-data /var/www/html/fusio/run_cron.sh clean" >> /etc/cron.d/fusio
RUN chmod 0644 /etc/cron.d/fusio
RUN chmod +x /var/www/html/fusio/run_cron.sh

# add entrypoint
COPY ./docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod +x /docker-entrypoint.sh

EXPOSE 80

ENTRYPOINT ["/docker-entrypoint.sh"]
