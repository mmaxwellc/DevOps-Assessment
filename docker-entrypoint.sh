#!/bin/sh

php artisan key:generate
php artisan migrate 
php artisan db:seed
exec php-fpm