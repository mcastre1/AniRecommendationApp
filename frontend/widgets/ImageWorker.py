from PyQt6.QtCore import QObject, pyqtSignal
from PyQt6.QtGui import QPixmap
import requests

class ImageWorker(QObject):
    finished = pyqtSignal(QPixmap)
    error = pyqtSignal(str)

    def __init__(self, url):
        super().__init__()
        self.url = url

    def run(self):
        try:
            response = requests.get(self.url)
            response.raise_for_status()

            pixmap = QPixmap()
            pixmap.loadFromData(response.content)

            self.finished.emit(pixmap)

        except Exception as e:
            self.error.emit(str(e))