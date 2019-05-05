import requests as rqs
import numpy as np
import matplotlib.pyplot as plt
import cv2
import pytesseract
import base64
from split_and_get_no import split


f = lambda text ,number : text if not number else number 
arabic_numbers = ['٠' ,'١' , ' ٢' , '٣' , '٤' , '٥' , '٦' , '٧' ,'٨' , '٩' ]

f = lambda text ,number : text if not number else number 
arabic_numbers = ['٠' ,'١' , ' ٢' , '٣' , '٤' , '٥' , '٦' , '٧' ,'٨' , '٩' ]

def check_plate_text_and_no(plate_text , plate_no) : 
    if ( not plate_text or not plate_no ) : 
        print('One is empty ....')
        plate = f(plate_text,plate_no)
        print(plate[0] , plate[5])
        plate = plate.replace(' ','')
        #no =   [x for x in plate if x in arabic_numbers]
        #text = [x for x in plate if not(x in arabic_numbers)]
        text = list(plate[0:3])
        no = plate[3:]
        if '٤' in text : 
            #print('Found')
            text[index('٤')]  = \
            'ع'
        return int(1),text,no
    else :
        plate_text = plate_text.replace(' ','')
        plate_no = plate_no.replace(' ','')
        plate_text = list(plate_text[0:3])
        plate_no   = plate_no[0:3]
        #print(plate_text)
        if '٤' in plate_text : 
            #print('Found')
            plate_text[plate_text.index('٤')]  = \
            'ع'
        return 2,plate_text,plate_no
        
        











def get_no_and_text(image) : 
    '''
	## Path to image 

	path =  
    '''

    numImg, lettersImg = split(image)

    pytesseract.pytesseract.tesseract_cmd = r'/app/.apt/usr/bin/tesseract'
    digits = pytesseract.image_to_string(numImg, lang='ara_number')
    print("Digits : " + digits)

    _, lettersImg = cv2.imencode('.jpg', lettersImg)
    base64Image = base64.b64encode(lettersImg).decode()
    base64Image = 'data:image/jpg;base64,{}'.format(base64Image)
    
    payload = {'apikey': '310081fb4188957' ,
               'isOverlayRequired' : 'True' ,
               'language': 'ara' , 
               'detectOrientation' : 'True' , 
               'scale':'False',
               'base64Image': base64Image
              } 
    r = rqs.post('https://api.ocr.space/parse/image',
                    data=payload
                )
    d = r.json()
    print("Ocr Space JSON :")
    print(d)
    letters = d['ParsedResults'][0]['ParsedText']
    letters = letters.replace(" ", "")
    return letters, digits
