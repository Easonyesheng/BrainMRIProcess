'''
1 一键去脑壳 -- conditional dilation + '-'
2 信息的显示 -- 




'''
import cv2
import time
import numpy as np 
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import sys
import pydicom
import vtk
from Imread import DicomIn
from PIL import Image,ImageQt
from GMorphology import *
from De_bone import DSK_DI_Morpho
from OTSU_G import OTSU_GET
from ENTRO_G import Entropy_get
from VTK3D import VTK3d


# Operation Window
class BrainProcess(QWidget):
    def __init__(self):
        super(BrainProcess, self).__init__()
        self.SE = np.ones([3,3], dtype='int')
        self.info = {}
        self.path = '/Users/zhangyesheng/Desktop/医学信息学/BrainMRIProcess/temp/'
        

        #Window 1200x1000
        self.resize(1200,1050)
        self.setWindowTitle('BrainMRIProcessing')
        self.setWindowIcon(QIcon('/Users/zhangyesheng/Desktop/Icon.jpg'))

        #label   -- original pic -- LeftUp
        self.label_OriPic = QLabel(self)
        self.label_OriPic.setFixedSize(400,400)
        self.label_OriPic.move(120,50)
        self.label_OriPic.setStyleSheet("QLabel{background:white}" "QLabel{color:rgb(20,20,20);font-size:10px;font-weight:bold;font-family:宋体;}")
        self.label_Oritxt = QLabel(self)
        self.label_Oritxt.move(270,30) #+150,-20
        self.label_Oritxt.setText('Original Picture')

       

        #label -- DeSkull -- RightUp
        self.label_DS = QLabel(self)
        self.label_DS.setFixedSize(400,400)
        self.label_DS.move(540,50)
        self.label_DS.setStyleSheet("QLabel{background:white}" "QLabel{color:rgb(20,20,20);font-size:10px;font-weight:bold;font-family:宋体;}")
        self.label_DStxt = QLabel(self)
        self.label_DStxt.move(690,30)
        self.label_DStxt.setText('Deskull')
        
        #label -- Information -- LeftDown
        '''
        information['PatientID'] 
        information['PatientName']
        information['PatientBirthDate'] 
        information['PatientSex'] 
        information['StudyID'] 
        information['StudyDate'] 
        information['StudyTime'] 
        information['InstitutionName'] 
        information['Manufacturer'] 
        '''
        self.label_PaID = QtWidgets.QLabel(self)
        self.label_PaID.setFixedSize(400,40)
        self.label_PaID.move(120,470)
        self.label_PaID.setStyleSheet("QLabel{background:white}" "QLabel{color:rgb(20,20,20);font-size:15px;font-weight:bold;font-family:Roman times;}")
        self.label_PaID.setAlignment(Qt.AlignHCenter)

        self.label_PaN = QtWidgets.QLabel(self)
        self.label_PaN.setFixedSize(400,40)
        self.label_PaN.move(120,510)
        self.label_PaN.setStyleSheet("QLabel{background:white}" "QLabel{color:rgb(20,20,20);font-size:15px;font-weight:bold;font-family:Roman times;}")
        self.label_PaN.setAlignment(Qt.AlignHCenter)

        self.label_PaBD = QtWidgets.QLabel(self)
        self.label_PaBD.setFixedSize(400,40)
        self.label_PaBD.move(120,550)
        self.label_PaBD.setStyleSheet("QLabel{background:white}" "QLabel{color:rgb(20,20,20);font-size:15px;font-weight:bold;font-family:Roman times;}")
        self.label_PaBD.setAlignment(Qt.AlignHCenter)

        self.label_PaS = QtWidgets.QLabel(self)
        self.label_PaS.setFixedSize(400,40)
        self.label_PaS.move(120,590)
        self.label_PaS.setStyleSheet("QLabel{background:white}" "QLabel{color:rgb(20,20,20);font-size:15px;font-weight:bold;font-family:Roman times;}")
        self.label_PaS.setAlignment(Qt.AlignHCenter)

        self.label_SID = QtWidgets.QLabel(self)
        self.label_SID.setFixedSize(400,40)
        self.label_SID.move(120,630)
        self.label_SID.setStyleSheet("QLabel{background:white}" "QLabel{color:rgb(20,20,20);font-size:15px;font-weight:bold;font-family:Roman times;}")
        self.label_SID.setAlignment(Qt.AlignHCenter)
        
        self.label_SD = QtWidgets.QLabel(self)
        self.label_SD.setFixedSize(400,40)
        self.label_SD.move(120,670)
        self.label_SD.setStyleSheet("QLabel{background:white}" "QLabel{color:rgb(20,20,20);font-size:15px;font-weight:bold;font-family:Roman times;}")
        self.label_SD.setAlignment(Qt.AlignHCenter)

        self.label_ST= QtWidgets.QLabel(self)
        self.label_ST.setFixedSize(400,40)
        self.label_ST.move(120,710)
        self.label_ST.setStyleSheet("QLabel{background:white}" "QLabel{color:rgb(20,20,20);font-size:15px;font-weight:bold;font-family:Roman times;}")
        self.label_ST.setAlignment(Qt.AlignHCenter)


        self.label_IN = QtWidgets.QLabel(self)
        self.label_IN.setFixedSize(400,40)
        self.label_IN.move(120,750)
        self.label_IN.setStyleSheet("QLabel{background:white}" "QLabel{color:rgb(20,20,20);font-size:15px;font-weight:bold;font-family:Roman times;}")
        self.label_IN.setAlignment(Qt.AlignHCenter)

        self.label_M = QtWidgets.QLabel(self)
        self.label_M.setFixedSize(400,40)
        self.label_M.move(120,790)
        self.label_M.setStyleSheet("QLabel{background:white}" "QLabel{color:rgb(20,20,20);font-size:15px;font-weight:bold;font-family:Roman times;}")
        self.label_M.setAlignment(Qt.AlignHCenter)
        
        
        #label -- Segmentation -- RightDown
        self.count = 0
        self.label_S = QLabel(self)
        self.label_S.setFixedSize(400,400)
        self.label_S.move(540,470)
        self.label_S.setStyleSheet("QLabel{background:white}" "QLabel{color:rgb(20,20,20);font-size:10px;font-weight:bold;font-family:宋体;}")
        self.label_Stxt = QLabel(self)
        self.label_Stxt.move(690,450)
        self.label_Stxt.setText('Segmentation')

        
        
        #------------------------------------------------------button
        #button -- imread
        btn_ir = QPushButton(self)
        btn_ir.setText('Open Image')
        btn_ir.move(0,45)
        btn_ir.clicked.connect(self.openimage)

        #button -- quit
        btn_q = QPushButton(self)
        btn_q.setText('Quit')
        btn_q.move(1000,45)
        btn_q.clicked.connect(QCoreApplication.instance().quit)

        #button -- DeSkull
        btn_DS = QPushButton(self)
        btn_DS.setText('DeSkull')
        btn_DS.move(1000,75)
        btn_DS.clicked.connect(self.DeSkullWin)

        #button -- Segmentation -- OTSU_Mod
        btn_OS = QPushButton(self)
        btn_OS.setText('OTSU')
        btn_OS.move(1000,500)
        btn_OS.clicked.connect(self.OTSUSeg)

        #button -- Segmentation -- Entropy_Mod
        btn_ES = QPushButton(self)
        btn_ES.setText('Entropy')
        btn_ES.move(1000,530)
        btn_ES.clicked.connect(self.EntroSeg)

        #button -- VTK -- 3D Reconstruction
        btn_vtk = QPushButton(self)
        btn_vtk.setText("3DRec")
        btn_vtk.move(1000,560)
        btn_vtk.clicked.connect(self.TDRec)


    #------------------------------------------------------function
    # open image button-pushed event
    def openimage(self):
        imgName, imgType = QFileDialog.getOpenFileName(self,"Open Image","","All Files(*)")
        self.name = imgName.split('.')[0][-1]
        self.info, imgArray = DicomIn(imgName)
        self.array = imgArray
        imgArray = (imgArray/imgArray.max())*255
        img = Image.fromarray(imgArray)
        img = img.convert('L') #  -- https://blog.csdn.net/chris_pei/article/details/78261922
        img.save(self.path+'ori.jpg')
        #show Img
        imshow = cv2.imread(self.path+'ori.jpg',0)
        self.img = imshow # ori image
        QApplication.processEvents()
        height, width = imshow.shape
        bytesPerLine = width
        QImg_Gray = QImage(imshow.data, width, height, bytesPerLine, QImage.Format_Grayscale8)
        pixmap_Gray = QPixmap.fromImage(QImg_Gray)
        pixmap_Gray = pixmap_Gray.scaled(self.label_OriPic.width(),self.label_OriPic.height())
        self.label_OriPic.setPixmap(pixmap_Gray)
        # show information
        '''
        information['PatientID'] 
        information['PatientName']
        information['PatientBirthDate'] 
        information['PatientSex'] 
        information['StudyID'] 
        information['StudyDate'] 
        information['StudyTime'] 
        information['InstitutionName'] 
        information['Manufacturer'] 
        '''
        self.label_PaID.setText('PatientID: '+self.info['PatientID'])
        self.label_PaN.setText('PatientName: '+str(self.info['PatientName']))
        self.label_PaBD.setText('PatientBirthDate: '+self.info['PatientBirthDate'])
        self.label_PaS.setText('PatientSex: '+self.info['PatientSex'])
        self.label_SID.setText('StudyID: '+self.info['StudyID'])
        self.label_SD.setText('StudyDate: '+self.info['StudyDate'])
        self.label_ST.setText('StudyTime: '+self.info['StudyTime'])
        self.label_IN.setText('InstitutionName: '+self.info['InstitutionName'])
        self.label_M.setText('Manufacturer: '+self.info['Manufacturer'])

    # get rid of the skull and show on the QT
    def DeSkullWin(self):
        # t = str(time.time())[-1]
        t = self.name
        '''
        self.imshow -- image without skull 
        '''
        self.imshow = cv2.imread(self.path+'de_sk_fin'+t+'.jpg',-1) 
        try:
            height, width = self.imshow.shape
        except AttributeError:
            img_R = DSK_DI_Morpho(self.array)
            cv2.imwrite(self.path+'de_sk_fin'+t+'.jpg',img_R)
            self.imshow = cv2.imread(self.path+'de_sk_fin'+t+'.jpg',-1)
            height, width = self.imshow.shape
        QApplication.processEvents()
        bytesPerLine = width
        QImg_Gray = QImage(self.imshow.data, width, height,bytesPerLine, QImage.Format_Grayscale8)
        pixmap_Gray = QPixmap.fromImage(QImg_Gray)
        pixmap_Gray = pixmap_Gray.scaled(self.label_DS.width(),self.label_DS.height())
        self.label_DS.setPixmap(pixmap_Gray)
        self.label_DStxt.setText('De_skull')




    # Use modified OTSU
    def OTSUSeg(self):
        T = OTSU_GET(self.imshow)
        # print(T)
        T_,imgd = cv2.threshold(self.imshow, T, 255, cv2.THRESH_BINARY)

        # imgd is a binary image
        QApplication.processEvents()
        height, width = imgd.shape
        bytesPerLine = width
        QImg_Gray = QImage(imgd.data, width, height, bytesPerLine, QImage.Format_Grayscale8)
        pixmap_Gray = QPixmap.fromImage(QImg_Gray)
        pixmap_Gray = pixmap_Gray.scaled(self.label_OriPic.width(),self.label_OriPic.height())
        
        self.label_S.setPixmap(pixmap_Gray)


    # Use modified Entropy
    def EntroSeg(self):
        T = Entropy_get(self.imshow)
        # print(T)
        T_,imgd = cv2.threshold(self.imshow, T, 255, cv2.THRESH_BINARY)

        # imgd is a binary image
        QApplication.processEvents()
        height, width = imgd.shape
        bytesPerLine = width
        QImg_Gray = QImage(imgd.data, width, height, bytesPerLine, QImage.Format_Grayscale8)
        pixmap_Gray = QPixmap.fromImage(QImg_Gray)
        pixmap_Gray = pixmap_Gray.scaled(self.label_OriPic.width(),self.label_OriPic.height())
        
        self.label_S.setPixmap(pixmap_Gray)

    def TDRec(self):
        VTK3d()




if __name__ == "__main__":
    #QtCore.QCoreApplication.setLibraryPaths("")
    app = QtWidgets.QApplication(sys.argv)
    my = BrainProcess()
    my.show()
    
    
    sys.exit(app.exec_())