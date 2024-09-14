import os
from urllib.parse import urlparse

from PyQt5.QtCore import QThread

import DownloadFile


def extract_filename_from_url(url):  # Added 'self' here
    parsed_url = urlparse(url)
    filename = os.path.basename(parsed_url.path)
    return filename
class DownloadThread(QThread):
    def __init__(self, url, file_path, progress):
        super().__init__()
        self.url = url
        self.file_path = file_path
        self.progress = progress

    def run(self):
        DownloadFile.download_file(self.url, self.file_path, self.progress)

