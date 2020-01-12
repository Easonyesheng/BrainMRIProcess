'''
get rid of skull
    1. use the original DICOM pixel array -- make the highest to 0
    2. use conditional dilation
'''

import cv2
import numpy as np 
from Imread import DicomIn 
from DilateAndErosion import *
from PIL import Image,ImageQt
import time


TempPath='/Users/zhangyesheng/Desktop/temp/ConDSkull/'


'''
output : img - 0 & 255
'''
def OpenSk(SE,img):
    Img_ER = ErosionGet(img, SE) 
    none, Img_ER = cv2.threshold(Img_ER,0,255,cv2.THRESH_BINARY)
    Img_ER_DR = DilationGet(Img_ER, SE)
    none, Img_ER_DR = cv2.threshold(Img_ER_DR,0,255,cv2.THRESH_BINARY)

    
    name = TempPath+'Open.jpg'
    cv2.imwrite(name,Img_ER_DR)
    Im_show = cv2.imread(name,-1) 
    
    return Im_show

'''
Conditional Dialate
input : img & line's position
output : img_R
'''
def ConDia_Sk(img,lineP,TempPath='/Users/zhangyesheng/Desktop/temp/ConDSkull/'):
    
    w,h = img.shape
    path = TempPath
    cv2.imwrite(path+'Ori.jpg',img*255)
    # cv2.imwrite(path+'Ori.jpg',img*255)
    img = img.astype(np.int)
    img_line = np.zeros([w,h],dtype='int')
    img_line[:,lineP] = 1
    
    
    temp = np.zeros([w,h],dtype='int')
    SE = np.ones([3,3],dtype='bool')
    c = 0
    img_grayt = img.astype(np.bool)
    # print(img_grayt.dtype)
    
    # img_graytl = img_grayt*255
    a = 0
    b = 0
    while(True):
        print(c)
        img_line = DilationGet(img_line,SE)
        temp = img_line.copy()
        # print(temp.dtype)
        # temp = temp.astype(np.int)
        # img_line = img_line.astype(np.bool)
        img_line = img_line & img_grayt # 0 & 1
        img_line = img_line.astype(np.int)
        # print(img_line.dtype)
        img_l = img_line*255
    
        cv2.imwrite(path+str(c)+'.jpg',img_l)
        c+=1
        # print((temp == img_line).all())
        res = temp == img_line
        a = np.sum(res == False)
        if (a == b):
            break
        b = a
        
    return img_line.astype(np.int)


'''
Use the different value of skull in MRI to de-skull
input : DICOM array
output : image array
'''
def DSk_DICOM(array):
    Max = array.max()

    index_min = np.argwhere(array < 300)
    index_max = np.argwhere(array > Max-100)
    # print('Min: ',Min)
    # print('index shape: ',index.shape)
    num, temp = index_min.shape
    for i in range(num):
        array[index_min[i,0],index_min[i,1]] = 0

    num, temp = index_max.shape
    for i in range(num):
        array[index_max[i,0],index_max[i,1]] = 0


    array = (array/array.max())*255
    return array


'''
Combined Method
input : DICOM array
output : image array : [0,255]
'''
def DSK_DI_Morpho(array):

    t = str(time.time())[-1]

    Max = array.max()

    index_min = np.argwhere(array < 300)
    index_max = np.argwhere(array > Max-100)
    # print('Min: ',Min)
    # print('index shape: ',index.shape)
    num, temp = index_min.shape
    for i in range(num):
        array[index_min[i,0],index_min[i,1]] = 0

    num, temp = index_max.shape
    for i in range(num):
        array[index_max[i,0],index_max[i,1]] = 0


    array = (array/array.max())*255

    
    # Threshod
    Mask = np.where(array>21,1,0)
    w, h = Mask.shape

    for i in range(h):
        if (array[:,i]>0).any():
            lineP = i
            break
    
    Mask = ConDia_Sk(Mask, lineP, )
    Mask_ = (Mask*255)
    cv2.imwrite(TempPath+'Mask.jpg',Mask_)
    array = array - Mask_
    cv2.imwrite('/Users/zhangyesheng/Desktop/医学信息学/Project/temp/de_sk'+t+'.jpg',array) # Skull deminished
    # Open
    img = cv2.imread('/Users/zhangyesheng/Desktop/医学信息学/Project/temp/de_sk'+t+'.jpg',-1)
    Mask2 = np.where(img>21,1,0) * 255
    '''
    The SE size need to change accroding to differrent images
    '''
    SE = np.ones([11,11],dtype='bool') 
    Mask2 = OpenSk(SE, Mask2)
    cv2.imwrite('/Users/zhangyesheng/Desktop/医学信息学/Project/temp/mask'+t+'.jpg',Mask2)
    Mask3 = cv2.imread('/Users/zhangyesheng/Desktop/医学信息学/Project/temp/mask'+t+'.jpg',-1)
    array = array * (Mask3).astype('int')

    array = (array/array.max())*255   # get rid of small dots 

    return array






DICOMPath = '/Users/zhangyesheng/Desktop/医学信息学/BrainMRIProcess/Dicom_Seg/brain_013.dcm'


if __name__ == "__main__":
    info, PixelArray = DicomIn(DICOMPath)
    array_no_skull = DSk_DICOM(PixelArray)
    # array_no_skull = DSK_DI_Morpho(PixelArray)
    # cv2.imwrite('/Users/zhangyesheng/Desktop/医学信息学/Project/temp/de_sk_fin'+t+'.jpg',array_no_skull)
    Ima = Image.fromarray(array_no_skull)
    Ima.show() 
    # img = cv2.imread('/Users/zhangyesheng/Desktop/医学信息学/Project/temp/de_sk1.jpg',-1)
    # Mask2 = np.where(img>21,1,0) * 255
    # SE = np.ones([5,5],dtype='bool')
    # Mask2 = OpenSk(SE, Mask2)
    
    # cv2.imwrite('/Users/zhangyesheng/Desktop/医学信息学/Project/temp/mask.jpg',Mask2)
    # Ima = Image.fromarray(Mask2)
    # Ima.show()


