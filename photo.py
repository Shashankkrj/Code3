import sys
import cv2
from PyQt5.QtWidgets import QLabel, QApplication, QMainWindow, QFileDialog,QMessageBox
from PyQt5 import uic
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtGui import QIcon, QImage, QPixmap

class ImageEditor(QMainWindow):
    def __init__(self):
        super(ImageEditor,self).__init__()
        uic.loadUi("design.ui",self) # Load the UI file
        self.setWindowTitle("Baggage Scanner System")
        self.setWindowIcon(QIcon("LOGO.png"))
        self.image_path = None
        self.original_image = None
        self.modified_image = None

        self.browse_img_file.clicked.connect(self.browse_image_file)
        self.browse_noobj_file.clicked.connect(self.browse_noobject_file)
        self.rotate.clicked.connect(self.rotate_image)
        self.flip.clicked.connect(self.flip_lr)
        self.main.clicked.connect(self.flip_ud)
        self.filter1.clicked.connect(self.clip_image)
        self.filter2.clicked.connect(self.clip_image2)
        self.filter3.clicked.connect(self.clip_image3)
        self.save.clicked.connect(self.save_changes)
        self.cancel.clicked.connect(self.cancel_changes)
        # self.figure = plt.figure()
        # self.canvas = FigureCanvas(self.figure)
        # self.img_label.addWidget(self.canvas)

    def browse_image_file(self):
        file_dialog = QFileDialog()
        image_path, _ = file_dialog.getOpenFileName(self, "Select File", "", "All Files (*.*)")
        orig_image = cv2.imread(image_path)
        image_text = orig_image.tobytes().hex()
        text_file_path = "path_to_save_text_file.txt"
        with open(text_file_path, 'w') as file:
            file.write(image_text)
        
        # Read the image data from the text file
        with open(text_file_path, 'r') as file:
            image_data = file.read()
        # Convert the image data to bytes
        image_bytes = bytes.fromhex(image_data)
        # Create a QImage from the image bytes
        qimage = QImage.fromData(image_bytes)
        # Create a QPixmap from the QImage
        pixmap = QPixmap.fromImage(qimage)
        # Set the pixmap on the QLabel to display the image
        self.img_label.setPixmap(pixmap)

    #     if image_path:
    #         self.image_path = image_path
    #         self.original_image = plt.imread(image_path)
    #         self.modified_image = self.original_image.copy()
    #         self.display_image(self.original_image)

    def browse_noobject_file(self):
        file_dialog = QFileDialog()
        image_path, _ = file_dialog.getOpenFileName(self, "Select File", "", "All Files (*.*)")
        # # Read the image using OpenCV or any other library
        # image = cv2.imread(image_path)
        # # Save the image data to an npy file
        # npy_file_path = "path_to_save_npy_file.npy"
        # # np.save(npy_file_path, image)
        # # Load the image data from the .npy file
        # image_data = np.load(npy_file_path)
        # # Convert color channels if necessary
        # if len(image_data.shape) == 3 and image_data.shape[2] == 3:
        #     image_data = cv2.cvtColor(image_data, cv2.COLOR_BGR2RGB)
        # # Create a QImage from the image data
        # height, width, channel = image_data.shape
        # bytes_per_line = width * channel
        # qimage = QImage(image_data.data, width, height, bytes_per_line, QImage.Format_RGB888)
        # # Create a QPixmap from the QImage
        # pixmap = QPixmap.fromImage(qimage)
        # # Set the QPixmap on the QLabel to display the image
        # self.img_label.setPixmap(pixmap)
        if image_path:
            self.image_path = image_path
            self.original_image = np.load(image_path)
            self.modified_image = self.original_image.copy()
            self.display_image(self.original_image)

    def display_image(self, image):
        # Convert color channels if necessary
        if len(image.shape) == 3 and image.shape[2] == 3:
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        plt.imshow(image)
        plt.axis('off')
        # Save the plotted image temporarily
        plt.savefig("temp.png", bbox_inches='tight', pad_inches=0)
        plt.close()  # Close the figure to free up memory
        # Load the temporary image into QPixmap and set it on the QLabel
        pixmap = QPixmap("temp.png")
        self.img_label.setPixmap(pixmap)
        self.img_label.setScaledContents(True)
    
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

