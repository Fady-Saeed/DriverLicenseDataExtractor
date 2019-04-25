#imports

import cv2
import numpy as np
import matplotlib.pyplot as plt
%matplotlib inline



#define a function to display images in large size

def display_img(img,name):
    
    output = img
    fig = plt.figure(figsize=(12,10))
    ax = fig.add_subplot(111)
    plt.title(name)
    ax.imshow(output)
    
    



def get_box(img):

    x = img.shape[0]
    y = img.shape[1]

   

    #the required box is black, so if we use closing it will be removed
    #then by subtracting original from closing we remove background and get photo containing words and box 


    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (11,11))
    close = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)

    subt = cv2.subtract(close, img)

    #use binary thresholding to remove background noise

    subt_max = np.max(subt)
    percent = 0.5

    rey, thresh_out = cv2.threshold(subt, percent*subt_max, 255, cv2.THRESH_BINARY)

    # use hough lines to get the boundary of the box

    minLineLength = 30
    maxLineGap = 1

    img2 =  np.zeros(img.shape)

    lines = cv2.HoughLinesP(thresh_out,1,np.pi/360, 150, minLineLength,maxLineGap)

    x_min = img2.shape[1]
    x_max = 0

    y_min = img2.shape[0]
    y_max = 0

    #3 distances with 6 points


    for line in lines:
        for x1,y1,x2,y2 in line:

            dist = np.square(x2-x1) + np.square(y2-y1)


            if(dist < 2500):
                continue


            tmp = min(y1, y2)

            if(y_min > tmp):
                y_min = tmp

            tmp = min(x1, x2) 

            if(x_min > tmp):
                x_min = tmp


            tmp = max(y1, y2)

            if(y_max < tmp):
                y_max = tmp

            tmp = max(x1, x2)

            if(x_max < tmp):
                x_max = tmp   




            cv2.line(img2,(x1,y1),(x2,y2),(255,0,0),1)




    delta  = 20

    y_begin = 0
    y_end = img2.shape[0]

    x_begin = 0
    x_end = img2.shape[1]


    if( y_min-delta >= 0):
        y_begin = y_min-delta

    if( y_max + delta <= y_end):
        y_end = y_max + delta

    if( x_min-delta >= 0):
        x_begin = x_min-delta

    if( y_max + delta <= y_end):
        x_end = x_max + delta


    slice = np.copy(img[y_begin: y_end, x_begin: x_end])

    return slice





    
    