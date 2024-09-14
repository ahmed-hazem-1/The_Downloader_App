

# 🛠️ The Downloader APP

**The Downloader Manager** is a PyQt-based desktop application designed to simplify the process of downloading files from the internet. With a clean and intuitive interface, users can effortlessly retrieve detailed file information before initiating a download. The app is also being extended to support YouTube video and playlist downloads.

## ✨ Features

- 🔄 **General File Downloader**: Download any file from a valid URL.
- 📄 **File Information Retrieval**: Get file type and size before downloading.
- 🎥 **YouTube Integration (Planned)**: Download YouTube videos and playlists.
- 💻 **User-Friendly Interface**: Clean and simple UI built with PyQt5.

## 🛠️ Installation

### Prerequisites

- **Python 3.12.6** or later
- **PyQt5**: Python bindings for the Qt application framework.
- **Requests**: Simple HTTP library for Python.

### Install Dependencies

First, ensure you have the required Python packages:

```bash
pip install PyQt5 requests
```

### Clone the Repository

```bash
git clone (https://github.com/ahmed-hazem-1/The_Downloader_App.git)
cd The_Downloader_App
```

## 🚀 Usage

### Running the Application

To start the application, navigate to the project directory and run:

```bash
py -3 main.py
```

### Main Features

1. **🔗 Enter URL**: Paste the URL of the file you want to download.
2. **🔍 Fetch File Info**: The app will automatically fetch and display the file type and size.
3. **💾 Browse Save Location**: Click the "Browse" button to select where you want to save the file.
4. **⬇️ Download**: Click the "Download" button to start the download process.

### File Information Display

Upon entering a valid URL, the application displays:

- **📂 File Type**: The MIME type of the file.
- **📏 File Size**: The size of the file in MB.

### Planned Features

- **🎬 YouTube Video/Playlist Downloader**: Download videos or playlists from YouTube.
- **⚙️ Advanced Error Handling**: Comprehensive error messages and troubleshooting tips.

## 📁 Project Structure

```
downloader-manager/
│
├── main.py                  # Main application logic
├── downloader.py            # Download logic
├── downloading_page.py      # Downloading page UI management
├── url_handler.py           # URL validation and file info retrieval
├── utils.py                 # Utility functions
├── main.ui                  # Main UI layout file
├── README.md                # Project documentation (this file)
└── requirements.txt         # List of dependencies
```

## 🤝 Contributing

We welcome contributions! If you'd like to help, please submit a pull request or open an issue to discuss your ideas.

### How to Contribute

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes.
4. Commit your changes (`git commit -m 'Add some feature'`).
5. Push to the branch (`git push origin feature-branch`).
6. Open a pull request.

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📧 Contact

For questions or further assistance, feel free to reach out:

- **Email**: ahmed453189@fci.bu.edu.eg
- **GitHub**: [Ahmed Hazem](https://github.com/ahmed-hazem-1)


