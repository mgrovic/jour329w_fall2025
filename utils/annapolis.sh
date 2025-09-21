#!/bin/bash

# Script to filter posts with category 154 from cns_maryland_posts.json
# Usage: ./annapolis.sh

# Set the data directory path
DATA_DIR="../data"
INPUT_FILE="$DATA_DIR/cns_maryland_posts.json"
OUTPUT_FILE="$DATA_DIR/annapolis.json"

# Check if input file exists
if [ ! -f "$INPUT_FILE" ]; then
    echo "Error: Input file $INPUT_FILE not found!"
    exit 1
fi

echo "Filtering posts with category 154..."

# Use jq to filter posts that have category 154
# Categories is an array, so we check if 154 is contained in it
jq '[.[] | select(.categories | contains([154]))]' "$INPUT_FILE" > "$OUTPUT_FILE"

# Check if the operation was successful
if [ $? -eq 0 ]; then
    # Count the number of posts in the output file
    COUNT=$(jq 'length' "$OUTPUT_FILE")
    echo "Success! Found $COUNT posts with category 154"
    echo "Output saved to: $OUTPUT_FILE"
else
    echo "Error: Failed to process the file"
    exit 1
fi
