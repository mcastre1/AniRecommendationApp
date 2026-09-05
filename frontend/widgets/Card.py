from PyQt6.QtWidgets import QPushButton, QWidget, QVBoxLayout, QLabel
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt, QThread, pyqtSignal
import requests
from widgets.ImageWorker import ImageWorker

class Card(QWidget):
    # Custom signal emitted when the widget is clicked
    clicked = pyqtSignal()
    deleteClicked = pyqtSignal(int)
    
    # We add the mousePress event and emit the pyqtSignal
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit()
        super().mousePressEvent(event)
    
    def __init__(self, id:str, title: str, images: str, deleteable: bool = False):
        super().__init__()
        #Allow this widget to use its stylesheet instead of the QGridLayout
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)

        # Class attributes    
        self.title = title
        self.id = id
        self.images = images
        self.deleteable = deleteable
        
        # Layout
        layout = QVBoxLayout()
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(8)

        # Image Label
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Start worker thread
        self.thread = QThread()
        self.worker = ImageWorker(self.images['jpg']['image_url'])
        self.worker.moveToThread(self.thread)

        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.set_image)
        self.worker.error.connect(self.load_failed)

        # Cleanup thread when done
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)

        self.thread.start()
        
        # Title Label
        self.title_label = QLabel(self.title)
        self.title_label.setWordWrap(True)
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.title_label.setStyleSheet("""
            font-size: 16px;
            font-weight: bold;
            color: #000;
        """)
        
        
        # Adding all widgets to the layout
        layout.addWidget(self.image_label)
        layout.addWidget(self.title_label)
        
        if self.deleteable:
            deleteButton = QPushButton("Delete")
            deleteButton.clicked.connect(self.deleteLikedAnime)
            deleteButton.setStyleSheet("""
                QPushButton {
                    background-color: #ff4d6d;
                    border: none;
                    padding: 8px 12px;
                    border-radius: 8px;
                    font-weight: bold;
                    color: #000000;}""")
            layout.addWidget(deleteButton)
        
        # We set the widget's layout
        self.setLayout(layout)
        
        # Setting this widget'ss style
        self.setObjectName("animeCard")

        self.setStyleSheet("""
            QWidget#animeCard {
                background: #ffffff;
                border: 1px solid #dcdcdc;
                border-radius: 10px;
            }
            QWidget#animeCard:hover {
                border: 1px solid #a0a0a0;
                background: #f7f7f7;
            }
        """)

        # Setting minimum and max width
        self.setMinimumWidth(200)
        self.setMaximumWidth(250)
        
        #Setting minimum and max height
        self.setMinimumHeight(350)
        self.setMaximumHeight(400)
        
    def set_image_from_url(self, label: QLabel, url: str):
        try:
            response = requests.get(url)
            response.raise_for_status()
            
            pixmap = QPixmap()
            pixmap.loadFromData(response.content)
            
            label.setPixmap(pixmap)
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            
        except Exception as e:
            print("Failed to load image:", e)
            
    def set_image(self, pixmap):
        scaled = pixmap.scaled(
            200, 300,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )
        self.image_label.setPixmap(scaled)

    def load_failed(self, msg):
        self.image_label.setText("Failed to load")
        

    def deleteLikedAnime(self):
        self.deleteClicked.emit(self.id)