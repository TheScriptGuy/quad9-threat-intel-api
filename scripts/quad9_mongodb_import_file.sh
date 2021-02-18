#!/bin/bash

QUAD9_FILE=$1

DATABASE=quad9
COLLECTION=threatdata
NUM_INSERT_WORKERS=10

# Uncomment for specific mode
#INSERTMODE="--mode=upsert"

# sed expression
SED_EXPRESSION="s/^{\"id\"\(.*\)\,\"timestamp\"\:\"\(.*\)\"\,\"city\"\:\(.*\)$/{\"_id\"\1,\"timestamp\":\{\"\$date\":\"\2\" \},\"city\":\3/g"

zcat $QUAD9_FILE | sed -e $SED_EXPRESSION | mongoimport -d $DATABASE -c $COLLECTION -j $NUM_INSERT_WORKERS $INSERT_MODE

echo "$QUAD9_FILE ...processed"


