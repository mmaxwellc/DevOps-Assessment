FROM php:8.3-fpm-alpine

ARG UID=2000
ARG GID=2000

# Create a new user and group with a specific UID and GID
RUN addgroup --system --gid ${GID} appuser \
    && adduser --system --ingroup appuser --uid ${UID} appuser

WORKDIR /app

COPY composer.json composer.lock /app/

COPY . /app

# Install system dependencies
RUN apk add --no-cache libzip-dev unzip \
    && docker-php-ext-install zip pdo_mysql

# Install composer
RUN curl -sS https://getcomposer.org/installer | php \
    && mv composer.phar /usr/bin/composer

# Install dependencies
RUN composer install -o

COPY docker-entrypoint.sh /app/docker-entrypoint.sh

RUN chmod +x /app/docker-entrypoint.sh \
    && chown -R appuser:appuser /app


USER appuser

EXPOSE 9000

ENTRYPOINT ["sh", "/app/docker-entrypoint.sh"]