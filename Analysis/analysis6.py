import numpy as np
#import matplotlib.pyplot as plt
import cv2
from findpeaks import findpeaks



def process(directory, extension=".png"):
    filename = directory+"/belakangk6"+extension
    #open image
    img = cv2.imread(filename)
    #crop
    y=0
    x=0
    h=700
    w= 340
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

    #Filter Coordinates Pixel Right
    y_kanan_position = [i for i in y1 if i>=value_y]
    panjang_kanan = len(y_kanan_position)
    x_kanan_position = x[0:panjang_kanan]

    fp = findpeaks(lookahead=1)
    results1 = fp.fit(y_kanan_position)
    a_kanan = results1['df']
    b_kanan = a_kanan.index[a_kanan['valley'] == True]
    index_drop_kanan = b_kanan.values.tolist()

    index_drop_minimum_abduksi_kanan = index_drop_kanan[1]
    nilai_minimum_abduksi_kanan = results1['df']['y'][index_drop_minimum_abduksi_kanan]
    x_position_abduksi_minimum_kanan = y_kanan_position.index(nilai_minimum_abduksi_kanan)

    y_kanan_optimasi = y_kanan_position[x_position_abduksi_minimum_kanan:]
    y_kanan_optimasi_max = max(y_kanan_optimasi)
    index_manipulasi_kanan = y_kanan_optimasi.index(y_kanan_optimasi_max)
    index_y_kanan_optimasi_max = x_position_abduksi_minimum_kanan + index_manipulasi_kanan
    x_kanan_optimasi_max = x_kanan_position[index_y_kanan_optimasi_max]

    nilai_maksimum_abduksi_kanan = max(y_kanan_position)
    x_position_abduksi_maksimum_kanan = x_kanan_position[y_kanan_position.index(nilai_maksimum_abduksi_kanan)]

    #Filter Coordinates Pixel Left
    y_kiri_position = [i for i in y1 if i<=value_y]
    panjang_kiri = len(y_kiri_position)
    x_kiri_position = x[0:panjang_kiri]

    fp = findpeaks(lookahead=1)
    results1 = fp.fit(y_kiri_position)
    a_kiri = results1['df']
    b_kiri = a_kiri.index[a_kiri['peak'] == True]
    index_drop_kiri = b_kiri.values.tolist()

    index_drop_minimum_abduksi_kiri = index_drop_kiri[0]
    nilai_minimum_abduksi_kiri = results1['df']['y'][index_drop_minimum_abduksi_kiri]
    x_position_abduksi_minimum_kiri = y_kiri_position.index(nilai_minimum_abduksi_kiri)

    y_kiri_optimasi = y_kiri_position[x_position_abduksi_minimum_kiri:]
    nilai_maksimum_abduksi_kiri = min(y_kiri_optimasi)
    index_manipulasi_kiri= y_kiri_optimasi.index(nilai_maksimum_abduksi_kiri)
    index_y_kiri_optimasi_min = x_position_abduksi_minimum_kiri + index_manipulasi_kiri
    x_position_abduksi_maksimum_kiri = x_kiri_position[index_y_kiri_optimasi_min]

    #Clasification
    abduksi_kanan = nilai_maksimum_abduksi_kanan - nilai_minimum_abduksi_kanan
    abduksi_kiri = (nilai_maksimum_abduksi_kiri - nilai_minimum_abduksi_kiri) * -1
    beda_6th = abduksi_kiri - abduksi_kanan

    if beda_6th >= 6:
        index = 2
    elif -5 <= beda_6th <= 6:
        index = 1
    elif -46 <= beda_6th < -5:
        index = 0
    elif -92 <= beda_6th < -47:
        index = -1
    elif beda_6th < -92:
        index = -2
    return index