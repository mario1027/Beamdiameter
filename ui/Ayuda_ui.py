# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Ayuda.ui'
##
## Created by: Qt User Interface Compiler version 6.6.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QDialog, QSizePolicy, QTextBrowser,
    QVBoxLayout, QWidget)

class Ui_Ayuda(object):
    def setupUi(self, Ayuda):
        if not Ayuda.objectName():
            Ayuda.setObjectName(u"Ayuda")
        Ayuda.resize(805, 643)
        icon = QIcon()
        icon.addFile(u"../imagenes/Figure_2-.ico", QSize(), QIcon.Normal, QIcon.Off)
        Ayuda.setWindowIcon(icon)
        self.verticalLayout = QVBoxLayout(Ayuda)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.textBrowser = QTextBrowser(Ayuda)
        self.textBrowser.setObjectName(u"textBrowser")

        self.verticalLayout.addWidget(self.textBrowser)


        self.retranslateUi(Ayuda)

        QMetaObject.connectSlotsByName(Ayuda)
    # setupUi

    def retranslateUi(self, Ayuda):
        Ayuda.setWindowTitle(QCoreApplication.translate("Ayuda", u"Ayuda", None))
        self.textBrowser.setHtml(QCoreApplication.translate("Ayuda", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:'Ubuntu'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" background-color:transparent;\">Guardar: </span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" background-color:transparent;\"><br />Para guardar archivos, se debe ir a la opci\u00f3n men\u00fa -&gt; Guardar, el archivo se le debe asignar un nombre y se guardara con una extensi\u00f3n .30j, este archivo es un objeto que contiene la informaci\u00f3n y par\u00e1metros del perfil gaussiano. </span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-to"
                        "p:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" background-color:transparent;\">Abrir archivo: </span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /><span style=\" background-color:transparent;\">Para abrir los archivos se debe ir a la opci\u00f3n men\u00fa -&gt; Abrir, en esta opci\u00f3n, solo se podra abrir un archivo de formato .03j. </span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" background-color:transparent;\">Abrir imagen: </span></p>\n"
"<p style"
                        "=\"-qt-paragraph-type:empty; margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" background-color:transparent;\">Para abrir una imagen, se debe ir a la opci\u00f3n men\u00fa -&gt; Seleccionar imagen, con compatibilidad con los formatos *.bmp *.cur *.gif *.icns *.ico *.jpeg *.jpg *.pbm *.pgm *.png *.ppm *.svg *.svgz *.tga *.tif *.tiff *.wbmp *.webp *.xbm *.xpm. </span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" background-color:transparent;\"><br />Visualizar gr\u00e1ficas individualmente: </span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" background-color:transparent;\"><br />En la opci\u00f3n Visual"
                        "izar podemos encontrar cada una de las graficas, en donde podemos navegar, cambiar la presentaci\u00f3n, t\u00edtulos, legendas y la opci\u00f3n para guardar la gr\u00e1fica, para mayor informaci\u00f3n puede leer la documentaci\u00f3n de la librer\u00eda Matplotlib.</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" background-color:transparent;\">Tema o apariencia: </span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" background-color:transparent;\">En la opci\u00f3n, Opciones -&gt; Aparien"
                        "cia, puede encontrar la lista de temas disponibles de la versi\u00f3n, que puede usar. </span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" background-color:transparent;\">Pixel size: </span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" background-color:transparent;\">Esta opci\u00f3n esta relacionada con las dimensiones de los pixeles de la c\u00e1mara usada, esta informaci\u00f3n puede ser encontrada con el fabricante con la referencia del equipo. </span></p>\n"
"<p style=\"-qt-paragraph-ty"
                        "pe:empty; margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" background-color:transparent;\">Filtro: </span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" background-color:transparent;\">Esta opci\u00f3n reduce el ruido al rededor del centroide, seg\u00fan el an\u00e1lisis de variaci\u00f3n en el m\u00e9todo ISO \u2013 11146:2021 lo cual se recomienda 0,035, pero cada imagen necesita variar este par\u00e1metro seg\u00fan el ruido alrededor del centroide.</span><br /></p></body></html>", None))
    # retranslateUi

