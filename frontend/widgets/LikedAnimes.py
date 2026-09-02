from PyQt6.QtWidgets import QHBoxLayout, QPushButton, QVBoxLayout, QSizePolicy, QScrollArea, QWidget, QGridLayout
from PyQt6.QtCore import pyqtSignal, Qt

class LikedAnimes(QWidget):
    backToMainSignal = pyqtSignal()
    
    def __init__(self, liked_animes):
        super().__init__()
        
        self.liked_animes = liked_animes
        print(self.liked_animes)
        
        self.topContainer = QWidget()
        self.topContainer.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.topLayout = QHBoxLayout()
        self.topContainer.setLayout(self.topLayout)
        self.topLayout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        
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

        main_layout = QVBoxLayout()
    
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        
        content = QWidget()
        grid = QGridLayout()
        content.setLayout(grid)
        
        scroll.setWidget(content)
        
        main_layout.addWidget(self.topContainer)
        main_layout.addWidget(scroll)
        
        self.setLayout(main_layout)