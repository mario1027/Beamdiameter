# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'tabla.ui'
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
from PySide6.QtWidgets import (QApplication, QDialog, QGridLayout, QHeaderView,
    QSizePolicy, QTableView, QWidget)

class Ui_tabla(object):
    def setupUi(self, tabla):
        if not tabla.objectName():
            tabla.setObjectName(u"tabla")
        tabla.resize(621, 452)
        icon = QIcon()
        icon.addFile(u"../imagenes/Figure_2-.ico", QSize(), QIcon.Normal, QIcon.Off)
        tabla.setWindowIcon(icon)
        self.gridLayout = QGridLayout(tabla)
        self.gridLayout.setObjectName(u"gridLayout")
        self.tableView = QTableView(tabla)
        self.tableView.setObjectName(u"tableView")

        self.gridLayout.addWidget(self.tableView, 0, 0, 1, 1)


        self.retranslateUi(tabla)

        QMetaObject.connectSlotsByName(tabla)
    # setupUi

    def retranslateUi(self, tabla):
        tabla.setWindowTitle(QCoreApplication.translate("tabla", u"Tabla", None))
    # retranslateUi

