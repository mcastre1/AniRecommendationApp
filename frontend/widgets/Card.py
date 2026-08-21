from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt
import requests

class Card(QWidget):
    def __init__(self, id:str, title: str, images: str):
        super().__init__()
        
        # Class attributes    
        self.title = title
        self.id = id
        self.images = images
        
        # Layout
        layout = QVBoxLayout()
        layout.setContentsMargins(12,12,12,12) # Margins from all sides
        layout.setSpacing(5)

        # Image Label
        self.image_label = QLabel()
        
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
        
        
        # We set the widget's layout
        self.setLayout(layout)
        
        # Setting this widget'ss style
        self.setStyleSheet("""
            QWidget {
                background: #ffffff;
                border: 1px solid #dcdcdc;
                border-radius: 10px;
            }
            QWidget:hover {
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
        
        if self.images:
            self.set_image_from_url(self.image_label, images['jpg']['image_url'])
        
        
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