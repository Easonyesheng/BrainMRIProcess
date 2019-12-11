'''
Dicom input & convert to img
'''

import pydicom
import matplotlib.pyplot as plt 
from PIL import Image, ImageQt


'''
input : DICOM 
output : information & pixel array
'''
def DicomIn(filename):
    di = pydicom.dcmread(filename)
    ds = pydicom.read_file(filename)
    information = {}
    information['PatientID'] = ds.PatientID
    information['PatientName'] = ds.PatientName
    information['PatientBirthDate'] = ds.PatientBirthDate
    information['PatientSex'] = ds.PatientSex
    information['StudyID'] = ds.StudyID
    information['StudyDate'] = ds.StudyDate
    information['StudyTime'] = ds.StudyTime
    information['InstitutionName'] = ds.InstitutionName
    information['Manufacturer'] = ds.Manufacturer
    img = ds.pixel_array
    # print('imgtype:',type(img))
    # print('shape: ',img.shape)
    return information, img



if __name__ == "__main__":
    filename = '/Users/zhangyesheng/Desktop/医学信息学/Project/Dicom/Z_IM7'
    info, img = DicomIn(filename)
    Ima = Image.fromarray(img)
    Ima.show()
    
    # for key in info.keys():
    #     print(key,' : ',info[key])
