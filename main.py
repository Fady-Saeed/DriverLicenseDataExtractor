

## Imports
import cv2
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.pyplot import figure
import statistics as sts


##Matching images using SIFT feature detection

def match_images(match, img , mini) : 
    sift = cv2.xfeatures2d.SIFT_create()

    kp1 , des1 = sift.detectAndCompute(match , None)
    kp2 , des2 = sift.detectAndCompute(img , None)

    matcher = cv2.BFMatcher()
    matches = matcher.knnMatch(des1 , des2 , k=2)
    #print(len(matches))
    
    ## Choosing best matches
    best_matches = []

    for match1 , match2 in matches : 
        if match1.distance < 0.75*match2.distance : 
            best_matches.append(match1)
    if len(best_matches)==0 : 
	best_matches = matches

    ## get X,Y
    list_kp1 = []
    list_kp2 = []

    for mat in best_matches : 
        img1_idx = mat.queryIdx
        img2_idx = mat.trainIdx

        # x - columns
        # y - rows
        # Get the coordinates
        (x1,y1) = kp1[img1_idx].pt
        (x2,y2) = kp2[img2_idx].pt

        # Append to each list
        list_kp1.append((x1, y1))
        list_kp2.append((x2, y2))
    
    #normalizing x and y 
    a = [x[0] for x in list_kp2]
    b = [x[1] for x in list_kp2]
    #print(a)
    

    #print(len(list_kp1))
    #print(len(list_kp2))
    #print(len(a))
    #print(len(best_matches))
    #print('Mean is s ', sts.median(a))
    if mini : 
        returned = min(b)
        #print('Min of Y ' , returned)
    else : 
        returned = max(b)
        #print('Max of Y ', returned)
    
   # print(list_kp1[0])
   # print(list_kp2)
    #print(b)

    final = cv2.drawMatchesKnn(match , kp1 , img , kp2 , [best_matches] , None , flags = 2)
    #fig = plt.figure(figsize=(18,12))
    #plt.imshow(final)
    return sts.median(a) , returned



def cut_image(match_bottom_left , match_t , image) : 
    #plt.imshow(image)
    x1,y1 = match_images(match_bottom_left , image , 1)
    x2,y2 = match_images(match_t,image , 0)
    
    if y1 < y2 : 
        #print('...More Processing ....')
        y_top_left = y1 - ((y2-y1)/2)
        if y_top_left <0 : 
            y_top_left = 0
        x_top_left =max(0,x1 - 25)
        
        y_bottom_right = y2 + (2*(y2-y1))
        #print('Diff in x is',x2-x_top_left)
        x_bottom_right = x2 + 7*(x2-x_top_left)
            
        #print(x_top_left ,y_top_left  , x_bottom_right , y_bottom_right)
        
        return image[int(y_top_left):int(y_bottom_right) , int(x_top_left):int(x_bottom_right)]
    else : 
        y_top_right = y2*2 - y1
        x_top_right = x2 + 2.5*(x2-x1)
        
        y_top_right = int(y_top_right)
        x_top_right = int(x_top_right)
                
        
        return image[int(y_top_right):int(y1+30) , max(0,int(x1-40)):int(x_top_right)]



def get_bounding_box(img):
        
    # https://stackoverflow.com/questions/35854197/how-to-use-opencvs-connected-components-with-stats-in-python?fbclid=IwAR2oFmjaP_z7RTwvxh2hX86ChlZEvtY-MM8Qs2ybf2puftaFypbQiDk2veI

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (11,11))
    close = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)
    subt = cv2.subtract(close, img)
    
    src = np.copy(subt)
    
    ret, thresh = cv2.threshold(src,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
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

 
    return img[y_begin:y_end, x_begin:x_end]


## To get final image :-  img = get_bounding_box( cut_image(match_bottom , match_t , image ) )  
## Where match_bottom , match are the two images in images folder 
## Apply cv2.pyrUp(img) to obtain smaller image to pass to OCR

