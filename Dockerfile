# Start with minimal install of alpine
FROM alpine

# Grab updates, and install packages
RUN apk update
RUN apk add --no-cache python3 py3-pip
RUN apk add --no-cache tzdata
RUN pip3 install asyncio websockets argparse

# Configure Time Zone
ENV TZ=America/Los_Angeles
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Define stop signals to help with graceful stop of quad9 service
STOPSIGNAL SIGINT
