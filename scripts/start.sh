#!/bin/sh

# Author         : dryiceza 
# Date created   : 2020-12-26
# Version        : 0.01
# Changelog      : None - first creation


# Define variables - change these to your needs
QUAD9_AUTH_TOKEN=<TOKEN>
QUAD9_CONNECTIONS=2
OUTPUTDIR=/quad9-intel-data/

# Uncomment this line if you want to test connectivity first before downloading all the data.
#NOACK="--noack"


# ---------------------------------------------------------------------------
# DO NOT EDIT BELOW HERE

# Define functions to catch attempts to shutdown python script.

_term_SIGTERM() { 
  echo "Caught SIGTERM signal!" 
  echo "PID - $child"
  kill -15 $child

  # This ensures that python script has a chance to write all it's contents to a file.
  # Adjust based on speed of disk area that is being written to.
  sleep 5 
}

_term_SIGINT() {
  echo "Caught SIGINT signal!"
  echo "PID - $child"
  kill -15 $child

  # This ensures that python script has a chance to write all it's contents to a file.
  # Adjust based on speed of disk area that is being written to.
  sleep 5
}


# What signals are we going to capture and run appropriate functions.
trap _term_SIGTERM SIGTERM
trap _term_SIGINT SIGINT

echo "Starting Quad9 Threat Intel Python Script";
python3 /scripts/quad9-threat-intel-download.py  --connections $QUAD9_CONNECTIONS $NOACK --auth_token $QUAD9_AUTH_TOKEN --output_dir $OUTPUTDIR &

child=$! 
wait "$child"

