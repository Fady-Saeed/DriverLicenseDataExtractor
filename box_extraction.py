import cv2
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.pyplot import figure
import statistics as sts

def get_bounding_box(img):
        
    # https://stackoverflow.com/questions/35854197/how-to-use-opencvs-connected-components-with-stats-in-python?fbclid=IwAR2oFmjaP_z7RTwvxh2hX86ChlZEvtY-MM8Qs2ybf2puftaFypbQiDk2veI

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (11,11))
    close = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)
    subt = cv2.subtract(close, img)
    
    ret, thresh = cv2.threshold(subt,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    connectivity = 4  
    output = cv2.connectedComponentsWithStats(thresh, connectivity, cv2.CV_32S)
    
    num_labels = output[0]
    labels = output[1]
    stats = output[2]
    centroids = output[3]
    
    # looping on the centroids of the circles and writing on each of them a number

    tmp = 1
    delta = 0
    mask = np.zeros(thresh.shape)
    
    max_length = 0
    max_index = 1


    for i in centroids[1:]:
        
        left_most_x = stats[tmp][0]
        upmost_y = stats[tmp][1]
        width = stats[tmp][2]
        height = stats[tmp][3]
        area = stats[tmp][4]
        
        x1 = int(left_most_x)
        y1 = int(upmost_y)
        
        x2 = int(x1 + width)
        y2 = int(y1 + height)
    
        if(max(width, height) > max_length):
            max_length = max(width, height)
            max_index = tmp

    
        tmp += 1
    
    

    left_most_x = stats[max_index][0]
    upmost_y = stats[max_index][1] 
    width = stats[max_index][2]
    height = stats[max_index][3]
        
    y_begin = upmost_y
    y_end = upmost_y + height
    x_begin = left_most_x 
    x_end = left_most_x+width

 
    return y_begin, y_end, x_begin, x_end

#####################################to test#################################### 
#img = cv2.imread("slice6.png", 0)

#y_begin, y_end, x_begin, x_end = get_bounding_box(img)


#plt.imshow(img[y_begin:y_end, x_begin:x_end])
    
    
    