import urllib.request
import urllib.error
import requests


def get_info(url):
    try:
        response = urllib.request.urlopen(url)
        mime_type = response.headers.get('Content-Type', 'Unknown')
        File_size = response.headers.get('Content-Length', None)
        if File_size is not None:
            file_size = int(File_size)
            file_size_mb = file_size / (1024 * 1024)
            file_size = f"{file_size_mb:.2f} MB"
        else:
            file_size = "Unknown"

        return mime_type, file_size

    except urllib.error.URLError as e:
        print(f"Error getting file info: {e}")
        return "Unknown", "Unknown"


def download_file(url, file_path, progress_callback):
    try:
        response = requests.get(url, stream=True)
        total_size = int(response.headers.get('Content-Length', 0))
        block_size = 1024  # 1 Kibibyte
        num_blocks = total_size // block_size

        with open(file_path, 'wb') as file:
            for block_num, block in enumerate(response.iter_content(block_size), 1):
                file.write(block)
                progress_callback(block_num, block_size, total_size)

        return True

    except requests.RequestException as e:
        print(f"Error downloading file: {e}")
        return False
