#!/bin/sh

# Serve application
bundle exec rackup --host 0.0.0.0 -p $APP_PORT
