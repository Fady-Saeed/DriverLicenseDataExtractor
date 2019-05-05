echo "############## Downloading Tessdata files"
cd .apt/usr/share/tesseract-ocr/4.00/tessdata
wget https://github.com/ahmed-tea/tessdata_Arabic_Numbers/raw/master/ara_number.traineddata
wget https://github.com/tesseract-ocr/tessdata/raw/master/script/Arabic.traineddata
echo "############## Downloaded Tessdata files"