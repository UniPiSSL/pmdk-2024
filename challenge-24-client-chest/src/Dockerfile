FROM nginx:alpine

# Copy challenge files
RUN rm -rf /usr/share/nginx/html
COPY html /usr/share/nginx/html
RUN chmod -R 777 /usr/share/nginx/html

# Expose port
EXPOSE 80
