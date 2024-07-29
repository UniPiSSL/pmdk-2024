FROM ruby:3.0-slim

# set environment variables
ENV APP_PORT 4242

RUN apt-get update && \
    apt-get install -y --no-install-recommends build-essential && \
    rm -rf /var/lib/apt/lists/*

# Copy challenge files
RUN mkdir -p /opt/app
COPY app/ /opt/app/
WORKDIR /opt/app

# Install gems
RUN bundle install

# Execute
EXPOSE 4242
CMD ["/bin/sh", "/opt/app/serve.sh"]
