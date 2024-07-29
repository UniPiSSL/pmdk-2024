FROM python:slim

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Add apt requirements
RUN apt-get update && apt-get install -y socat \
    && rm -rf /var/lib/apt/lists/*

# Prepare folder
RUN mkdir -p /opt/app
WORKDIR /opt/app

# Add python requirements
COPY app/requirements.txt /opt/app/requirements.txt
RUN pip install -r requirements.txt --no-cache-dir

# Copy all the files
COPY app/ /opt/app/

# Create a non-root user named 'ctf'
RUN useradd -m ctf
# Set ownership (root) and permissions (read & execute for all)
RUN chown -R root:root /opt/app && \
    chmod -R 555 /opt/app

# Expose port 1337
EXPOSE 1337

# Run challenge
CMD socat TCP4-LISTEN:1337,reuseaddr,fork EXEC:"python server.py",stderr,pty,iexten=0,echo=0
