FROM ubuntu:latest

# Add socat
RUN apt-get update && apt-get install -y \
	socat \
	&& rm -rf /var/lib/apt/lists/*

# Copy files
RUN mkdir -p /opt/app
COPY app/ /opt/app/
WORKDIR /opt/app
RUN chmod +x ./start.sh
RUN chmod a+r ./flag.txt

# Add user
RUN useradd -m ctflib

# Expose port and run
EXPOSE 4242
CMD ["/opt/app/start.sh"]
