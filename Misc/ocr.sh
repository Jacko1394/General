#!/usr/bin/env bash

echo "Converting to TIF..."
gs -sDEVICE=tiffgray -r300 -o img.tif $1

echo "OCR-ing..."
tesseract img.tif $1

echo "Clearing TIF..."
rm -f ./img.tif

echo "DONE"
