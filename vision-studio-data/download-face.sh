#!/bin/bash

path="./face-recognition/detect-faces.zip"

# download zip file
wget -O $path -q --show-progress https://aka.ms/mslearn-detect-faces
# extract images
unzip $path -d ./face-recognition
# remove .zip file
rm $path
