'''
Entropy method -- motified -- get rid of background
input : gray pic(cv2 image)
output : Threshold
'''

import cv2
import numpy as np
import math
from PIL import Image

#EN = entropy
def Entropy_get(img):
    T_EN = 0 # OTSU Threshold 
    H = []
    # get the list of every pixel probability
    w,h = img.shape
    pixsum = w*h #pixel sum 
    data = np.zeros((256),dtype=int)
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


    for j in range(0,256):
        if data_n[j] == 0:
            data_n[j] = 1


    for t in range(1,256):
        Hb = -1*sum(data_n[i]*math.log(data_n[i]) for i in range(0,t))
        Hw = -1*sum(data_n[i]*math.log(data_n[i]) for i in range(t,255))
        H.append(Hb+Hw)

    T_EN = H.index(max(H))
    
    return T_EN




if __name__ == "__main__":
    img = cv2.imread('/Users/zhangyesheng/Desktop/医学信息学/Project/temp/de_sk_fin4.jpg',-1)
    T = Entropy_get(img)
    print(T)
    T,imgd = cv2.threshold(img, T, 255, cv2.THRESH_BINARY)
    Ima = Image.fromarray(imgd)
    Ima.show() 


# if __name__ == "__main__":
#     img = cv2.imread('/Users/zhangyesheng/Desktop/Icon.JPG')
#     imgG = cv2.cvtColor(img,cv2.COLOR_RGB2GRAY)
#     T = Entropy_get(imgG)
#     T_idea,imgd = cv2.threshold(imgG, T, 255, cv2.THRESH_BINARY)
#     #print(T,'*',T_idea)
#     cv2.imshow('H',imgd)
#     cv2.waitKey(0)