from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QSizePolicy
from PyQt6.QtCore import pyqtSignal, Qt

class AnimeInfo(QWidget):
    backToMainSignal = pyqtSignal()
    
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
        
        self.title = QLabel(data['title'])
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
        self.centerLayout.addWidget(self.title)
        self.centerLayout.addWidget(self.description)
        
        layout.addWidget(self.topContainer)
        layout.addWidget(self.centerContainer)
        
        
        self.setLayout(layout)
        
        self.setStyleSheet("""
                           background-color : #123123""")  