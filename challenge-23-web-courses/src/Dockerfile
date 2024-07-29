FROM php:apache

# Copy challenge files
RUN rm -rf /var/www/html
COPY html /var/www/html
COPY flag.txt /var/www/flag.txt
RUN chmod -R 777 /var/www/

# Expose port
EXPOSE 80
