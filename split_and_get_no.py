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
	num_img = img[:,int(0:img.shape[1])]
	numbers = pst.image_to_string( num_img , lang='ara_number')
	return english_to_arabic(list(numbers))



## Call split(img) to get car numbers



