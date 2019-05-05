import pytesseract as pst
import matplotlib.pyplot as plt
import cv2
import numpy as np
from PIL import Image



def english_to_arabic(num) : 
    english_numbers=['0','1','2','3','4','5','6','7','8','9']
    arabic_numbers = ['٠' ,'١' , ' ٢' , '٣' , '٤' , '٥' , '٦' , '٧' ,'٨' , '٩' ]
    new_lst=[]
    for i in num : 
        y = english_numbers.index(i)
        new_lst.append(arabic_numbers[y])
    return new_lst



def split(img) : 
	#img is GrayScale image
	num_img  = img[:,10:int(img.shape[1]/2)]
	text_img = img[:,int((img.shape[1]/2)+10):img.shape[1]]
	return num_img, text_img

def get_number(num_img) :
    return pst.image_to_string( num_img , lang='ara_number')


## Call split(img) to get car numbers



