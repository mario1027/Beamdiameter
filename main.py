import sys
import os


try:
    from pyueye import ueye
except:
    None

from modules import *
from widgets import *


import numpy as np
import cv2
import pyqtgraph as pg
from liblaser.mein_laser_class import *
from camera import CameraDummy,UeyeCamera
os.environ["QT_FONT_DPI"] = "96" # FIX Problem for High DPI and Scale above 100%




class VideoThread(QThread):
    change_pixmap_signal = Signal(np.ndarray)
    run_flag = True
   

    pixel_size=5
    paused = False
   
    def __init__(self):
        super().__init__()
        
        self._run_flag = True
        self.filter=0.05
        self.pixel_size=5.2
        self.paused = False
        self.typecamera="Ueye"
        if self.typecamera=="Ueye":
            self.camera=UeyeCamera(0)
            x,y,width,height=self.camera.get_aoi()
            self.camera.init(x=x, y=y ,width = width, height = height,
	         exposure = 30)

        else:    
            self.camera=CameraDummy("laser-bajo-costo-intermitencia.mp4")
            self.camera.run()

        

        if self.typecamera=="Ueye": 
            gray=np.copy(self.camera.capture())
            
            self.LaserAnalyzer=LaserAnalyzer(gray , self.pixel_size, units='μm', background_fraction=self.filter,crop=False)
        else:
            
        
            gray=self.camera.frame
        
            self.LaserAnalyzer=LaserAnalyzer(gray , self.pixel_size, units='μm', background_fraction=self.filter,crop=False)

        #self.LaserAnalyzer.calibrate_LaserData_backgraund_noise()
        self.filter=self.LaserAnalyzer.LaserData.background_fraction
    def run(self):

        
        while self._run_flag:
            if not self.paused:
                if self.typecamera=="Ueye": 
                    gray=np.copy(self.camera.capture())
                    
                    self.LaserAnalyzer=LaserAnalyzer(gray , self.pixel_size, units='μm', background_fraction=self.filter,crop=False)
                    gray=self.LaserAnalyzer.LaserData.image
                else:
                    self.camera.run()
                
                    gray=self.camera.frame
                
                    self.LaserAnalyzer=LaserAnalyzer(gray , self.pixel_size, units='μm', background_fraction=self.filter,crop=False)
                    gray=self.LaserAnalyzer.LaserData.image
                center_coordinates = (int(self.LaserAnalyzer.LaserData.xc), int(self.LaserAnalyzer.LaserData.yc))

                axesLength = int(self.LaserAnalyzer.LaserData.dx*0.5), int(self.LaserAnalyzer.LaserData.dy*0.5)

                angle = self.LaserAnalyzer.LaserData.phi*180/np.pi

                startAngle = 0

                endAngle = 360

                # Red color in BGR
                color = (255, 255, 255)

                # Line thickness of 5 px
                thickness = 1

                # Using cv2.ellipse() method
                # Draw a ellipse with red line borders of thickness of 5 px
                image = cv2.ellipse(cv2.applyColorMap(np.uint8(gray*(255/gray.max())), cv2.COLORMAP_JET), center_coordinates, axesLength,
                            angle, startAngle, endAngle, color, thickness)
                xp, yp = get_ellipse_axes(self.LaserAnalyzer.LaserData.xc, self.LaserAnalyzer.LaserData.yc, self.LaserAnalyzer.LaserData.dx, self.LaserAnalyzer.LaserData.dy, self.LaserAnalyzer.LaserData.phi)
                xp=xp.astype(int)
                yp=yp.astype(int)
                pt1 = (xp[0], yp[0])
                pt2 = (xp[1], yp[1])
                color = (255, 255, 255)

                cv2.line(image, pt1, pt2,color)
                pt1 = (xp[3], yp[3])
                pt2 = (xp[4], yp[4])
                cv2.line(image, pt1, pt2,color)
            

                #waits for user to press any key 
                #(this is necessary to avoid Python kernel form crashing)
                cv2.waitKey(0) 

                #closing all open windows 
                cv2.destroyAllWindows() 

                self.change_pixmap_signal.emit(image)
            # shut down capture system
        try:
            self.camera.release()
        except:
            pass
    
    def addimage(self,gray):
        self.LaserAnalyzer=LaserAnalyzer(gray , self.pixel_size, units='μm', background_fraction=self.filter,crop=False)

        center_coordinates = (int(self.LaserAnalyzer.LaserData.xc), int(self.LaserAnalyzer.LaserData.yc))

        axesLength = int(self.LaserAnalyzer.LaserData.dx*0.5), int(self.LaserAnalyzer.LaserData.dy*0.5)

        angle = 140+self.LaserAnalyzer.LaserData.phi*180/np.pi

        startAngle = 0

        endAngle = 360

        # Red color in BGR
        color = (255, 255, 255)

        # Line thickness of 5 px
        thickness = 1

        # Using cv2.ellipse() method
        # Draw a ellipse with red line borders of thickness of 5 px
        image = cv2.ellipse(cv2.applyColorMap(np.uint8(gray*(255/gray.max())), cv2.COLORMAP_JET), center_coordinates, axesLength,
                    angle, startAngle, endAngle, color, thickness)
        xp, yp = get_ellipse_axes(self.LaserAnalyzer.LaserData.xc, self.LaserAnalyzer.LaserData.yc, self.LaserAnalyzer.LaserData.dx, self.LaserAnalyzer.LaserData.dy, self.LaserAnalyzer.LaserData.phi)
        xp=xp.astype(int)
        yp=yp.astype(int)
        pt1 = (xp[0], yp[0])
        pt2 = (xp[1], yp[1])
        color = (255, 255, 255)

        cv2.line(image, pt1, pt2,color)
        pt1 = (xp[3], yp[3])
        pt2 = (xp[4], yp[4])
        cv2.line(image, pt1, pt2,color)
    

        #waits for user to press any key 
        #(this is necessary to avoid Python kernel form crashing)
        cv2.waitKey(0) 

        #closing all open windows 
        cv2.destroyAllWindows() 

        self.change_pixmap_signal.emit(image)

    def stop(self):
        """Sets run flag to False and waits for thread to finish"""
        self._run_flag = False
        self.wait()
    def show_information_message(self, title, message):
        message_box = QMessageBox(self.parent())  # Usar el QWidget padre como primer argumento
        message_box.information(self.parent(), title, message)

    def pause(self):
        """Pausa el hilo de video"""
        self.paused = True

    def resume(self):
        """Reanuda el hilo de video"""
        self.paused = False

# SET AS GLOBAL WIDGETS

widgets = None

class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.state_in = "home"
        # SET AS GLOBAL WIDGETS
        
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        global widgets
        widgets = self.ui

        # USE CUSTOM TITLE BAR | USE AS "False" FOR MAC OR LINUX
        
        Settings.ENABLE_CUSTOM_TITLE_BAR = True

        # APP NAME
        
        title = "Beamdiameter"
        description = "Beamdiameter"
        # APPLY TEXTS
        self.setWindowTitle(title)
        widgets.titleRightInfo.setText(description)

        # TOGGLE MENU
        
        #widgets.toggleButton.clicked.connect(lambda: UIFunctions.toggleMenu(self, True))

        # SET UI DEFINITIONS
        
        UIFunctions.uiDefinitions(self)

        # QTableWidget PARAMETERS
        
        widgets.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        
        #label
        widgets.value_gain.setText(str(widgets.GainSlider.value())+ " %")
        

        # LEFT MENUS
        widgets.btn_home.clicked.connect(self.buttonClick)
        widgets.btn_widgets.clicked.connect(self.buttonClick)
        widgets.btn_play.clicked.connect(self.buttonClick)
        widgets.btn_save.clicked.connect(self.buttonClick)
        widgets.btn_openimage.clicked.connect(self.buttonClick)
        widgets.btn_close.clicked.connect(self.closeEvent)
        widgets.btn_themes.clicked.connect(self.change_style)
        widgets.lineEdit.returnPressed.connect(self.do_action)
        double_validator = QDoubleValidator(0, 10, 16)
        locale = QLocale(QLocale.English, QLocale.UnitedStates)
        double_validator.setLocale(locale)
        double_validator.setNotation(QDoubleValidator.StandardNotation)
        widgets.lineEdit.setValidator(double_validator)
        widgets.GainSlider.sliderMoved.connect(self.gain_value)
        widgets.FactorBgSlider.sliderMoved.connect(self.factor_Bg_slider)
        self.btn_play_press=True

        self.image_label = QLabel(self)
        self.image_label2 = QLabel(self)


        self.disply_width = widgets.widget.size().width()+340
        self.display_height = widgets.widget.size().height()

        vbox = QVBoxLayout()
        vbox2 = QVBoxLayout()
        vbox.addWidget(self.image_label)
        vbox2.addWidget(self.image_label2)
        widgets.widget_video.setLayout(vbox)
        widgets.widget_2.setLayout(vbox2)
        ##plot
        #self.layout = QVBoxLayout()
        #self.canvas = MyMplCanvas(self, width=4, height=3, dpi=58)
        #self.layout.addWidget(self.canvas)
        #widgets.widget.setLayout(self.layout)

        #self.layout1 = QVBoxLayout()
        #self.canvas1 = MyMplCanvas(self, width=4, height=3, dpi=58)
        #self.layout1.addWidget(self.canvas1)
        #widgets.widget_4.setLayout(self.layout1)


        # create the video capture thread
        self.thread = VideoThread()
        
        self.graph_windows = []
        # connect its signal to the update_image slot
        self.thread.change_pixmap_signal.connect(lambda img: self.update_image(img,self.disply_width,self.display_height))
        # start the thread
        #self.thread.change_pixmap_signal.connect(lambda: self.update_graph1())
        #self.thread.change_pixmap_signal.connect(lambda: self.update_graph2())
        self.thread.start()
        self.paused = False
        try:
            if self.state_in=="btn_widgets":
                self.table_output(self.thread.LaserAnalyzer.data())
        except:
            None
        
        # Plot semiminor
        # self.zy = self.thread.LaserAnalyzer.Semiminor.ss
        # self.p = 0.0
        # self.smmy = self.thread.LaserAnalyzer.LaserData.zy
        # self.canvas.axes.set_title("Semieje menor")
        # self.canvas.axes.text(0, 100, '  Gaussian')
        # self.canvas.axes.set_xlabel('f desde el centro [%s]' % self.thread.LaserAnalyzer.LaserData.units)
        # self.canvas.axes.set_ylabel('Intensidad a lo largo del semieje menor (%)')
        # self.canvas.axes.set_title('Semieje menor')
        # try:

        #     self.line, = self.canvas.axes.plot(self.zy, self.smmy*100,'.b',label='original', animated=True, lw=2)
        #     self.line2, = self.canvas.axes.plot(self.zy, self.thread.LaserAnalyzer.Semiminor.I, 'red', label='Interpolada', animated=True, lw=2)
        # except:
        #     self.line, = self.canvas.axes.plot([], [],'.b',label='original', animated=True, lw=2)
        #     self.line2, = self.canvas.axes.plot([], [], 'red', label='Interpolada', animated=True, lw=2)
        # self.miniorlegend=self.canvas.axes.legend(numpoints=1)
        # self.ani = animation.FuncAnimation(
        #         self.canvas.figure,
        #         self.update_line,
        #         blit=True, interval=25,save_count=10
        #     )
        
        # Plot Semimajor
        # self.zx = self.thread.LaserAnalyzer.Semimajor.ss
        # self.smmx = self.thread.LaserAnalyzer.LaserData.zx
        # self.canvas1.axes.set_title("Semieje menor")
        # self.canvas1.axes.text(0, 100, '  Gaussian')
        # self.canvas1.axes.set_xlabel('Distancia desde el centro [%s]' % self.thread.LaserAnalyzer.LaserData.units)
        # self.canvas1.axes.set_ylabel('Intensidad a lo largo del semieje menor (%)')
        # self.canvas1.axes.set_title('Semieje mayor')
        # self.line21, = self.canvas1.axes.plot(self.zx, self.smmx*100,'.b',label='original', animated=True, lw=2)
        # self.line22, = self.canvas1.axes.plot(self.zx, self.thread.LaserAnalyzer.Semimajor.I, 'red', label='Interpolada', animated=True, lw=2)
        # self.canvas1.axes.legend(numpoints=1)

        # self.ani2 = animation.FuncAnimation(
        #         self.canvas1.figure,
        #         self.update_line2,
        #         blit=True, interval=25,save_count=10
        #     )
        #self.show()
    
        
        self.graphWidget = pg.PlotWidget()
        layout_minorpq=QVBoxLayout(widgets.widget_4)
        layout_minorpq.addWidget(self.graphWidget)
        self.graphWidget.setBackground('w')
        pen = pg.mkPen(color=(255, 0, 0))
        self.zx = self.thread.LaserAnalyzer.Semimajor.ss
        self.smmx = self.thread.LaserAnalyzer.LaserData.zx
        self.canvas01= pg.PlotCurveItem(x = self.zx, 
                                    y = self.thread.LaserAnalyzer.Semimajor.I, 
                                    pen = pg.mkPen(color = "r"),
                                    name = "adjust", 
                                    antialias = True)
        self.data_canvas012 =  self.graphWidget.plotItem
        self.data_canvas012.setLabels(bottom = 'Distancia desde el centro [%s]' % self.thread.LaserAnalyzer.LaserData.units, 
                     left = 'Intensidad a lo largo del semimajor (%)' , 
                     top = "Semimajor")
  
        self.data_canvas012.addLegend(offset = (0,5),labelTextSize = "11pt")
        self.scatter=pg.ScatterPlotItem(x = self.zx, 
                                      y = self.smmx*100, 
                                      symbol = "o", 
                                      pen = pg.mkPen(None), 
                                      brush = pg.mkBrush("b"),
                                      size = 4,        
                                      name = "original", 
                                      antialias = True)
        self.data_canvas012.addItem(self.scatter)
        self.data_canvas012.addItem(self.canvas01)
        #2
        self.zy = self.thread.LaserAnalyzer.Semiminor.ss

        self.smmy = self.thread.LaserAnalyzer.LaserData.zy
        self.graphWidget2 = pg.PlotWidget()
        layout_minorpq2=QVBoxLayout(widgets.widget)
        layout_minorpq2.addWidget(self.graphWidget2)
        self.graphWidget2.setBackground('w')
        pen = pg.mkPen(color=(255, 0, 0))
        self.canvas02= pg.PlotCurveItem(x = self.zy, 
                                    y = self.thread.LaserAnalyzer.Semimajor.I, 
                                    pen = pg.mkPen(color = "r"),
                                    name = "adjust", 
                                    antialias = True)
        self.data_canvas022 =  self.graphWidget2.plotItem
        self.data_canvas022.setLabels(bottom = 'Distancia desde el centro [%s]' % self.thread.LaserAnalyzer.LaserData.units, 
                     left = 'Intensidad a lo largo del semiminor (%)' , 
                     top = "Semiminor")
  
        self.data_canvas022.addLegend(offset = (0,5),labelTextSize = "11pt")
        self.scatter2=pg.ScatterPlotItem(x = self.zy, 
                                      y = self.smmy*100, 
                                      symbol = "o", 
                                      pen = pg.mkPen(None), 
                                      brush = pg.mkBrush("b"),
                                      size = 4,        
                                      name = "original", 
                                      antialias = True)
        self.data_canvas022.addItem(self.scatter2)
        self.data_canvas022.addItem(self.canvas02)

        

    


        self.timer=QTimer(self)
        self.timer.timeout.connect(self.update_graph1)
        self.timer.timeout.connect(self.update_graph2)
        #self.timer.timeout.connect(self.update_table_home)
        self.timer.start(60)
        #tabla home
        
        layoutable = QVBoxLayout()
        self.tablehome=QTableWidget()
        filas = 7
        columnas = 5
        self.tablehome.setRowCount(filas)
        self.tablehome.setColumnCount(columnas)
        self.tablehome.setEditTriggers(QTableWidget.NoEditTriggers)
        # Ocultar los encabezados de fila
        self.tablehome.verticalHeader().setVisible(False)
        self.tablehome.horizontalHeader().setVisible(False)
        widgets.tableWidget.verticalHeader().setVisible(False)
        widgets.tableWidget.horizontalHeader().setVisible(True)
        # Combinar la primera fila de la primera columna con la segunda fila de la primera columna
        self.tablehome.setSpan(0, 0, 2, 1)

        # Dividir las columnas como se indica en el diseño original
        self.tablehome.setSpan(0, 1, 1, 2)
        self.tablehome.setSpan(0, 3, 1, 2)
        self.tablehome.setSpan(2, 1, 1, 2)
        self.tablehome.setSpan(2, 3, 1, 2)
        self.tablehome.setSpan(6, 1, 1, 2)
        self.tablehome.setSpan(6, 3, 1, 2)
        
        layoutable.addWidget(self.tablehome)
        widgets.widget_3.setLayout(layoutable)
        
        # EXTRA LEFT BOX
        def openCloseLeftBox():
            UIFunctions.toggleLeftBox(self, True)
        #widgets.toggleLeftBox.clicked.connect(openCloseLeftBox)
        #widgets.extraCloseColumnBtn.clicked.connect(openCloseLeftBox)

        # EXTRA RIGHT BOX
        def openCloseRightBox():
            UIFunctions.toggleRightBox(self, True)
        widgets.settingsTopBtn.clicked.connect(openCloseRightBox)
        widgets.ButtonBackgraund.clicked.connect(self.get_factor_backgraund)
        # SHOW APP
        
        widgets.contentTopBg.mouseMoveEvent=self.mouseMoveEvent
        widgets.stackedWidget.mouseMoveEvent=self.mouseMoveEventNone
        self.show()

        # SET CUSTOM THEME
        
        self.current_style = 1

        # SET HOME PAGE AND SELECT MENU
        
        widgets.stackedWidget.setCurrentWidget(widgets.home)
        widgets.btn_home.setStyleSheet(UIFunctions.selectMenu(widgets.btn_home.styleSheet()))
    def gain_value(self):
        value=widgets.GainSlider.value()
        widgets.value_gain.setText(str(widgets.GainSlider.value())+ " %")
        self.thread.camera.update_gain(gain_value=int(value))

    def factor_Bg_slider(self):
        value=widgets.GainSlider.value()
        widgets.value_FactorBg.setText(str(widgets.FactorBgSlider.value()/100)+ " %")
        self.thread.filter=widgets.FactorBgSlider.value()/1000
    def change_style(self):
        # Toggle between two styles
        if self.current_style == 1:
            self.set_style(2)
            self.current_style = 2
        else:
            self.set_style(1)
            self.current_style = 1

    def set_style(self, style):
        themes_directory = os.path.join(os.path.dirname(__file__), "themes")
        
        if style == 1:
            qss_file = "py_dracula_dark.qss"
        
        else:
            qss_file = "py_dracula_light.qss"
        themeFile = os.path.join(themes_directory, qss_file)
        
        # LOAD AND APPLY STYLE
        UIFunctions.theme(self, themeFile, True)

        # SET HACKS
        #AppFunctions.setThemeHack(self)
    
    def stop_video_and_animation(self):
        if self.thread.isRunning():
            if self.thread.paused:
                # Resume the thread

                self.thread.resume()
                
                widgets.btn_play.setText("Pause")
                widgets.btn_play.setToolTip("Pause")
            else:
                # Pause the thread
                self.thread.pause()

                widgets.btn_play.setText("Play")
                widgets.btn_play.setToolTip("Play")
    
    



    # BUTTONS CLICK
    # Post here your functions for clicked buttons
    
    def buttonClick(self):
        # GET BUTTON CLICKED
        btn = self.sender()
        btnName = btn.objectName()

        # SHOW HOME PAGE
        if btnName == "btn_home":
            self.state_in ="home"

            widgets.stackedWidget.setCurrentWidget(widgets.home)
            UIFunctions.resetStyle(self, btnName)
            btn.setStyleSheet(UIFunctions.selectMenu(btn.styleSheet()))

        # SHOW WIDGETS PAGE
        if btnName == "btn_widgets":
    
            self.state_in ="btn_widgets"
            widgets.stackedWidget.setCurrentWidget(widgets.widgets)
            UIFunctions.resetStyle(self, btnName)
            btn.setStyleSheet(UIFunctions.selectMenu(btn.styleSheet()))

        # SHOW NEW PAGE
        if btnName == "btn_new":
            widgets.stackedWidget.setCurrentWidget(widgets.new_page) # SET PAGE
            UIFunctions.resetStyle(self, btnName) # RESET ANOTHERS BUTTONS SELECTED
            btn.setStyleSheet(UIFunctions.selectMenu(btn.styleSheet())) # SELECT MENU
            
        if btnName == "btn_play":
            #btn.setStyleSheet("background-image: url(:/icons/images/icons/cil-caret-right.png);")  
            #widgets.stackedWidget.setCurrentWidget(widgets.new_page) # SET PAGE
            #UIFunctions.resetStyle(self, btnName) # RESET ANOTHERS BUTTONS SELECTED
            #btn.setStyleSheet(UIFunctions.selectMenu(btn.styleSheet())) # SELECT MENU

            self.stop_video_and_animation()
            if self.btn_play_press==True:
                btn.setStyleSheet("background-image: url(:/icons/images/icons/cil-caret-right.png);")
                self.btn_play_press=False
            else:
                btn.setStyleSheet("background-image:  url(:/icons/images/icons/cil-media-pause.png);")
                self.btn_play_press=True
        if btnName == "btn_save":
            print("Save BTN clicked!")

        if btnName == "btn_openimage":
            fileName, _ = QFileDialog.getOpenFileName(self, "Open Image", "", "Image Files (*.png *.jpg *.jpeg *.bmp *.gif *.tiff *.webp *.svg *.ico)")
            if fileName!="":
                self.btn_play_press=False
                self.add_image(fileName,self.disply_width,self.display_height)
    
    
    
    @Slot(np.ndarray)
    def update_image(self, frame,widget_width,widget_height):
        """Updates the image_label with a new opencv image"""
        if self.state_in =="btn_widgets":
            self.disply_width = widgets.widget.size().width()
            self.display_height = widgets.widget.size().height()
            qt_img = self.convert_cv_qt(frame,widget_width,widget_height)
            self.image_label.setPixmap(qt_img)
        
            self.table_output(self.thread.LaserAnalyzer.data())
            
        if self.state_in == "home":
            self.disply_width = widgets.widget.size().width()
            self.display_height = widgets.widget.size().height()
            qt_img = self.convert_cv_qt(frame,widget_width,widget_height)
            self.image_label2.setPixmap(qt_img)
            self.update_table_home()
    def add_image(self, frame,widget_width,widget_height):
        """Updates the image_label with a new opencv image"""
        if type(frame)==str:
            frame =cv2.imread(frame)
        if(len(frame.shape)<3):
            frame
        elif len(frame.shape)==3:
            frame=cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        self.disply_width = widgets.widget.size().width()
        self.display_height = widgets.widget.size().height()
        qt_img = self.convert_cv_qt(frame,widget_width,widget_height)
        self.image_label.setPixmap(qt_img)
        self.thread.addimage(frame)
        self.table_output(self.thread.LaserAnalyzer.data())
        

        self.disply_width = widgets.widget.size().width()
        self.display_height = widgets.widget.size().height()
        qt_img = self.convert_cv_qt(frame,widget_width,widget_height)
        self.image_label2.setPixmap(qt_img)
        self.update_table_home()
    @Slot()
    def update_graph1(self):
        if not self.paused and self.state_in == "home":
            
            self.zy=self.thread.LaserAnalyzer.Semiminor.ss
            y = self.thread.LaserAnalyzer.LaserData.zy
            self.canvas01.setData(self.zy, self.thread.LaserAnalyzer.Semiminor.I)  # Update the data.
            self.scatter.setData(self.zy, y*100)  # Update the data.

    @Slot()
    def update_graph2(self):
        if not self.paused and self.state_in == "home":
            self.zx=self.thread.LaserAnalyzer.Semimajor.ss
            y = self.thread.LaserAnalyzer.LaserData.zx
            self.canvas02.setData(self.zx, self.thread.LaserAnalyzer.Semimajor.I)  # Update the data.
            self.scatter2.setData(self.zx, y*100)  # Update the data.
    @Slot()
    def update_table_home(self):
        if not self.paused and self.state_in == "home":
            # Supongamos que tienes un DataFrame llamado 'dataframe' con datos
            df=self.thread.LaserAnalyzer.data()
            df["semi-axis major beam"][0]
            dataframe = pd.DataFrame({
                'Col 1': ["", "", "Centroid [μm]", "Width [μm] (80%)", "Width [μm] (50%)","Width [μm] (13.5%)", "Correlation (%)"], # Añadimos una fila vacía
                'Col 2': ["Semimajor", "Beam", df["semi-axis major beam"][4], df["semi-axis major beam"][2], df["semi-axis major beam"][1], df["semi-axis major beam"][0], df["semi-axis major beam"][5]], # Añadimos elementos vacíos en los bordes
                'Col 3': ["3", "Gaussian", 23, df["semi-axis major gaussian"][2], df["semi-axis major gaussian"][1], df["semi-axis major gaussian"][0], ""],
                'Col 4': ["Semiminor", "Beam", df["semi-axis minor beam"][4], df["semi-axis minor beam"][2], df["semi-axis minor beam"][1], df["semi-axis minor beam"][0], df["semi-axis minor beam"][5]],
                'Col 5': ["5", "Gaussian", 43, df["semi-axis minor gaussian"][2], df["semi-axis minor gaussian"][1], df["semi-axis minor gaussian"][0], ""]
            })
            

            filas = 7
            columnas = 5
            
            
            for row in range(dataframe.shape[0]):
                for col in range(dataframe.shape[1]):
                    item = QTableWidgetItem(str(dataframe.iat[row, col]))
                    self.tablehome.setItem(row, col, item)  

            for row in range(filas):
                for col in range(columnas):
                    item = self.tablehome.item(row, col)
                    if item is not None:
                        if not col==0:
                            item.setTextAlignment(Qt.AlignCenter)        
            self.tablehome.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents) 

       
    def update_line(self, i):
        self.p += 0.1
        self.zx = self.thread.LaserAnalyzer.Semimajor.ss
        y = self.thread.LaserAnalyzer.LaserData.zy
        self.line.set_ydata(y*100)
        self.line.set_xdata(self.zx)
        self.line2.set_xdata(self.zx)
        htext=self.miniorlegend
        self.line2.set_ydata(self.thread.LaserAnalyzer.Semimajor.I)

        return [self.line,self.line2]
    
    def update_line2(self, i):
        
        self.p += 0.1
        self.zy=self.thread.LaserAnalyzer.Semiminor.ss
        y = self.thread.LaserAnalyzer.LaserData.zx
        self.line21.set_ydata(y*100)
        self.line21.set_xdata(self.zy)
        self.line22.set_xdata(self.zy)
        htext=self.miniorlegend
        self.line22.set_ydata(self.thread.LaserAnalyzer.Semimajor.I)

        return [self.line21,self.line22]
    
    def convert_cv_qt(self, frame, widget_width, widget_height):
        """Convert from an opencv image to QPixmap"""
        rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image_width = frame.shape[1]
        image_height = frame.shape[0]

        # Calcula la escala necesaria
        scale_width = widget_width / image_width
        scale_height = widget_height / image_height
        min_scale = min(scale_width, scale_height)

        # Escala la imagen y crea un QImage
        scaled_image = cv2.resize(rgb_image, (int(image_width * min_scale), int(image_height * min_scale)))
        h, w, ch = scaled_image.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QImage(scaled_image.data, w, h, bytes_per_line, QImage.Format.Format_RGB888)

        # Escala la imagen para mantener la relación de aspecto y crea un QPixmap
        p = convert_to_Qt_format.scaled(widget_width, widget_height, Qt.AspectRatioMode.KeepAspectRatioByExpanding)
        return QPixmap.fromImage(p)



    # RESIZE EVENTS
    
    def resizeEvent(self, event):
        # Update Size Grips
        UIFunctions.resize_grips(self)

    # MOUSE CLICK EVENTS
    


    def do_action(self):
        self.pixel_size = float(widgets.lineEdit.text())

        self.thread.pixel_size=self.pixel_size
    
    def get_factor_backgraund(self):
        self.thread.LaserAnalyzer.calibrate_LaserData_backgraund_noise()
        self.thread.filter=self.thread.LaserAnalyzer.LaserData.background_fraction
    
    def table_output(self, df):
        column_names = df.columns.tolist()

        # Inserta una nueva fila al principio con los nombres de las columnas
        
        num_filas, num_columnas = df.shape

        # Configurar el número de filas y columnas en el QTableWidget
        widgets.tableWidget.setRowCount(num_filas)
        widgets.tableWidget.setColumnCount(num_columnas)

        for row in range(num_filas):
            for col in range(num_columnas):
                item = QTableWidgetItem(str(df.iat[row, col]))
                widgets.tableWidget.setItem(row, col, item)

        # Establecer los encabezados de columna en el QTableWidget
        widgets.tableWidget.setHorizontalHeaderLabels(list(df.columns))

        # Ajustar el tamaño de las columnas
        #widgets.tableWidget.resizeColumnsToContents()

        # Mostrar la ventana con QTableWidget
        widgets.tableWidget.show()

    def mousePressEvent(self, event):
        self.dragPos = event.globalPosition()

    def mouseMoveEvent(self, event):
        if hasattr(self, 'dragPos'):
            delta = event.globalPosition() - self.dragPos
            parent_window = self.window()  # Accede al widget principal de la ventana
            parent_window.move(parent_window.x() + delta.x(), parent_window.y() + delta.y())
            self.dragPos = event.globalPosition()
            #if parent_window.y() + delta.y()<-60:
            #    self.showMaximized()
            #print(parent_window.x() + delta.x(), parent_window.y() + delta.y())
    def mouseMoveEventNone(self, event):
        pass
    def closeEvent(self, event):
        self.thread.stop()
        sys.exit(0)
        event.accept()
        


        

if __name__ == "__main__":
    import time
    pbar = """
    QProgressBar {
    background-color: #19232D;
    border: 1px solid #455364;
    color: #E0E1E3;
    border-radius: 4px;
    text-align: center;
    }

    QProgressBar:disabled {
    background-color: #19232D;
    border: 1px solid #455364;
    color: #9DA9B5;
    border-radius: 4px;
    text-align: center;
    }

    QProgressBar::chunk {
    background-color: #346792;
    color: #19232D;
    border-radius: 4px;
    }

    QProgressBar::chunk:disabled {
    background-color: #26486B;
    color: #9DA9B5;
    border-radius: 4px;
    }
    """
    app = QApplication(sys.argv)
    if sys.platform == 'win32':
        app.setStyle(QStyleFactory.create("Fusion"))
    app.setStyleSheet(pbar)
    app.setWindowIcon(QIcon("icon.ico"))
    splash_pix = QPixmap('images/images/pixmap.jpg')

    splash = QSplashScreen(splash_pix, Qt.WindowType.WindowStaysOnTopHint)
    splash.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.FramelessWindowHint)
    splash.setEnabled(False)
    # splash = QSplashScreen(splash_pix)
    # adding progress bar
    progressBar = QProgressBar(splash)
    progressBar.setMaximum(10)
    progressBar.setAlignment(Qt.AlignmentFlag.AlignCenter)

    progressBar.setGeometry(0, splash_pix.height() - 10, splash_pix.width(), 10)

    # splash.setMask(splash_pix.mask())

    splash.show()
    for i in range(1, 11):
        progressBar.setValue(i)
        t = time.time()
        while time.time() < t + 0.1:
           app.processEvents()

    # Simulate something that takes time
    time.sleep(1)
    
    window = MainWindow()
    window.show()
    splash.close()
    sys.exit(app.exec())


# @software{Wanderson-Magalhaes,
#   author       = {Wanderson, Magalhaes},
#   title        = {{PyDracula - GUI moderna PySide6 / PyQt6}},
#   year         = 2021,
#   publisher    = {Github},
#   version      = {1.0.0},
#   url          = {https://github.com/Wanderson-Magalhaes/Modern_GUI_PyDracula_PySide6_or_PyQt6}
# }
