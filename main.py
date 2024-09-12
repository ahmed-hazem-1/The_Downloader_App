# main.py is the main file that contains the main application logic.

import os
import sys
from urllib.parse import urlparse

from PyQt5.uic import loadUiType
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog, QMessageBox
from pip._internal.utils.filesystem import file_size

import DownloadFile
import downloading_page

from downloading_page import DownloadingPage

FORM_CLASS, _ = loadUiType(os.path.join(os.path.dirname(__file__), "main.ui"))


class MainApp(QMainWindow, FORM_CLASS):
    def __init__(self, parent=None):
        super(MainApp, self).__init__(parent)
        self.full_save_path = None
        self.downloading_page = None
        self.setupUi(self)
        self.Fixed_UI()
        self.Handle_Buttons()


    def Fixed_UI(self):
        self.setWindowTitle("The Downloader")
        self.setFixedSize(900, 720)

    def Browse_Button_File(self):
        initial_filename = self.lineEdit.text() if self.lineEdit.text() else "untitled"
        file_path, _ = QFileDialog.getSaveFileName(self, "Save File", initial_filename, "All Files (*)")
        if file_path:
            self.full_save_path = file_path
            self.SaveLocation.setText(os.path.basename(file_path))

    def Handle_Buttons(self):
        self.BrowseButton.clicked.connect(self.Browse_Button_File)
        self.DownloadButton.clicked.connect(self.Download_File)
        self.lineEdit.textChanged.connect(self.update_file_info)

    def update_file_info(self):
        url = self.lineEdit.text()
        if not url:
            self.FileSize.setText("Size: Unknown")
            self.MimeType.setText("Type: Unknown")
            return

        # Fetch file info
        mime_type, File_size = DownloadFile.get_info(url)

        # Update the UI with the file info
        self.FileType.setText(f" {mime_type}")
        self.FileSize.setText(f" {File_size}")
        self.SaveLocation.setText(f" {self.extract_filename_from_url(url)}")




    def extract_filename_from_url(self, url):  # Added 'self' here
        parsed_url = urlparse(url)
        filename = os.path.basename(parsed_url.path)
        return filename

    def Download_File(self):
        url = self.lineEdit.text()
        if not url:
            self.show_error_message("Please enter a valid URL.")
            return
        else:

            file_path = self.full_save_path
            downloading_page_2 = DownloadingPage(self)
            downloading_page_2.show()
            success = DownloadFile.download_file(url, file_path, downloading_page_2.progress)  # Corrected here
            if success:
                QMessageBox.information(self, "Download Complete", "The file has been downloaded successfully.")
            else:
                QMessageBox.critical(self, "Download Failed", "The file could not be downloaded.")


def main():
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
