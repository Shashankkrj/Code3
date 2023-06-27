import sys
import socket
from PyQt5.QtCore import Qt, QByteArray, QTimer
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel
from your_ui_module import Ui_MainWindow  # Replace with the generated UI module name

class MyMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set up the GUI
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Create label for displaying camera data
        self.camera_label = QLabel()
        self.ui.horizontalLayout.addWidget(self.camera_label)

        # Set up TCP socket
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_address = ('127.0.0.1', 5000)  # Replace with your server address and port

        # Connect signals and slots
        self.ui.startButton.clicked.connect(self.start_receiving)
        self.ui.stopButton.clicked.connect(self.stop_receiving)

    def start_receiving(self):
        try:
            self.socket.connect(self.server_address)
            self.ui.statusLabel.setText("Receiving live camera data...")
            self.receive_data()
        except ConnectionRefusedError:
            self.ui.statusLabel.setText("Connection refused. Make sure the server is running.")
        except Exception as e:
            self.ui.statusLabel.setText(f"Error occurred: {str(e)}")

    def stop_receiving(self):
        self.socket.close()
        self.ui.statusLabel.setText("Receiving stopped.")

    def receive_data(self):
        # Set up a QTimer to continuously receive and update camera data
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_camera_data)
        self.timer.start(100)  # Adjust the interval as per your requirements

    def update_camera_data(self):
        try:
            data = self.socket.recv(1024)  # Adjust the buffer size as per your requirements
            if not data:
                return

            # Convert the received data to QImage
            image = QImage.fromData(QByteArray(data))

            # Rotate the image horizontally
            mirrored_image = image.mirrored(horizontal=True)

            # Convert QImage to QPixmap and update the camera label
            pixmap = QPixmap.fromImage(mirrored_image)
            self.camera_label.setPixmap(pixmap.scaled(self.camera_label.size(), Qt.AspectRatioMode.KeepAspectRatio))
        except Exception as e:
            self.ui.statusLabel.setText(f"Error occurred: {str(e)}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = MyMainWindow()
    mainWindow.show()
    sys.exit(app.exec_())
