import sys
import cv2
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtWidgets import QApplication, QLabel, QPushButton, QVBoxLayout, QWidget, QFileDialog
from camera import UeyeCamera
import numpy as np
class CameraApp(QWidget):
    def __init__(self):
        super().__init__()

        self.video_capture = UeyeCamera(0)  # Puedes cambiar 0 por otro número si tienes múltiples cámaras.
        x,y,width,height=self.video_capture.get_aoi()
        self.video_capture.init(x=x, y=y ,width = width, height = height,
            exposure = 30)
        self.image_label = QLabel(self)
        self.frame_counter_label = QLabel(self)
        self.timer_label = QLabel(self)

        self.capture_button = QPushButton("Capturar", self)
        self.capture_button.clicked.connect(self.toggle_capture)

        self.frame_count = 0
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)

        self.is_capturing = False
        self.output_directory = ""

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.addWidget(self.image_label)
        layout.addWidget(self.frame_counter_label)
        layout.addWidget(self.timer_label)
        layout.addWidget(self.capture_button)

        self.setWindowTitle("Capturador de Imágenes")
        self.setGeometry(100, 100, 800, 600)

    def toggle_capture(self):
        if not self.is_capturing:
            self.output_directory = self.get_output_directory()
            if self.output_directory:
                self.is_capturing = True
                self.capture_button.setText("Detener")
                self.timer.start(1000 // 10)  # Inicia el temporizador si la captura está habilitada.
        else:
            self.is_capturing = False
            self.capture_button.setText("Capturar")
            self.timer.stop()

    def get_output_directory(self):
        dialog = QFileDialog()
        dialog.setFileMode(QFileDialog.Directory)
        dialog.setOption(QFileDialog.ShowDirsOnly, True)
        if dialog.exec_() == QFileDialog.Accepted:
            return dialog.selectedFiles()[0]
        return ""

    def capture_frame(self):
        frame=np.copy(self.video_capture.capture())
        
        image_path = f"{self.output_directory}/frame_{self.frame_count}.png"
        cv2.imwrite(image_path, frame)
        self.frame_count += 1

    def update_frame(self):
        frame=np.copy(self.video_capture.capture())
        
        height, width,_ = frame.shape
        bytes_per_line = 3 * width
        q_image = QImage(frame.data, width, height, bytes_per_line, QImage.Format.Format_RGB888)
        pixmap = QPixmap.fromImage(q_image)
        self.image_label.setPixmap(pixmap)

        self.frame_counter_label.setText(f"Frames guardados: {self.frame_count}")
        self.timer_label.setText(f"Tiempo transcurrido: {self.frame_count / 10} segundos")

        if self.is_capturing:
            self.capture_frame()

    def closeEvent(self, event):
        self.video_capture.stop()
        event.accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = CameraApp()
    window.show()
    sys.exit(app.exec_())
