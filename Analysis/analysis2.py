import numpy as np
#import matplotlib.pyplot as plt
import cv2
from findpeaks import findpeaks
import math

def process(directory, extension=".png"):
    filename = directory+"/belakangk2"+extension
    #open image
    img = cv2.imread(filename)

    #crop
    y=0
    x=0
    h= 350
    w= 330
    crop = img[y:y+h, x:x+w]

    #convert to black and white
    imgray = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)

    #gaussian blur
    blur = cv2.GaussianBlur(imgray,(9,9),0)

    #image thresholding
    ret, thresh = cv2.threshold(blur, 10, 255, 0)

    #contour image
    edges = cv2.Canny(thresh, 100, 200)

    x1 = []
    y1 = []
    for x in range(0, edges.shape[0]):
        for y in range(0, edges.shape[1]):
            if edges[x, y] != 0:            
                x1 = x1 + [x]
                y1 = y1 + [y]
    x = x1[::2]
    max_x = max(x1)
    index_x = x1.index(max_x)
    value_y = y1[index_x]

    #Filter Coordinates Pixel Left
    y_kiri_position = [i for i in y1 if i<=value_y]
    panjang_kiri = len(y_kiri_position)
    x_kiri_position = x[0:panjang_kiri]

    fp = findpeaks(lookahead=1)
    results1 = fp.fit(y_kiri_position)
    a_kiri = results1['df']
    b_kiri = a_kiri.index[a_kiri['peak'] == True]
    index_drop_kiri = b_kiri.values.tolist()

    #find supralateral value
    index_peak = index_drop_kiri[0]
    nilai_lengkung_supralateral = results1['df']['y'][index_peak]
    x_position_supralateral = y_kiri_position.index(nilai_lengkung_supralateral)

    #find Infralateral value
    index_peak1 = index_drop_kiri[1]
    nilai_lengkung_infralateral = results1['df']['y'][index_peak1]
    x_position_infralateral = y_kiri_position.index(nilai_lengkung_infralateral)

    #Clasification
    beda_2nd =  nilai_lengkung_supralateral - nilai_lengkung_infralateral
    print(beda_2nd)
    if beda_2nd <= -3:
        index = 2
    elif -2 < beda_2nd <= -1:
        index = 1
    elif 0 <= beda_2nd <= 14:
        index = 0
    elif 15 <= beda_2nd < 17:
        index = -1
    elif beda_2nd < 17:
        index = -2

    return index