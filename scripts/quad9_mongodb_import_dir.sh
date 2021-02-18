#!/bin/bash

QUAD9_DIR=$1

DATABASE=quad9
COLLECTION=threatdata
NUM_INSERT_WORKERS=10

# Uncomment for specific mode
#INSERTMODE="--mode=upsert"

# sed expression
SED_EXPRESSION="s/^{\"id\"\(.*\)\,\"timestamp\"\:\"\(.*\)\"\,\"city\"\:\(.*\)$/{\"_id\"\1,\"timestamp\":\{\"\$date\":\"\2\" \},\"city\":\3/g"

for i in `ls $QUAD9_DIR`
do
  zcat $QUAD9_DIR/$i | sed -e $SED_EXPRESSION | mongoimport -d $DATABASE -c $COLLECTION -j $NUM_INSERT_WORKERS $INSERT_MODE
  echo "$i ...processed"
done

