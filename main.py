from PyQt5 import QtCore, QtGui, QtWidgets
from pyqtgraph import PlotWidget
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox
import pandas as pd
import numpy as np
from scipy.fft import fftshift
from scipy import signal
import matplotlib.pyplot as plt
from scipy.io import loadmat
from fpdf import FPDF
import os
from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg
import pyqtgraph.exporters


class Ui_MainWindow(object):
    
    #dictinary stores files with its format
    filenames = dict()
    #dictinary stores files with its graph widget
    Current_File = dict()
    #a list of images of the graphs (use for create_pdf)
    image_list = []
    #a list of images of the spectrograms (use for create_pdf)
    spectroImg_list = [None,None,None]
    #flags for pause and stop functions
    isPaused = False
    isStoped = False
    #the length of data on a file
    dataLength = 0
    #pens colors for the graph
    pen1 = [255,0,0]
    pen2 = [0,255,0]
    pen3 = [0,0,255]
    # a list for pens to used in plot function
    pens = [pen1, pen2, pen3]
    #stores number of the selected widget
    current_widget = int
    #intial graph range 
    graph_rangeMin = [0,0,0]
    graph_rangeMax = [1000,1000,1000]
    
    def setupUi(self, MainWindow):
        
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(696, 704)
        """ MainWindow.setWindowTitle("Signal Viewer")
        MainWindow.setWindowIcon("images/window") """
        self.centralwidget = QtWidgets.QWidget(MainWindow) 
        self.centralwidget.setObjectName("centralwidget")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(10, 0, 28, 28))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.setIcon(QtGui.QIcon("images/browse.png"))
        self.pushButton.setIconSize(QtCore.QSize(28,28))
        self.pushButton.setToolTip("open new signal file")
        
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(50, 0, 28, 28))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.setIcon(QtGui.QIcon("images/x axis.png"))
        self.pushButton_2.setIconSize(QtCore.QSize(28,28))
        self.pushButton_2.setToolTip("move the signal in x-axis")
        
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(90, 0, 28, 28))
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_3.setIcon(QtGui.QIcon("images/y axis.png"))
        self.pushButton_3.setIconSize(QtCore.QSize(28,28))
        self.pushButton_3.setToolTip("move the signal in y-axis")
        
        self.pushButton_4 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_4.setGeometry(QtCore.QRect(130, 0, 28, 28))
        self.pushButton_4.setObjectName("pushButton_4")
        self.pushButton_4.setIcon(QtGui.QIcon("images/move.png"))
        self.pushButton_4.setIconSize(QtCore.QSize(28,28))
        self.pushButton_4.setToolTip("move the signal in both directions")
        
        self.pushButton_5 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_5.setGeometry(QtCore.QRect(170, 0, 28,28))
        self.pushButton_5.setObjectName("pushButton_5")
        self.pushButton_5.setIcon(QtGui.QIcon("images/save.jpg"))
        self.pushButton_5.setIconSize(QtCore.QSize(28,28))
        self.pushButton_5.setToolTip("save the signal graph")
        
        self.pushButton_6 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_6.setGeometry(QtCore.QRect(210, 0, 28, 28))
        self.pushButton_6.setObjectName("pushButton_6")
        self.pushButton_6.setIcon(QtGui.QIcon("images/clear.png"))
        self.pushButton_6.setIconSize(QtCore.QSize(28,28))
        self.pushButton_6.setToolTip("clear the signal")
    
        self.pushButton_7 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_7.setGeometry(QtCore.QRect(250, 0, 28, 28))
        self.pushButton_7.setObjectName("pushButton_7")
        self.pushButton_7.setIcon(QtGui.QIcon("images/play.png"))
        self.pushButton_7.setIconSize(QtCore.QSize(28,28))
        self.pushButton_7.setToolTip("play the signal")

        self.pushButton_8 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_8.setGeometry(QtCore.QRect(290, 0, 28, 28))
        self.pushButton_8.setObjectName("pushButton_8")
        self.pushButton_8.setIcon(QtGui.QIcon("images/pause.png"))
        self.pushButton_8.setIconSize(QtCore.QSize(28,28))
        self.pushButton_8.setToolTip("pause the signal")
        
        self.pushButton_9 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_9.setGeometry(QtCore.QRect(330, 0, 28, 28))
        self.pushButton_9.setObjectName("pushButton_9")
        self.pushButton_9.setIcon(QtGui.QIcon("images/stop.png"))
        self.pushButton_9.setIconSize(QtCore.QSize(28,28))
        self.pushButton_9.setToolTip("restart the signal")
        
        self.pushButton_10 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_10.setGeometry(QtCore.QRect(370, 0, 28, 28))
        self.pushButton_10.setObjectName("pushButton_10")
        self.pushButton_10.setIconSize(QtCore.QSize(28,28))
        self.pushButton_10.setToolTip("Zoom In")
        
        self.pushButton_11 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_11.setGeometry(QtCore.QRect(410, 0, 28, 28))
        self.pushButton_11.setObjectName("pushButton_11")
        self.pushButton_11.setIconSize(QtCore.QSize(28,28))
        self.pushButton_11.setToolTip("Zoom Out")
        
        self.pushButton_12 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_12.setGeometry(QtCore.QRect(540, 0, 28, 28))
        self.pushButton_12.setObjectName("pushButton_12")
        self.pushButton_12.setIconSize(QtCore.QSize(28,28))
        self.pushButton_12.setToolTip("Move Right")
        
        self.pushButton_13 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_13.setGeometry(QtCore.QRect(590, 0, 28, 28))
        self.pushButton_13.setObjectName("pushButton_13")
        self.pushButton_13.setIconSize(QtCore.QSize(28,28))
        self.pushButton_13.setToolTip("Move Left")

        """ self.pushButton_10 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_10.setGeometry(QtCore.QRect(460, 0, 75, 23))
        self.pushButton_10.setObjectName("pushButton_9") """

        self.comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox.setGeometry(QtCore.QRect(460, 0, 70, 28))
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.graphicsView = pg.PlotWidget(self.centralwidget)
        self.graphicsView.setGeometry(QtCore.QRect(10, 40, 591, 192))
        self.graphicsView.setObjectName("graphicsView")
        self.graphicsView_2 = pg.PlotWidget(self.centralwidget)
        self.graphicsView_2.setGeometry(QtCore.QRect(10, 260, 591, 192))
        self.graphicsView_2.setObjectName("graphicsView_2")
        self.graphicsView_3 = pg.PlotWidget(self.centralwidget)
        self.graphicsView_3.setGeometry(QtCore.QRect(10, 480, 591, 192))
        self.graphicsView_3.setObjectName("graphicsView_3")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 696, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        #connecting each button by its function
        self.pushButton.clicked.connect(self.load_file)
        self.pushButton_2.clicked.connect(self.only_x)
        self.pushButton_3.clicked.connect(self.only_y)
        self.pushButton_4.clicked.connect(self.zoom)
        self.pushButton_5.clicked.connect(self.export)
        self.pushButton_6.clicked.connect(self.clear)
        self.pushButton_7.clicked.connect(self.start)
        self.pushButton_8.clicked.connect(self.pause)
        self.pushButton_9.clicked.connect(self.stop)
        self.pushButton_10.clicked.connect(self.zoom_in)
        self.pushButton_11.clicked.connect(self.zoom_out)
        self.pushButton_12.clicked.connect(self.move_right)
        self.pushButton_13.clicked.connect(self.move_left)
        
        self.widget1 = self.graphicsView
        self.widget2 = self.graphicsView_2
        self.widget3 = self.graphicsView_3
        #a list of widgets on the program used in selecting a widget
        self.widgets = [self.widget1,self.widget2,self.widget3]
        
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton.setText(_translate("MainWindow", ""))
        self.pushButton.setShortcut(_translate("MainWindow", "Ctrl+L"))
        self.pushButton_2.setText(_translate("MainWindow", ""))
        self.pushButton_2.setShortcut(_translate("MainWindow", "Ctrl+X"))
        self.pushButton_3.setText(_translate("MainWindow", ""))
        self.pushButton_3.setShortcut(_translate("MainWindow", "Ctrl+Y"))
        self.pushButton_4.setText(_translate("MainWindow", ""))
        self.pushButton_4.setShortcut(_translate("MainWindow", "Ctrl+M"))
        self.pushButton_5.setText(_translate("MainWindow", ""))
        self.pushButton_5.setShortcut(_translate("MainWindow", "Ctrl+S"))
        self.pushButton_6.setText(_translate("MainWindow", ""))
        self.pushButton_6.setShortcut(_translate("MainWindow", "Ctrl+Shift+D"))
        self.pushButton_7.setText(_translate("MainWindow", ""))
        self.pushButton_7.setShortcut(_translate("MainWindow", "Ctrl+P"))
        self.pushButton_8.setText(_translate("MainWindow", ""))
        self.pushButton_8.setShortcut(_translate("MainWindow", "Ctrl+Shift+P"))
        self.pushButton_9.setText(_translate("MainWindow", ""))
        self.pushButton_9.setShortcut(_translate("MainWindow", "Ctrl+Shift+S"))
        self.pushButton_10.setText(_translate("MainWindow", "+"))
        self.pushButton_10.setShortcut(_translate("MainWindow", "Up"))
        self.pushButton_11.setText(_translate("MainWindow", "-"))
        self.pushButton_11.setShortcut(_translate("MainWindow", "Down"))
        self.pushButton_12.setText(_translate("MainWindow", "R"))
        self.pushButton_12.setShortcut(_translate("MainWindow", "Right"))
        self.pushButton_13.setText(_translate("MainWindow", "L"))
        self.pushButton_13.setShortcut(_translate("MainWindow", "Left"))
        self.comboBox.setItemText(0, _translate("MainWindow", "Widget1"))
        self.comboBox.setItemText(1, _translate("MainWindow", "Widget2"))
        self.comboBox.setItemText(2, _translate("MainWindow", "Widget3"))
    
    def load_file(self):
        #a function that loads the files data
        
        self.check_widget()
        self.filename, self.format = QtWidgets.QFileDialog.getOpenFileName(None, "Load Signal File", "", "*.csv;;" " *.txt;;" "*.mat")
        #checks if no file selected
        if self.filename == "":
            pass
        else:
            #checks if the file already existed in another widget
            if self.filename in self.filenames:
                self.show_popup("File Already Existed", "This file already uploaded before")
            else:
                #load the file for the first time
                self.clear()
                
                self.filenames[self.filename] = self.format
                self.Current_File[self.current_widget] = self.filename
                
                self.checkFileEXT(self.filenames)
    
    def checkFileEXT(self, file):
        #a function that checks file extintions 
        
        for i in file.items():
            if i[1] == "*.csv":
                csv_file = pd.read_csv(i[0]).iloc[:,1]
                #saves data length of the file
                self.widgets[self.current_widget].dataLength = csv_file.__len__()
                
                self.plot_here(csv_file, i[0])
                self.plot_spectro(csv_file)
                
            elif i[1] == "*.txt":
                txt_file = pd.read_csv(i[0]).iloc[:,2]
                #saves data length of the file
                self.widgets[self.current_widget].dataLength = txt_file.__len__()
                
                self.plot_here(txt_file, i[0])
                self.plot_spectro(txt_file)
            
            elif i[1] == "*.mat":
                mat = loadmat(i[0])
                mat_file = pd.DataFrame(mat["F"]).iloc[:,1]
                #saves data length of the file
                self.widgets[self.current_widget].dataLength = mat_file.__len__()
                
                self.plot_here(mat_file, i[0])
                self.plot_spectro(mat_file)

    def clear(self):
        #a functions that clears a graph and delete its file
        
        self.check_widget()
        self.widgets[self.current_widget].clear()
        self.stop()
        self.widgets[self.current_widget].plotItem.showGrid(False,False)
        
        if self.current_widget in self.Current_File:
            #delete the file from filenames dict and current_file dict
            del self.filenames[self.Current_File[self.current_widget]]
            del self.Current_File[self.current_widget]
            
    def only_y(self):
        # only move and zoom in y-axis
        self.check_widget()
        self.widgets[self.current_widget].plotItem.setMouseEnabled(x=False,y=True)
    
    def only_x(self):
        # only move and zoom in x-axis
        self.check_widget()
        self.widgets[self.current_widget].plotItem.setMouseEnabled(y=False,x=True)
    
    def zoom(self):
        #u can zoom and move in any direction
        self.check_widget()
        self.widgets[self.current_widget].plotItem.setMouseEnabled(y=True,x=True)
    
    def export(self):
        #a function that creates a pictures of the drawn graphs
        
        exporter1 = pg.exporters.ImageExporter(self.graphicsView.plotItem)
        exporter1.export('fileName1.png')
        exporter2 = pg.exporters.ImageExporter(self.graphicsView_2.plotItem)
        exporter2.export('fileName2.png')
        exporter3 = pg.exporters.ImageExporter(self.graphicsView_3.plotItem)
        exporter3.export('fileName3.png')
        
        #stores the pictures files in image list
        self.image_list = ['fileName1.png','fileName2.png','fileName3.png']
        
        self.create_pdf()
        
    
    def check_widget(self):
        #a function checks the selected widget
        
        if self.comboBox.currentText() == "Widget1":
            self.current_widget = 0
            
        elif self.comboBox.currentText() == "Widget2":
            self.current_widget = 1
            
        elif self.comboBox.currentText() == "Widget3":
            self.current_widget = 2
    
    def plot_here (self, file, fileName):
        # the function that plot the graphs on the selected widget
        
        self.check_widget()
        self.widgets[self.current_widget].clear()
        name = fileName.split("/")[-1]
        self.widgets[self.current_widget].plotItem.setTitle("Channel " + str(self.current_widget + 1))
        self.widgets[self.current_widget].plotItem.addLegend(size=(2, 3))
        self.widgets[self.current_widget].plotItem.showGrid(True, True, alpha=1)
        self.widgets[self.current_widget].setXRange(0, 1000)
        self.widgets[self.current_widget].plotItem.setLabel("bottom", text="Time (ms)")
        self.widgets[self.current_widget].plot(file, name=name, pen = self.pens[self.current_widget])            

    def plot_spectro(self,file):
        # the function that plot spectrogram of the selected signal

        self.check_widget
        plt.specgram(file,Fs=10e3)
        plt.xlabel('Time')
        plt.ylabel('Frequency')
        plt.savefig('spectro'+str(self.current_widget + 1)+'.png')
        self.spectroImg_list[self.current_widget] = 'spectro'+str(self.current_widget + 1)+'.png'
        plt.show()
        
        print("spectro")

    def start(self):
        # the function that makes the graph starts to move
        
        self.check_widget()
        self.isPaused = False
        self.isStoped = False
        data_length = self.widgets[self.current_widget].dataLength
        
        for x in range(data_length):
            #increasing the x-axis range by x
            self.widgets[self.current_widget].setXRange(self.graph_rangeMin[self.current_widget] + x, self.graph_rangeMax[self.current_widget] + x)
            QtWidgets.QApplication.processEvents()

            if self.isPaused == True:
                #saving the new x-axis ranges
                self.graph_rangeMin[self.current_widget] = self.graph_rangeMin[self.current_widget] + x
                self.graph_rangeMax[self.current_widget] = self.graph_rangeMax[self.current_widget] + x
                break
            if self.isStoped == True:
                break

    def pause(self):
        self.check_widget()
        self.isPaused = True

    def stop(self):
        #the function that stops the graph
        
        self.check_widget()
        self.isStoped = True
        # reset the graph ranges
        self.widgets[self.current_widget].setXRange(0, 1000)
        self.graph_rangeMin[self.current_widget] = 0
        self.graph_rangeMax[self.current_widget] = 1000
        
    def create_pdf(self):
        #the function that creates the pdf report
        
        pdf = FPDF()
        
        for x in range(3):
            # set pdf title
            pdf.add_page()
            pdf.set_font('Arial', 'B', 15)
            pdf.cell(70)
            pdf.cell(60, 10, 'Siganl Viewer Report', 1, 0, 'C')
            pdf.ln(20)
            
            # put the graphs on the pdf
            pdf.image(self.image_list[x], 10, 50, 190, 50)
            pdf.image(self.spectroImg_list[x], 10, 110, 190, 100)
            
        pdf.output("report.pdf", "F")    
        
        #removes the graphs pictures as we dont need
        os.remove("fileName1.png")
        os.remove("fileName2.png")
        os.remove("fileName3.png")
        os.remove("spectro1.png")
        os.remove("spectro2.png")
        os.remove("spectro3.png")
    
    def zoom_in(self):
        self.check_widget
        self.widgets[self.current_widget].plotItem.getViewBox().scaleBy(x = 0.5, y = 1)
        
    def zoom_out(self):
        self.check_widget
        self.widgets[self.current_widget].plotItem.getViewBox().scaleBy(x = 2, y = 1)
    
    def move_right(self):
        self.check_widget
        self.widgets[self.current_widget].setXRange(self.graph_rangeMin[self.current_widget] + 100, self.graph_rangeMax[self.current_widget] + 100)

        self.graph_rangeMin[self.current_widget] = self.graph_rangeMin[self.current_widget] + 100
        self.graph_rangeMax[self.current_widget] = self.graph_rangeMax[self.current_widget] + 100
    
    def move_left(self):
        self.check_widget
        self.widgets[self.current_widget].setXRange(self.graph_rangeMin[self.current_widget] - 100, self.graph_rangeMax[self.current_widget] - 100)

        self.graph_rangeMin[self.current_widget] = self.graph_rangeMin[self.current_widget] - 100
        self.graph_rangeMax[self.current_widget] = self.graph_rangeMax[self.current_widget] - 100
        
    def show_popup(self, message, information):
        msg = QMessageBox()
        msg.setWindowTitle("Message")
        msg.setText(message)
        msg.setIcon(QMessageBox.Warning)
        msg.setStandardButtons(QMessageBox.Ok)
        msg.setDefaultButton(QMessageBox.Ok)
        msg.setInformativeText(information)
        x = msg.exec_()
        

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
