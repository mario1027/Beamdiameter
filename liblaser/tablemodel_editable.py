from PySide6.QtCore import Qt
from PySide6.QtGui import QColor
from PySide6.QtWidgets import QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget

class PandasTable(QTableWidget):
    def __init__(self, data):
        super().__init__()

        self.setData(data)

    def setData(self, data):
        self.setRowCount(data.shape[0])
        self.setColumnCount(data.shape[1])

        self.setHorizontalHeaderLabels(list(data.columns))

        for row in range(data.shape[0]):
            for col in range(data.shape[1]):
                item = QTableWidgetItem(str(data.iat[row, col]))
                self.setItem(row, col, item)

class MyWidget(QWidget):
    def __init__(self, data):
        super().__init()

        layout = QVBoxLayout(self)

        table_widget = PandasTable(data)

        layout.addWidget(table_widget)

        self.setLayout(layout)
