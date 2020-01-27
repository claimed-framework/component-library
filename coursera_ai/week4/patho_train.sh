#!/bin/bash
if [ -f IDC_regular_ps50_idx5.zip ]; then echo "images already downloaded"; else wget http://andrewjanowczyk.com/wp-static/IDC_regular_ps50_idx5.zip; fi
if [ -d images ]; then echo "images folder already created"; else echo "creating images folder and unzipping "; mkdir images;  unzip IDC_regular_ps50_idx5.zip -d images/ ; fi
mkdir imagesprep
mkdir imagesprep/train
mkdir imagesprep/train/0
mkdir imagesprep/train/1
mkdir imagesprep/test
mkdir imagesprep/test/0
mkdir imagesprep/test/1

i=0
for file in `find images` -name ".png"; do 
    ((i++))
    if ! ((i % 10 == 0)); then 
        if [[ $file == *"class0.png"* ]]; then 
            cp $file imagesprep/train/0/
        elif [[ $file == *"class1.png"* ]]; then 
            cp $file imagesprep/train/1/
        fi
    else 
        if [[ $file == *"class0.png"* ]]; then 
            cp $file imagesprep/test/0/
        elif [[ $file == *"class1.png"* ]]; then 
            cp $file imagesprep/test/1/
        fi
    fi
done
