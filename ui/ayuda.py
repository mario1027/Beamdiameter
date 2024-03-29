# Form implementation generated from reading ui file 'Ayuda.ui'
#
# Created by: PyQt6 UI code generator 6.4.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_Ayuda(object):
    def setupUi(self, Ayuda):
        Ayuda.setObjectName("Ayuda")
        Ayuda.resize(805, 643)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("../imagenes/Figure_2-.ico"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        Ayuda.setWindowIcon(icon)
        self.verticalLayout = QtWidgets.QVBoxLayout(Ayuda)
        self.verticalLayout.setObjectName("verticalLayout")
        self.textBrowser = QtWidgets.QTextBrowser(parent=Ayuda)
        self.textBrowser.setObjectName("textBrowser")
        self.verticalLayout.addWidget(self.textBrowser)

        self.retranslateUi(Ayuda)
        QtCore.QMetaObject.connectSlotsByName(Ayuda)

    def retranslateUi(self, Ayuda):
        _translate = QtCore.QCoreApplication.translate
        Ayuda.setWindowTitle(_translate("Ayuda", "Ayuda"))
        self.textBrowser.setHtml(_translate("Ayuda", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Ubuntu\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" background-color:transparent;\">Guardar: </span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" background-color:transparent;\"><br />Para guardar archivos, se debe ir a la opción menú -&gt; Guardar, el archivo se le debe asignar un nombre y se guardara con una extensión .30j, este archivo es un objeto que contiene la información y parámetros del perfil gaussiano. </span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" background-color:transparent;\">Abrir archivo: </span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /><span style=\" background-color:transparent;\">Para abrir los archivos se debe ir a la opción menú -&gt; Abrir, en esta opción, solo se podra abrir un archivo de formato .03j. </span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" background-color:transparent;\">Abrir imagen: </span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" background-color:transparent;\">Para abrir una imagen, se debe ir a la opción menú -&gt; Seleccionar imagen, con compatibilidad con los formatos *.bmp *.cur *.gif *.icns *.ico *.jpeg *.jpg *.pbm *.pgm *.png *.ppm *.svg *.svgz *.tga *.tif *.tiff *.wbmp *.webp *.xbm *.xpm. </span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" background-color:transparent;\"><br />Visualizar gráficas individualmente: </span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" background-color:transparent;\"><br />En la opción Visualizar podemos encontrar cada una de las graficas, en donde podemos navegar, cambiar la presentación, títulos, legendas y la opción para guardar la gráfica, para mayor información puede leer la documentación de la librería Matplotlib.</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" background-color:transparent;\">Tema o apariencia: </span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" background-color:transparent;\">En la opción, Opciones -&gt; Apariencia, puede encontrar la lista de temas disponibles de la versión, que puede usar. </span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" background-color:transparent;\">Pixel size: </span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" background-color:transparent;\">Esta opción esta relacionada con las dimensiones de los pixeles de la cámara usada, esta información puede ser encontrada con el fabricante con la referencia del equipo. </span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" background-color:transparent;\">Filtro: </span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" background-color:transparent;\">Esta opción reduce el ruido al rededor del centroide, según el análisis de variación en el método ISO – 11146:2021 lo cual se recomienda 0,035, pero cada imagen necesita variar este parámetro según el ruido alrededor del centroide.</span><br /></p></body></html>"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Ayuda = QtWidgets.QDialog()
    ui = Ui_Ayuda()
    ui.setupUi(Ayuda)
    Ayuda.show()
    sys.exit(app.exec())
