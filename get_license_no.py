import webbrowser as wb
import webencodings
import json
import requests as rqs
import numpy as np
import matplotlib.pyplot as plt
import cv2
import statistics as sts



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
        print(plate_no , plate_text)
        return plate_no , plate_text
