import sys
import os
import re

from PyQt6.QtWidgets import QApplication, QLineEdit, QMainWindow, QVBoxLayout, QWidget, QPushButton, QHBoxLayout, QFileDialog, QProgressBar, QMessageBox
from PyQt6.QtCore import QObject, QThread, pyqtSignal

from pytube import YouTube

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("YT Downloader")
        self.setFixedSize(400, 150)  # Set window size to 400x150 and disable resizing

        # Create a central widget and a layout
        central_widget = QWidget()
        main_layout = QVBoxLayout()

        # Create an input field for YouTube URL
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Enter YouTube video URL")
        self.input_field.textChanged.connect(self.validate_url)

        # Create an input field for folder path and a button to browse
        self.folder_input = QLineEdit()
        self.folder_input.setPlaceholderText("Select download folder")
        self.folder_input.setText(self.get_default_download_folder())
        self.folder_input.setReadOnly(True)  # Set read-only
        self.browse_button = QPushButton("Browse")
        self.browse_button.clicked.connect(self.browse_folder)

        # Create a horizontal layout for the folder input and browse button
        folder_layout = QHBoxLayout()
        folder_layout.addWidget(self.folder_input)
        folder_layout.addWidget(self.browse_button)

        # Create a progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(100)
        self.progress_bar.setVisible(False)  # Initially invisible

        # Create a download button
        self.download_button = QPushButton("Download")
        self.download_button.clicked.connect(self.download_button_clicked)
        # self.download_button.setStyleSheet("background-color:")
        self.download_button.setEnabled(False)

        # Add widgets to the layout
        main_layout.addWidget(self.input_field)
        main_layout.addLayout(folder_layout)
        main_layout.addWidget(self.progress_bar)  # Add progress bar above the button
        main_layout.addWidget(self.download_button)

        # Set the layout for the central widget
        central_widget.setLayout(main_layout)

        # Set the central widget of the window
        self.setCentralWidget(central_widget)

    def get_default_download_folder(self):
        if sys.platform == "win32":
            return os.path.join(os.getenv("USERPROFILE"), "Downloads")
        elif sys.platform == "darwin":
            return os.path.join(os.path.expanduser("~"), "Downloads")
        else:  # Assuming Linux or other Unix-like system
            return os.path.join(os.path.expanduser("~"), "Downloads")

    def browse_folder(self):
        folder_path = QFileDialog.getExistingDirectory(self, "Select Folder")
        if folder_path:
            self.folder_input.setText(folder_path)

    def validate_url(self):
        youtube_regex = re.compile(
            r'^(https?://)?(www\.)?(youtube|youtu|youtube-nocookie)\.(com|be)/'
            r'((watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11}))$')
        url = self.input_field.text()
        if youtube_regex.match(url):
            self.input_field.setStyleSheet("background-color: lightgreen;")
            self.download_button.setEnabled(True)
        else:
            self.input_field.setStyleSheet("background-color: lightcoral;")
            self.download_button.setEnabled(False)

    def download_button_clicked(self):
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)

        yt_url = self.input_field.text()
        output_path = self.folder_input.text()

        self.worker = YTDownloadThread(None,yt_url,output_path)
        self.worker.start()

        self.worker.progress.connect(self.evt_worker_progress)

        self.worker.finished.connect(self.evt_worker_finished)

    def evt_worker_progress(self,val):
        self.progress_bar.setValue(val)

    def evt_worker_finished(self):
        self.progress_bar.setVisible(False)
        QMessageBox.information(self,"Done","Downloaded!!")


class YTDownloadThread(QThread):
    yt_url = ""
    output_path = ""
    progress = pyqtSignal(int)

    def __init__(self, parent: QObject | None,url,output_path) -> None:
        super().__init__(parent)
        self.yt_url = url
        self.output_path = output_path
    def run(self):
        yt = YouTube(self.yt_url,on_progress_callback=self.progress_callback)
        
        yt.streams.first().download(self.output_path)

    def progress_callback(self,stream, chunk, bytes_remaining):
        total_size = stream.filesize
        bytes_downloaded = total_size - bytes_remaining
        pct_completed = bytes_downloaded / total_size * 100
        print(pct_completed)
        self.progress.emit(int(pct_completed))
    
app = QApplication(sys.argv)

window = MainWindow()
window.show()

sys.exit(app.exec())
