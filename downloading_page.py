# downloading_page.py
from PyQt5.QtWidgets import QDialog, QLabel, QProgressBar
from PyQt5.uic import loadUiType
import os


DownloadingPage_UI, _ = loadUiType(os.path.join(os.path.dirname(__file__), "Downloading_page.ui"))


class DownloadingPage(QDialog, DownloadingPage_UI):
    def __init__(self, parent=None):
        super().__init__(parent)
        try:
            self.setupUi(self)
            # Initialize UI elements
            self.file_name_label = self.findChild(QLabel, 'FileName_2')
            self.file_name_label.setText(f" Ahmed Hazem")
            self.file_size_label = self.findChild(QLabel, 'FileSize2')
            self.file_type_label = self.findChild(QLabel, 'FileType2')

            self.ProgressBar = self.findChild(QProgressBar, 'ProgressBar')  # Changed to 'ProgressBar'
            self.CloseButton.clicked.connect(self.close)
            print("DownloadingPage initialized successfully.")
        except Exception as e:
            print(f"Error initializing DownloadingPage: {e}")

    def progress(self, block_num, block_size, total_size):
        downloaded = block_num * block_size
        print(f"block_num: {block_num}, block_size: {block_size}, total_size: {total_size}, downloaded: {downloaded}")
        if total_size > 0:
            percentage = downloaded * 100 / total_size
            print(f"percentage: {percentage}")
            self.ProgressBar.setValue(int(percentage))  # Changed to 'ProgressBar'
            self.file_size_label.setText(f"{total_size / (1024 * 1024):.2f} MB")  # Update file size label
        else:
            self.ProgressBar.setValue(0)  # Changed to 'ProgressBar'
            self.file_size_label.setText("0 MB")  # Update file size label