import numpy as np
#import matplotlib.pyplot as plt
import cv2
import math


def process(directory, extension=".png"):
    filename = directory+"/samping"+extension
    #open image
    img = cv2.imread(filename)
    #convert to black and white
    imgray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    blur = cv2.GaussianBlur(imgray,(9,9),0)

    #image thresholding
    ret, thresh = cv2.threshold(blur, 10, 255, 0)

    #filling holes
    im_floodfill = thresh.copy()
    h, w = thresh.shape[:2]
    mask = np.zeros((h+2, w+2), np.uint8)
    cv2.floodFill(im_floodfill, mask, (0,0), 255);
    im_floodfill_inv = cv2.bitwise_not(im_floodfill)
    im_out = thresh | im_floodfill_inv

    #contour image
    edges = cv2.Canny(im_out, 40, 200)

    #proses
    ans = []
    for x in range(0, edges.shape[0]):
        for y in range(0, edges.shape[1]):
            if edges[x, y] != 0:            
                ans = ans + [[x,y]]

    #Normalisasi
    normalisasi = ans[2]
    normalisasi_crop = normalisasi[-1]
    y=0
    x=0
    h=700
    w=normalisasi_crop-27
    crop = edges[y:y+h, x:x+w]

    #Shape Normalisasi
    x1 = []
    y1 = []
    for x in range(0, crop.shape[0]):
        for y in range(0, crop.shape[1]):
            if crop[x, y] != 0:            
                x1 = x1 + [x]
                y1 = y1 + [y]

    #Feature
    max_kory = max(y1)
    index_ymax = y1.index(max_kory)
    korx_maxkory = x1[index_ymax]

    #Normalisasi1
    y1=korx_maxkory
    x1=0
    h1=700
    w1=700
    crop1 = crop[y1:y1+h1, x1:x1+w1]

    #Shape Normalisasi1
    x2 = []
    y2 = []
    for x in range(0, crop1.shape[0]):
        for y in range(0, crop1.shape[1]):
            if crop1[x, y] != 0:            
                x2 = x2 + [x]
                y2 = y2 + [y]

    #find the highest value longitudinal arch 
    max_korx = max(x2)
    index_xmax = x2.index(max_korx)
    kory_maxkorx = y2[index_xmax]

    norm_longitudinal_arch = kory_maxkorx + 90
    index_norm_longitudinal_arch = y2.index(norm_longitudinal_arch)
    x_norm_longitudinal_arch = x2[index_norm_longitudinal_arch]

    #clasification
    highest_value_longitudinalArch = max_korx - x_norm_longitudinal_arch

    if highest_value_longitudinalArch >= 57:
        index = -2
    elif 55  < highest_value_longitudinalArch <= 56:
        index = -1
    elif 34 < highest_value_longitudinalArch <= 54:
        index = 0
    elif 32 <= highest_value_longitudinalArch <= 34:
        index = 1
    elif highest_value_longitudinalArch <= 31:
        index = 2
    return index