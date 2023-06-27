import sys
import socket
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox
from PyQt5 import uic
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtGui import QIcon

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('127.0.0.1',12345))
server_socket.listen(5)

class ImageEditor(QMainWindow):
    def __init__(self):
        super(ImageEditor,self).__init__()
        uic.loadUi("design.ui",self) # Load the UI file
        self.setWindowTitle("Photo Editing app")
        self.setWindowIcon(QIcon("download.jpg"))
        self.image_path = None
        self.original_image = None
        self.modified_image = None

        self.rotate.clicked.connect(self.rotate_image)
        self.flip.clicked.connect(self.flip_lr)
        self.main.clicked.connect(self.flip_ud)
        self.filter1.clicked.connect(self.clip_image)
        self.filter2.clicked.connect(self.clip_image2)
        self.filter3.clicked.connect(self.clip_image3)
        self.save.clicked.connect(self.save_changes)
        self.cancel.clicked.connect(self.cancel_changes)

        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        self.image.addWidget(self.canvas)

    
    def display_image(self, image):
        self.figure.clear()
        plt.imshow(image)
        self.canvas.draw()
    
    def rotate_image(self):
        self.modified_image = np.rot90(self.modified_image)
        self.display_image(self.modified_image)

    def flip_lr(self):
        self.modified_image = np.fliplr(self.modified_image)
        self.display_image(self.modified_image)
        
    def flip_ud(self):
        self.modified_image = np.flipud(self.modified_image)
        self.display_image(self.modified_image)
    
    def clip_image(self):
        self.modified_image = np.clip(self.modified_image, 60, 200)
        self.display_image(self.modified_image)

    def clip_image2(self):
        self.modified_image = np.clip(self.modified_image, 80, 220)
        self.display_image(self.modified_image)

    def clip_image3(self):
        self.modified_image = np.clip(self.modified_image, 40, 150)
        self.display_image(self.modified_image)

    def save_changes(self):
        if self.image_path:
            save_path, _ = QFileDialog.getSaveFileName(self, "Save Image", "", "Image Files (*.png *.jpg)")
            if save_path:
                plt.imsave(save_path, self.modified_image)
                QMessageBox.information(self, "Save Changes", "Changes saved successfully")
        else:
            QMessageBox.warning(self, "Save changes", "No image loaded.")

    def cancel_changes(self):
        if self.original_image is not None:
            self.modified_image = self.original_image.copy()
            self.display_image(self.original_image)
            QMessageBox.information(self, "Cancel Changes", "Changes are removed")
        else:
            QMessageBox.warning(self, "Cancel Changes", "No image loaded.")

app = QApplication(sys.argv)
window = ImageEditor()
window.show()
sys.exit(app.exec_())

