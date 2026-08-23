from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel

class AnimeInfo(QWidget):
    def __init__(self, data):
        super().__init__()
        layout = QVBoxLayout()
        self.label = QLabel("test label")
        layout.addWidget(self.label)
        
        print(data)    