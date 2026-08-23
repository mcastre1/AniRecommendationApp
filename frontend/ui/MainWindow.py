from PyQt6.QtWidgets import QMainWindow, QGridLayout, QWidget, QVBoxLayout, QScrollArea
from widgets.Card import Card
from widgets.AnimeInfo import AnimeInfo
from functools import partial

class MainWindow(QMainWindow):
    def __init__(self, initial_data):
        super().__init__()
        self.setWindowTitle('Anime Recommendation')
        
        # QMainWindow requires a centralWidget
        container = QWidget()
        self.setCentralWidget(container)
        
        # main layout for main window
        main_layout = QVBoxLayout(container)
        
        # Scroll Area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        main_layout.addWidget(scroll)
        
        # Content widget inside scroll area
        content = QWidget()
        grid = QGridLayout()
        content.setLayout(grid)
        
        scroll.setWidget(content)
        
        # Create and add cards to the grid        
        for i, anime in enumerate(initial_data):
            widget = Card(anime['mal_id'], anime['title'], anime['images'])
            widget.clicked.connect(partial(self.showAnimeInfo,'Hello World'))
            grid.addWidget(widget, i // 5, i % 5)
            
    def showAnimeInfo(self, data):
        self.w = AnimeInfo(data)
        self.w.show()
        
        