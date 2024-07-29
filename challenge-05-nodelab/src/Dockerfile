FROM node:slim

# set environment variables
ENV APP_PORT 4242

# Copy challenge files
RUN mkdir -p /opt/app
COPY app/ /opt/app/
WORKDIR /opt/app

# Install dependencies
RUN npm install

# Execute
EXPOSE 4242
CMD ["server.js"]
