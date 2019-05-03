import requests as rqs
import numpy as np
import matplotlib.pyplot as plt
import cv2
import statistics as sts











def get_id(base64Image) :
    '''
    Put path to image in path
    ''' 
 
    payload = {'apikey': '310081fb4188957' ,
               'isOverlayRequired' : 'True' ,
               'language': 'eng' , 
               'detectOrientation' : 'True' , 
               'scale':'True',
               'base64Image': base64Image
              }
    r = rqs.post('https://api.ocr.space/parse/image',
                    data=payload
                )
    d = r.json()
    print(d)
    print(d['ParsedResults'][0]['ParsedText'])
    lis = d['ParsedResults'][0]['ParsedText'].split('\r\n')
    id_no = lis[0]
    print(id_no)
    return id_no