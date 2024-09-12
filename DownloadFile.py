import os
import urllib.request
import urllib.error
import requests
import time
import ssl
import certifi
import urllib.request

def get_name(url):
    try:
        parsed_url = urllib.parse.urlparse(url)
        filename = os.path.basename(parsed_url.path)
        return filename
    except Exception as e:
        print(f"Error getting file name: {e}")
        return "Unknown"
def get_info(url):
    try:
        ssl_context = ssl.create_default_context(cafile=certifi.where())

        response = urllib.request.urlopen(url, context=ssl_context)
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


def download_file(url, file_path, progress, max_retries=3, block_size=1024 * 1024):  # 1 Mebibyte
    try:
        file_size = 0
        if os.path.exists(file_path):
            file_size = os.path.getsize(file_path)

        headers = {}
        if file_size > 0:
            headers['Range'] = f'bytes={file_size}-'

        # Use the certifi CA bundle for SSL certificate verification
        response = requests.get(url, headers=headers, stream=True, verify=certifi.where())
        total_size = int(response.headers.get('Content-Length', 0)) + file_size
        num_blocks = total_size // block_size

        mode = 'ab' if file_size > 0 else 'wb'
        with open(file_path, mode) as file:
            for block_num in range(file_size // block_size, num_blocks):
                retries = 0
                while retries < max_retries:
                    try:
                        block = next(response.iter_content(block_size))
                        file.write(block)
                        progress(block_num, block_size, total_size)  # call progress here
                        break  # break the retry loop if successful
                    except requests.RequestException as e:
                        print(f"Error downloading block {block_num}: {e}, retrying...")
                        retries += 1
                        time.sleep(1)  # wait a bit before retrying
                else:  # if we exhausted all retries
                    print(f"Failed to download block {block_num} after {max_retries} attempts")
                    return False

        return True

    except requests.RequestException as e:
        print(f"Error initiating download: {e}")
        return False