#!/bin/bash

# Get the filename of the JSON file
filename="data/requests.json"
url="http://127.0.0.1:8000/predict"

# Open the JSON file in read mode
# file=open(filename)

while IFS= read -r line; do
    curl -X 'POST' 'http://127.0.0.1:8000/predict' \
        -H 'accept: application/json' \
        -H 'Content-Type: application/json' \
        -d "$line"

# Close the JSON file
done < "$filename"