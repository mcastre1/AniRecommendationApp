from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QSizePolicy
from PyQt6.QtCore import pyqtSignal, Qt, QThread
from widgets.ImageWorker import ImageWorker

class AnimeInfo(QWidget):
    backToMainSignal = pyqtSignal()
    likedAnimeSignal = pyqtSignal(dict)
    
    def __init__(self, data):
        super().__init__()

        self.topContainer = QWidget()
        self.topContainer.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.topLayout = QHBoxLayout()
        self.topContainer.setLayout(self.topLayout)
        self.topLayout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        
        layout = QVBoxLayout()
        
        self.centerContainer = QWidget()
        self.centerLayout = QVBoxLayout()
        self.centerContainer.setLayout(self.centerLayout)
        self.centerLayout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Start worker thread to load image
        self.thread = QThread()
        self.worker = ImageWorker(data['images']['jpg']['image_url'])
        self.worker.moveToThread(self.thread)
        
        # Listen to worker thread signals, finished and error.
        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.set_image)
        self.worker.error.connect(self.load_failed)
        
        # Cleanup thread when done
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)

        self.thread.start()
        
        self.title = QLabel(data['title'])
        self.likeButton = QPushButton("❤️")
        self.likeButton.setObjectName("likeButton")
        self.likeButton.setStyleSheet("""
            QPushButton#likeButton {
                font-size: 26px;
                background: transparent;
                border: none;
            }
            QPushButton#likeButton:hover {
                background-color: #ff4d6d;
                border-radius: 100px;
            }""")
        self.likeButton.clicked.connect(lambda: self.likedAnimeSignal.emit(data))
        
        self.description = QLabel(data['synopsis'])
        self.description.setWordWrap(True)
        
        self.backButton = QPushButton("Back to main")
        self.backButton.clicked.connect(self.backToMainSignal.emit)
        self.backButton.setStyleSheet("""
            QPushButton {
                background-color: #ffffff;
                border: none;
                padding: 10px 16px;
                border-radius: 8px;
                font-weight: bold;
                color: #000000;
            }

            QPushButton:hover {
                background-color: #f5f5f5;
            }

            QPushButton:pressed {
                background-color: #e8e8e8;
            }
        """)
        self.backButton.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

        self.topLayout.addWidget(self.backButton)
        
        self.centerLayout.addWidget(self.image_label)
        self.centerLayout.addWidget(self.title)
        self.centerLayout.addWidget(self.likeButton)
        self.centerLayout.addWidget(self.description)
        
        layout.addWidget(self.topContainer)
        layout.addWidget(self.centerContainer)
        
        self.setLayout(layout)
        
        self.setStyleSheet("""
                           background-color : #123123""")  
        
    def set_image(self, pixmap):
        scaled = pixmap.scaled(
            200, 300,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )
        self.image_label.setPixmap(scaled)
    
    def load_failed(self, msg):
        self.image_label.setText("Failed to load")