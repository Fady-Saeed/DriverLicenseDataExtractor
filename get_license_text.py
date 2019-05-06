import webbrowser as wb
import webencodings
import json
import requests as rqs
import numpy as np
import matplotlib.pyplot as plt
import cv2
import statistics as sts


def check_plate_text_and_no(plate_text) : 
    if '٤' in text : 
        text[index('٤')]  = \
        'ع'
    return text










def get_no_and_text(img) : 
    '''
	## img = image of box of letters and numbers 

    '''
    img = img[:,int(img.shape[1]/2):img.shape[1]]
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
        
        plate_text = all.replace(' ','')
	text = check_plate_text_and_no(plate_text)
 
        return text

