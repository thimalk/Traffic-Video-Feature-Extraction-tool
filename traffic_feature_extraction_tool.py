#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
ZetCode PyQt4 tutorial 

In this example, we create a bit
more complicated window layout using
the QtGui.QGridLayout manager. 

author: Jan Bodnar
website: zetcode.com 
last edited: October 2011
"""

import sys
from PyQt4 import QtGui, QtCore

import numpy as np
import pandas as pd
import cv2
import glob
import ntpath
import os.path

np.set_printoptions(threshold='nan')

# method to extract motion feature
def motionFeatureExtractionStart(folder,outfolder,f_type):
    if f_type ==0:
		outname = 'motion_frame_Difference'
    else:
		outname = 'motion_background_subtraction'
    max_val=0
    L = []
    arrayFiles = glob.glob(folder+"/*.avi")
    for name in arrayFiles:
            fname=os.path.splitext(ntpath.basename(name))[0]
            print "start ", name
            cap = cv2.VideoCapture(name)
            
            frameCount=cap.get(cv2.cv.CV_CAP_PROP_FRAME_COUNT)
            
            ret, frame = cap.read()
            #lower_reso = cv2.pyrDown(cv2.pyrDown(cv2.pyrDown(cv2.pyrDown(frame))))
            TMM = np.zeros((frame.shape[0],frame.shape[1]))
            rowVal=frame.shape[0]/2
            
            ret, frame = cap.read()
            ret = True
            
            if f_type == 1:
                #background subtract method
                fgbg = cv2.BackgroundSubtractorMOG()
            else:
                #frame difference method
                back=frame
            while(cap.isOpened() and ret):
                ret, frame = cap.read()
                if ret:
#                     frame=cv2.GaussianBlur(frame,(7,7),0)
                    #lower_reso = cv2.pyrDown(cv2.pyrDown(cv2.pyrDown(cv2.pyrDown(frame))))
                    if f_type == 1:
                        #background subtract method
                        fgmask = fgbg.apply(frame)
                    else:
                    
                        #frame difference method
                        fgmask1 =cv2.absdiff(frame,back)
                        fgmask2= cv2.cvtColor(fgmask1, cv2.COLOR_BGR2GRAY)
                        fgmask=cv2.GaussianBlur(fgmask2,(7,7),0)
                        (th,fgmask)=cv2.threshold(fgmask,20,255,cv2.THRESH_BINARY)
    #                     fgmask=cv2.GaussianBlur(fgmask2,(7,7),0)

                        back=frame
                    
                    fgmask = fgmask/255.0
                    TMM=TMM+fgmask
                    
            TMM=TMM/frameCount
            #TMM=cv2.pyrDown(TMM)
            #get the sum of all the rows and create a single row
            lower_reso = cv2.pyrDown(cv2.pyrDown(cv2.pyrDown(TMM)))        
            
            
            Res = np.sum(lower_reso, axis=0)
            
            #get the middle row as the input vector
            #Res = TMM[rowVal]
        
            print lower_reso.shape
            #print "row value",rowVal
            #Res1 = np.sum(TMM, axis=1)
            # Res1=Res1*1.0/np.max(Res1)
#             if np.max(Res) !=0.0:
#                 Res=Res*1.0/np.max(Res)
            temp=np.max(Res)
            if temp>max_val:
                max_val=temp
            l = [fname]
            l=l+Res.tolist()
            #l=l+Res1.tolist()
            print "length ", Res.shape[0]
            L.append(l)  
            print "complete ", name
    # write to file
    #L = np.array(L)
    l=["max value="+str(max_val)]
    L.append(l)
    d = pd.DataFrame(data=L)
    d.to_csv(outfolder+'/'+outname + '.txt', index=False, header=False)  
    print "max value=",max_val
    print "***********complete all*************"
    #T = set([l.shape for l in L])

# method to extract texture feature
def textureFeatureStart(folder,outfolder,f_type):

    if f_type ==0:
    	outname = 'texture_frame_Difference'
    else:
    	outname = 'texture_background_subtraction'
    
    L = []
    arrayFiles = glob.glob(folder+"/*.avi")
    for name in arrayFiles:
            fname=os.path.splitext(ntpath.basename(name))[0]
            print "start ", name
            cap = cv2.VideoCapture(name)
            
            frameCount=cap.get(cv2.cv.CV_CAP_PROP_FRAME_COUNT)
            
            ret, frame = cap.read()
            #lower_reso = cv2.pyrDown(cv2.pyrDown(cv2.pyrDown(cv2.pyrDown(frame))))
            TMM = np.zeros((frame.shape[0],frame.shape[1]))
            rowVal=frame.shape[0]/2
            
            ret, frame = cap.read()
            ret = True
            
            if f_type == 1:
        
                #background subtract method
                fgbg = cv2.BackgroundSubtractorMOG()
            else:
                #frame difference method
                back=frame
            while(cap.isOpened() and ret):
                ret, frame = cap.read()
                if ret:
#                     frame=cv2.GaussianBlur(frame,(7,7),0)
                    #lower_reso = cv2.pyrDown(cv2.pyrDown(cv2.pyrDown(cv2.pyrDown(frame))))
                    if f_type == 1:
                        #background subtract method
                        fgmask = fgbg.apply(frame)
                    else:
                        #frame difference method
                        fgmask1 =cv2.absdiff(frame,back)
                        fgmask2= cv2.cvtColor(fgmask1, cv2.COLOR_BGR2GRAY)
                        fgmask = cv2.Canny(fgmask2,100,200)
    #                     fgmask=cv2.GaussianBlur(fgmask2,(7,7),0)

                        back=frame
                    
                    fgmask = fgmask/255.0
                    TMM=TMM+fgmask
                    
            TMM=TMM/frameCount
            #TMM=cv2.pyrDown(TMM)
            #get the sum of all the rows and create a single row
            lower_reso = cv2.pyrDown(cv2.pyrDown(TMM))        
            
            
            Res = np.sum(lower_reso, axis=0)
            
            #get the middle row as the input vector
            #Res = TMM[rowVal]
        
            print lower_reso.shape
            #print "row value",rowVal
            #Res1 = np.sum(TMM, axis=1)
            # Res1=Res1*1.0/np.max(Res1)
#             if np.max(Res) !=0.0:
#                 Res=Res*1.0/np.max(Res)
            print np.max(Res)
            l = [fname]
            l=l+Res.tolist()
            #l=l+Res1.tolist()
            print "length ", Res.shape[0]
            L.append(l)  
            print "complete ", name
    # write to file
    #L = np.array(L)
    d = pd.DataFrame(data=L)
    d.to_csv(outfolder+'/'+outname + '.txt', index=False, header=False)  
    print "***********complete all*************"
    #T = set([l.shape for l in L])





class Example(QtGui.QWidget):

	def __init__(self):
		super(Example, self).__init__()
		
		self.initUI()

        
	def initUI(self):
        
		inputFileL= QtGui.QLabel('Input Video Folder')
		outputFileL = QtGui.QLabel('Output Folder')
		foergroundExtractionL = QtGui.QLabel('Foerground Extraction Method ')
		featureTypeL = QtGui.QLabel('Feature Type ')


		
		
		self.inputFile = QtGui.QLineEdit()
		self.outputFile = QtGui.QLineEdit()
		
		self.foergroundExtraction =  QtGui.QComboBox(self)
		self.foergroundExtraction.addItem("Frame Difference")
		self.foergroundExtraction.addItem("Background Subtraction")
		
		self.featureType =  QtGui.QComboBox(self)
		self.featureType.addItem("Motion")
		self.featureType.addItem("Texture (edge)")
		
		
		self.inputSelectButton = QtGui.QPushButton('Browse')
		self.outputSelectButton = QtGui.QPushButton('Broswe')
		
		
		
		grid = QtGui.QGridLayout()
		grid.setSpacing(10)
		
		

		grid.addWidget(inputFileL, 1, 0)
		grid.addWidget(self.inputFile, 1, 1)
		grid.addWidget(self.inputSelectButton, 1, 2)

		self.inputSelectButton.clicked.connect(self.selectInputFile) 
		
		grid.addWidget(outputFileL, 2, 0)
		grid.addWidget(self.outputFile, 2, 1)
		grid.addWidget(self.outputSelectButton,2,2)
		
		grid.addWidget(foergroundExtractionL, 3, 0)
		grid.addWidget(self.foergroundExtraction, 3, 1)
		
		grid.addWidget(featureTypeL, 4, 0)
		grid.addWidget(self.featureType, 4, 1)
		
		self.outputSelectButton.clicked.connect(self.selectOutputFile) 
		

		button = QtGui.QPushButton('Execute')
		grid.addWidget(button,5,0)
		button.clicked.connect(self.execute) 
        
		self.setLayout(grid) 
        
		self.setGeometry(300, 300, 350, 300)
		self.setWindowTitle('Video Feature Extraction: Frame Difference')    
		self.show()
        
	def execute(self):
        
		sender = self.sender()
		inputF = str(self.inputFile.text())
		outputF = str(self.outputFile.text())
		f_type = str(self.foergroundExtraction.currentIndex())
		feature_t = str(self.featureType.currentIndex())
		
		if feature_t == 0:
			motionFeatureExtractionStart(inputF,outputF,f_type)
		else :
			textureFeatureStart(inputF,outputF,f_type)
		
	def selectInputFile(self):
        
		self.inputFile.setText(QtGui.QFileDialog.getExistingDirectory(self, "Select Directory"))
		print self.inputFile.text()
		
	def selectOutputFile(self):
        
		self.outputFile.setText(QtGui.QFileDialog.getExistingDirectory(self, "Select Directory"))
		print self.outputFile.text()
	def normalOutputWritten(self, text):
		"""Append text to the QTextEdit."""
		# Maybe QTextEdit.append() works as well, but this is how I do it:
		cursor = self.textEdit.textCursor()
		cursor.movePosition(QtGui.QTextCursor.End)
		cursor.insertText(text)
		self.textEdit.setTextCursor(cursor)
		self.textEdit.ensureCursorVisible()
        
def main():
    
	app = QtGui.QApplication(sys.argv)
	ex = Example()
	sys.exit(app.exec_())


if __name__ == '__main__':
	main()
