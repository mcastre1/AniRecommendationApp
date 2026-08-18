from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QWidget
from widgets.Card import Card

class MainWindow(QMainWindow):
    def __init__(self, initial_data):
        super().__init__()
        self.setWindowTitle('Anime Recommendation')
        print(initial_data)
        
        container = QWidget()
        
        layout = QVBoxLayout(container)
        self.card = Card('1', 'title test', 'img test')
        layout.addWidget(self.card)
        
        container.setLayout(layout)
        self.setCentralWidget(container)
        
        
        