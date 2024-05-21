#!/bin/bash

path="./image-analysis/image-analysis.zip"

# download zip file
wget -O $path -q --show-progress https://aka.ms/mslearn-images-for-analysis
# extract images
unzip $path -d ./image-analysis
# remove .zip file
rm $path
