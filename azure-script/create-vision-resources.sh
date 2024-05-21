#!/bin/bash

# Variables
rg="ai-vision-rg"
vision="ai-vision-01"
loc="westus"

# Create resource group
az group create --name $rg --location $loc

# Create Vision resource
az cognitiveservices account create \
    --name $vision \
    -g $rg \
    --kind ComputerVision \
    --sku F0 \
    --location $loc

# Retrieve and set key, format output 
VISION_KEY=$(az cognitiveservices account keys list \
 --name $vision \
 --resource-group $rg \
 --query "key1" -o tsv)
export VISION_KEY

# Retrieve and set endpoint, also format output
VISION_ENDPOINT=$(az cognitiveservices account show \
 --name $vision \
 --resource-group $rg \
 --query "properties.endpoint" -o tsv)
export VISION_ENDPOINT

# Confirm values
echo "VISION_KEY: $VISION_KEY"
echo "VISION_ENDPOINT: $VISION_ENDPOINT"
