import cv2
import numpy as np
#import matplotlib.pyplot as plt
from sympy import Line, pi
import math
import statistics


def process(directory, extension=".png"):
    filename = directory+"/belakangk3"+extension
    #open image
    img = cv2.imread(filename)

    y=0
    x=0
    h=700
    w= 330
    crop = img[y:y+h, x:x+w]

    #convert to black and white
    imgray = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)

    #image thresholding
    ret, thresh = cv2.threshold(imgray, 10, 255, 0)

    edges = cv2.Canny(thresh, 100, 200)

    x1 = []
    y1 = []
    for x in range(0, edges.shape[0]):
        for y in range(0, edges.shape[1]):
            if edges[x, y] != 0:            
                x1 = x1 + [x]
                y1 = y1 + [y]

    #Filter Coordinates Pixel
    x1_kanan = x1[1::2]
    y1_kanan = y1[1::2]
    x1_kiri = x1[::2]
    y1_kiri = y1[::2]

    #Down Coordinates
    Max_down = max(x1_kanan)
    Max_down_index= x1_kiri.index(Max_down)
    Max_down_y = y1_kiri[Max_down_index:]
    b = len(Max_down_y)
    t = [Max_down]
    Max_down_x = [t[i//b] for i in range(len(t)*b)]

    #Median Coordinates 2 array
    leng1 = len(y1_kanan)
    middle_index1 = leng1//2
    leng2 = len(y1_kiri)
    middle_index2 = leng2//2
    kanan = y1_kanan[-200::20]
    kiri = y1_kiri[-200::20]
    res_list = []
    for i in range(0, len(kanan)):
        datt = (kanan[i] + kiri[i])//2
        res_list.append(datt)
    coordinates_same_res_list = x1_kanan[-200::20]

    #garis lurus
    x1_lower = res_list[1]
    y1_lower = coordinates_same_res_list[1]
    x2_lower = Max_down_y[0]
    y2_lower = Max_down_x[0]

    #garis bawah
    x3_lower = Max_down_y[0]
    y3_lower = Max_down_x[0]
    y4_lower = Max_down_x[0]
    x4_lower = y1_kiri[1]

    #Line
    cv2.line(img, (x1_lower, y1_lower), (x2_lower, y2_lower), (0, 255, 0), 5)
    cv2.line(img, (x3_lower, y3_lower), (x4_lower, y4_lower), (0, 255, 0), 5)

    #Find Angel
    L1 = Line((x1_lower, y1_lower), (x2_lower, y2_lower)) 
    L2 = Line((x3_lower, y3_lower), (x4_lower, y4_lower))
    rad = L1.angle_between(L2)
    derajat = math.degrees(rad)
    print(derajat)

    #Clasification
    if derajat < 80:
        index = 2
    elif 80 <= derajat <= 82:
        index = 1
    elif 82 < derajat <= 90:
        index = 0
    elif 91 < derajat <= 97:
        index = -1
    elif derajat >= 98:
        index = -2
    return index