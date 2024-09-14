import logging
import sys
from datetime import timedelta
from PyQt5.QtCore import pyqtSignal, QThread

import yt_dlp
from PyQt5.QtWidgets import QDialog, QLabel, QFileDialog, QMessageBox, QWidget
from PyQt5.uic import loadUiType
import os

import downloading_page
from utils import convert_size
# from main import MainApp
import re

YV_UI, _ = loadUiType(os.path.join(os.path.dirname(__file__), "YV.ui"))

import utils


def format_quality_info(fmt, size):
    """
    Formats quality and size information for a given format.

    Args:
        fmt (dict): Format dictionary containing format details.
        size (int or None): Size of the format in bytes.

    Returns:
        str or None: Formatted quality information or None if no size is provided.
    """
    quality = fmt.get('format_note', 'Unknown Quality')
    ext_type = fmt.get('ext', 'Unknown Extension')

    if size is not None:
        size, size_type = convert_size(size)
        return f"{quality} ({size} {size_type}) ({ext_type})"
    return None


def extract_qualities(formats):
    """
    Extracts video and audio qualities from the list of formats.

    Args:
        formats (list): List of format dictionaries.

    Returns:
        tuple: Two lists containing video/audio qualities and their format IDs.
    """
    video_audio_qualities = []
    audio_qualities = []

    for fmt in formats:
        ext_type = fmt.get('ext')
        size = fmt.get('filesize')
        quality_size = format_quality_info(fmt, size)

        # Format with both video and audio
        if quality_size and ext_type == 'mp4':
            quality_format_id = (quality_size, f'{fmt.get('format_id')} + bestaudio/best')
            if quality_format_id not in video_audio_qualities:
                video_audio_qualities.append(quality_format_id)

        # Format with audio only
        if fmt.get('acodec') != 'none' and fmt.get('vcodec') == 'none':
            if quality_size:  # Check if quality_size is not None before appending
                quality_format_id = (quality_size, fmt.get('format_id'))
                if quality_format_id not in audio_qualities:
                    audio_qualities.append(quality_format_id)

    return video_audio_qualities, audio_qualities


class YVideo_DownloadThread(QThread):
    def __init__(self, url, ydl_opts):
        super().__init__()
        self.url = url
        self.ydl_opts = ydl_opts

    def run(self):
        with yt_dlp.YoutubeDL(self.ydl_opts) as ydl:
            ydl.download(self.url)  # Pass the URL as a list to download


class YVideo(QDialog, YV_UI):
    download_progress = pyqtSignal(int, int)  # Signal to emit download progress

    def __init__(self, parent=None):
        super().__init__(parent)  # Corrected super() call to initialize both QDialog and YV_UI
        self.percent = 0
        self.full_save_path = None
        self.Video_Title = None
        self.url = None
        self.FileSize = None
        self.FileType = None
        self.progress = None
        try:
            self.setupUi(self)
            self.file_name_label = self.findChild(QLabel, 'FileType_2')
            self.file_duration_label = self.findChild(QLabel, 'FileType_3')
            self.Handel_Buttons()

            # Initialize UI elements
            # self.file_size_label = self.findChild(QLabel, 'FileSize_2')

            print("YV_UI initialized successfully.")
        except Exception as e:
            print(f"Error initializing YV_UI: {e}")

    def get_video_info(self, Url):
        video_info = yt_dlp.YoutubeDL().extract_info(Url, download=False)
        self.Video_Title = video_info.get('title', 'Video Title')
        self.SaveLocationYV.setText(self.Video_Title)

        Video_Duration = video_info.get('duration', 0)
        Video_Duration = str(timedelta(seconds=Video_Duration))

        self.file_name_label.setText(self.Video_Title)
        self.file_duration_label.setText(str(Video_Duration))

        formats = video_info.get('formats', [])
        video_audio_qualities, audio_qualities = extract_qualities(formats)

        # Sort the qualities
        video_audio_qualities.sort(key=lambda x: int(re.search(r'\d+', x[0]).group()))
        audio_qualities.sort(key=lambda x: int(re.search(r'\d+', x[0]).group()))

        # Add the qualities to the QualityBox
        self.QualityBox.clear()  # Clear previous entries
        for quality_size, format_id in video_audio_qualities:
            self.QualityBox.addItem(quality_size, format_id)
        for quality_size, format_id in audio_qualities:
            self.QualityBox.addItem(quality_size, format_id)

    def Handel_Buttons(self):
        self.BrowseButtonYV.clicked.connect(self.Browse_Button_YV)
        self.DownloadYoutubeVideo.clicked.connect(self.Download_Youtube_Video)
        self.pushButton_3.clicked.connect(self.close)

    def Browse_Button_YV(self):
        print("Browse button clicked")
        initial_filename = self.Video_Title if self.Video_Title else "untitled"
        file_path, _ = QFileDialog.getSaveFileName(self, "Save File", initial_filename, "All Files (*)")
        if file_path:
            self.full_save_path = file_path
            self.SaveLocationYV.setText(self.full_save_path)

    def progress_hook(self, progress):
        if progress['status'] == 'downloading':
            downloaded_bytes = int(progress.get('downloaded_bytes', 0))
            total_bytes = int(progress.get('total_bytes', 0))
            self.percent = progress.get('percent', 0)
            print(f"Downloaded {downloaded_bytes} of {total_bytes} bytes ({self.percent}%)")
            self.download_progress.emit(downloaded_bytes, total_bytes)  # Emit signal with download progress

    def Download_Youtube_Video(self):
        url = self.lineEdit2.text()  # Get the URL input
        output_path = self.full_save_path  # Get the full path where the file should be saved

        selected_quality = self.QualityBox.currentText()  # Get the selected quality text from the combo box
        self.FileSize = selected_quality.split('(')[1].split(' ')[0]
        self.FileType = selected_quality.split('(')[2].split(')')[0]
        formatted = self.QualityBox.currentData()
        utils.show_downloading_page(self, url, self.FileSize, self.FileType, self.Video_Title, self.percent)
        if formatted is None:
            print("Error: Selected quality not found!")
            return

        ydl_opts = {
            'quiet': True,
            'format': formatted,  # Set the format to the selected quality
            'outtmpl': output_path + '.%(ext)s',
            'retries': 10,
            'progress_hooks': [self.progress_hook],
            'socket_timeout': 30,
            'nocheckcertificate': True,  # Sometimes helps with download issues
        }


        self.download_thread = YVideo_DownloadThread(url, ydl_opts)
        self.download_progress.connect(self.downloading_page_2.progress)  # Connect signal to progress function
        self.download_thread.finished.connect(self.on_download_finished)  # Connect finished signal to on_download_finished function
        self.download_thread.start()


def main():
    app = QWidget(sys.argv)
    window = YVideo()
    window.show()
    sys.exit(app.exec_())
