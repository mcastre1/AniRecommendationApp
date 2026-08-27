from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PyQt6.QtCore import pyqtSignal

class AnimeInfo(QWidget):
    backToMainSignal = pyqtSignal()
    
    def __init__(self, data):
        super().__init__()

        
        layout = QVBoxLayout()
        self.label = QLabel("test label")
        
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

        
        layout.addWidget(self.backButton)
        layout.addWidget(self.label)
        self.setLayout(layout)
        
        self.setStyleSheet("""
                           background-color : #123123""")  