# downloading_page.py
from PyQt5.QtWidgets import QDialog, QLabel, QProgressBar
from PyQt5.uic import loadUiType
import os

DownloadingPage_UI, _ = loadUiType(os.path.join(os.path.dirname(__file__), "Downloading_page.ui"))


class DownloadingPage(QDialog, DownloadingPage_UI):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        # Initialize UI elements
        self.file_name_label = self.findChild(QLabel, 'FileName2')
        self.file_size_label = self.findChild(QLabel, 'FileSize2')
        self.file_type_label = self.findChild(QLabel, 'FileType2')
        self.ProgressBar = self.findChild(QProgressBar, 'DownloadProgressBar')  # Changed to 'ProgressBar'
        self.CloseButton.clicked.connect(self.close)
        print("DownloadingPage initialized successfully.")
        self.Handle_Buttons()

    def set_file_info(self, file_name, file_size, file_type):
        self.file_name_label.setText(file_name)
        self.file_size_label.setText(file_size)
        self.file_type_label.setText(file_type)

    def Handle_Buttons(self):
        self.CloseButton.clicked.connect(self.close)

    def progress(self, file_size, total_size):
        print(f"file_size: {file_size}, total_size: {total_size}")
        if total_size > 0:
            percentage = (file_size / total_size) * 100
            print(f"percentage: {percentage}")
            self.ProgressBar.setValue(int(percentage))
        else:
            self.ProgressBar.setValue(0)
            self.file_size_label.setText("0 MB")