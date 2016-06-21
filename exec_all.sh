#!/bin/bash

ENV_PATH="$1"
OUTPUT_DIR="$2"
DATE=$(date +"%d-%m-%y")
LOGLEVEL="--loglevel INFO"

STORES=("AlienTech" "Chiptec" "PCDiga" "Globaldata")

cd $(dirname $0)
source "$ENV_PATH/bin/activate"
for store in "${STORES[@]}"
do
    echo "Running fetcher for $store..."
    lower=$(echo $store | tr '[:upper:]' '[:lower:]')
    ARGS="$store -o $OUTPUT_DIR/$lower-$DATE.csv --logfile $OUTPUT_DIR/$lower-$DATE.log $LOGLEVEL"
    scrapy crawl $ARGS &
done

wait
echo "Done!"
