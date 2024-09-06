import cv2
import numpy as np
from PyQt5 import QtCore
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import pyqtgraph as pg
import sys
from process import Process
from webcam import Webcam
from video import Video
from interface import waitKey
class Communicate(QObject):
closeApp = pyqtSignal()
class GUI(QMainWindow, QThread):
def init (self):
super(GUI,self). init ()
self.initUI()
self.webcam = Webcam()
self.video = Video()
self.input = self.webcam
self.dirname = ""
print("Input: webcam")
self.statusBar.showMessage("Input: webcam", 5000)
self.btnOpen.setEnabled(False)
self.process = Process()
self.status = False
self.frame = np.zeros((10,10,3),np.uint8)
self.bpm = 0
def initUI(self):
font = QFont()
font.setPointSize(16)
self.btnStart = QPushButton("Start", self)
self.btnStart.move(440,520)
self.btnStart.setFixedWidth(200)
self.btnStart.setFixedHeight(50)
self.btnStart.setFont(font)
self.btnStart.clicked.connect(self.run)
self.btnOpen = QPushButton("Open", self)
self.btnOpen.move(230,520)
self.btnOpen.setFixedWidth(200)
self.btnOpen.setFixedHeight(50)
self.btnOpen.setFont(font)
self.btnOpen.clicked.connect(self.openFileDialog)
self.cbbInput = QComboBox(self)
self.cbbInput.addItem("Webcam")
self.cbbInput.addItem("Video")
self.cbbInput.setCurrentIndex(0)
self.cbbInput.setFixedWidth(200)
self.cbbInput.setFixedHeight(50)
self.cbbInput.move(20,520)
self.cbbInput.setFont(font)
self.cbbInput.activated.connect(self.selectInput)
self.lblDisplay = QLabel(self)
self.lblDisplay.setGeometry(10,10,640,480)
self.lblDisplay.setStyleSheet("background-color: #000000")
self.lblROI = QLabel(self) #label to show face with ROIs
self.lblROI.setGeometry(660,10,200,200)
self.lblROI.setStyleSheet("background-color: #000000")
self.lblHR = QLabel(self)
self.lblHR.setGeometry(900,20,300,40)
self.lblHR.setFont(font)
self.lblHR.setText("Frequency: ")
self.lblHR2 = QLabel(self)
self.lblHR2.setGeometry(900,70,300,40)
self.lblHR2.setFont(font)
self.lblHR2.setText("Heart Rate: ")
self.signal_Plt = pg.PlotWidget(self)
self.signal_Plt.move(660,220)
self.signal_Plt.resize(480,192)
self.signal_Plt.setLabel('bottom', "Signal")
self.fft_Plt = pg.PlotWidget(self)
self.fft_Plt.move(660,425)
self.fft_Plt.resize(480,192)
self.fft_Plt.setLabel('bottom', "FFT")
self.timer = pg.QtCore.QTimer()
self.timer.timeout.connect(self.update)
self.timer.start(200)
self.statusBar = QStatusBar()
self.statusBar.setFont(font)
self.setStatusBar(self.statusBar)
self.c = Communicate()
self.c.closeApp.connect(self.close)
self.setGeometry(100,100,1160,640)
self.setWindowTitle("Heart Rate Detector")
self.show()
