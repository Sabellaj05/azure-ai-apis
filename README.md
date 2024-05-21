# Azure AI Vision in Python

## Provision Resources

First we create the *AI Vision* resource on our Azure Subscription

We log in

```bash
az login
```
Let's define some variables to not type as much

```bash
rg="ai-vision-rg"
vision="ai-vision-01"
loc="West US"

```

Now we create the resource group

```bash
az group create \
	--name $rg \
	--location $loc
```
We then create the resource 

```bash
az cognitiveservices account create \
	--name $vision \
	--resource-group $rg \
	--kind ComputerVision \
	--sku F0 \
	--location $loc
```
Now we need to retrieve the *key* and *endpoint* to use later

```bash
az cognitive services account keys list \
	--name $vision \
	-g $rg \
	&& \
	az cognitive services account show \
	--name $vision \
	-g $rg \
	--query "properties.endpoint"
```
Set the environment variables for the key and endpoint

```bash
export VISION_KEY="<key>"
export VISION_ENDPOINT="<endpoint>"
```
Alternative,  we can just put all together on a simple script and run that

```bash
#!/bin/bash

# Variables
rg="ai-vision-rg"
vision="ai-vision-01"
loc="West US"

# Create resource group
az group create --name $rg --location $location

# Create Vision resource
az cognitiveservices account create \
    --name $vision \
    -g $rg \
    --kind ComputerVision \
    --sku S0 \
    --location $location

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

```
We make the script executable and run it

```bash
chmod +x create-vision.sh
./create-vision.sh
```
If we don't need the resource anymore we **destroy it**

```bash
az group delete \ 
--name $rg \
--yes
```
Verify 

```bash
az group show --name $rg
```

## Python Vision SDK

Structure

```
.
├── azure-script
│   └── create-vision-resources.sh
├── README.md
└── src
    ├── main.py
    ├── __pycache__
    │   ├── utils.cpython-311.pyc
    │   ├── validate.cpython-311.pyc
    │   └── vision_functions.cpython-311.pyc
    ├── sample.jpg
    ├── utils.py
    ├── validate.py
    └── vision_functions.py
```

**vision_functions.py** has a `VisionFunctions` Class with diferent azure vision api functions, like **OCR** **Face detection** etc.


