import webbrowser as wb
import webencodings
import json
import requests as rqs
import numpy as np
import matplotlib.pyplot as plt
import cv2
import statistics as sts



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
        
        











def get_no_and_text() : 
    '''
	## Path to image 

	path =  
    '''
    payload = {'apikey': '310081fb4188957' ,
               'isOverlayRequired' : 'True' ,
               'language': 'ara' , 
               'detectOrientation' : 'True' , 
               'scale':'True'
              }
    with open(path, 'rb') as f: 
        r = rqs.post('https://api.ocr.space/parse/image',
                     data=payload,
                     files={path:f}
                    )
         d = r.json()
        all = d['ParsedResults'][0]['ParsedText']
        #print(len(d['ParsedResults'][0]['TextOverlay']['Lines']))
        lis = all.split('\r\n')
        plate_no = lis[0]
        plate_text = lis[1]
        #print(plate_no , plate_text)
        _ , text , no = check_plate_text_and_no(plate_text,plate_no)
        num = [no[-1],no[-2],no[-3]]
        return text , num
