'''
OTSU algorithm
input : gray pic (cv2 Image)
output : Threshold
'''


import cv2
import numpy as np
from PIL import Image
from DilateAndErosion import *



'''
需要算出每个像素的概率
修改过的OTSU
将背景置为两个峰中的一个
'''
def OTSU_GET(img):
    T_OTSU = 0 # OTSU Threshold 
    delta = []
    # get the list of every pixel probability
    w,h = img.shape
    pixsum = w*h #pixel sum 
    data = np.zeros([256,1],dtype=int)
    for i in range(0,w):
        for j in range(0,h):
            data[int(img[i,j])]+=1
    data = data/pixsum 

    # Get rid of the background
    data_no_zero = list(data[1:])
    Max = max(data_no_zero)
    pix_val = data_no_zero.index(Max) + 1
    
    img_zero_index = np.argwhere(img < 150)
    num, temp = img_zero_index.shape
    for i in range(num):
        img[img_zero_index[i,0],img_zero_index[i,1]] = pix_val

    # Ima = Image.fromarray(img)
    # Ima.show() 

    data_n = np.zeros([256,1],dtype=int)
    for i in range(0,w):
        for j in range(0,h):
            data_n[int(img[i,j])]+=1
    data_n = data_n/pixsum 

    for t in range(1,256):

        w0 = sum(data_n[0:t])
        if w0 == 0:
            u0 = 0
        else:
            u0 = sum(i*data_n[i] for i in range(0,t))/w0

        w1 = sum(data_n[t:255])
        if w1 == 0:
            u1 = 0
        else:
            u1 = sum(j*data_n[j] for j in range(t,255))/w1

        delta.append(w0*w1*(u1-u0)*(u1-u0))
    
    max_de = max(delta)
    T_OTSU = delta.index(max_de)

    return T_OTSU





if __name__ == "__main__":
    img = cv2.imread('/Users/zhangyesheng/Desktop/医学信息学/Project/temp/de_sk_fin4.jpg',-1)
    # size = 3
    # Med = np.ones(size)
    # Med = Med/size
    # Img_B_M = cv2.filter2D(img,-1,Med)
    T = OTSU_GET(img)
    # print(T)
    T,imgd = cv2.threshold(img, T, 255, cv2.THRESH_BINARY)
    # SE = np.ones(([3,3]),dtype='bool')
    # Img_DR = DilationGet(imgd, SE) 
    # none, Img_DR = cv2.threshold(Img_DR,0,255,cv2.THRESH_BINARY)
    # Img_DR_ER = ErosionGet(Img_DR, SE)
    
    # none, Img_DR_ER = cv2.threshold(Img_DR_ER,0,255,cv2.THRESH_BINARY)

    Ima = Image.fromarray(imgd)
    Ima.show() 





# if __name__ == "__main__":
#     img = cv2.imread('/Users/zhangyesheng/Desktop/DOG.JPG')
#     imgG = cv2.cvtColor(img,cv2.COLOR_RGB2GRAY)
#     T = OTSU_GET(imgG)
#     T_idea,imgd = cv2.threshold(imgG, T, 255, cv2.THRESH_BINARY)
#     #print(T,'*',T_idea)
#     cv2.imshow('H',imgd)
#     cv2.waitKey(0)
    