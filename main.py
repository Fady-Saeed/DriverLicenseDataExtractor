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
    print(len(matches))
    
    ## Choosing best matches
    best_matches = []

    for match1 , match2 in matches : 
        if match1.distance < 0.75*match2.distance : 
            best_matches.append(match1)

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



## match_bottom_left and match_t -> 2 saved images (must be passed in order and in graysacle)
## image -> license image
## returns region of interest

def cut_image(match_bottom_left , match_t , image) : 
    x1,y1 = match_images(match_bottom_left , image , 0)
    x2,y2 = match_images(match_t,image , 1)
    
    if y1 < y2 : 
        #print('...More Processing ....')
        y_top_left = y1 - ((y2-y1)/2)
        if y_top_left <0 : 
            y_top_left = 0
        x_top_left = x1 - 25
        
        y_bottom_right = y2 + (2*(y2-y1))
        x_bottom_right = x2 + 2.5*(x2-x_top_left)
            
        #print(x_top_left ,y_top_left  , x_bottom_right , y_bottom_right)
        
        return image[int(y_top_left):int(y_bottom_right) , int(x_top_left):int(x_bottom_right)]
    else : 
        y_top_right = y2*2 - y1
        x_top_right = x2 + 2.5*(x2-x1)
        
        y_top_right = int(y_top_right)
        x_top_right = int(x_top_right)
        
        
        
        return image[int(y_top_right):int(y1+10) , int(x1-10):int(x_top_right)]
