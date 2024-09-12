# downloading_page.py
from PyQt5.QtWidgets import QDialog, QLabel, QProgressBar
from PyQt5.uic import loadUiType
import os

DownloadingPage_UI, _ = loadUiType(os.path.join(os.path.dirname(__file__), "Downloading page.ui"))


class DownloadingPage(QDialog, DownloadingPage_UI):
    def __init__(self, parent=None):
        super(DownloadingPage, self).__init__(parent)
        try:
            self.setupUi(self)
            # Initialize UI elements
            self.file_name_label = self.findChild(QLabel, 'FileName')
            self.file_size_label = self.findChild(QLabel, 'FileSize')
            self.progress_bar = self.findChild(QProgressBar, 'progress_bar')
            self.CloseButton.clicked.connect(self.close)
            print("DownloadingPage initialized successfully.")
        except Exception as e:
            print(f"Error initializing DownloadingPage: {e}")

    def progress(self, block_num, block_size, total_size):
        downloaded = block_num * block_size
        if total_size > 0:
            percentage = downloaded * 100 / total_size
            self.progress_bar.setValue(int(percentage))
        else:
            self.progress_bar.setValue(0)
