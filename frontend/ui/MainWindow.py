from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QWidget
from widgets.Card import Card

class MainWindow(QMainWindow):
    def __init__(self, initial_data):
        super().__init__()
        self.setWindowTitle('Anime Recommendation')
        
        # QMainWindow requires a centralWidget
        container = QWidget()
        
        # Layout for container
        layout = QVBoxLayout(container)
        
        # We create the cards
        self.card = Card('1', 'title test', 'img test')
        
        # Add cards to the layout
        layout.addWidget(self.card)
        
        # Set the layout on container
        container.setLayout(layout)
        
        # Set container as centralwidget
        self.setCentralWidget(container)
        
        
        