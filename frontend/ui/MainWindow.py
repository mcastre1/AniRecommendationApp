from PyQt6.QtWidgets import QMainWindow, QGridLayout, QWidget, QVBoxLayout, QScrollArea, QStackedWidget
from widgets.Card import Card
from widgets.AnimeInfo import AnimeInfo
from functools import partial

class MainWindow(QMainWindow):
    def __init__(self, initial_data):
        super().__init__()
        self.setWindowTitle('Anime Recommendation')
        
        self.stackedWidgets = QStackedWidget()
        
        # QMainWindow requires a centralWidget
        self.qContainer = QWidget()
        self.setCentralWidget(self.stackedWidgets)
        self.stackedWidgets.addWidget(self.qContainer)
        
        # main layout for main window
        main_layout = QVBoxLayout(self.qContainer)
        
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
        w = AnimeInfo(data)
        w.backToMainSignal.connect(self.goBack)
        self.stackedWidgets.addWidget(w)
        self.stackedWidgets.setCurrentIndex(1)
        
    def goBack(self):
        w = self.stackedWidgets.widget(1)
        self.stackedWidgets.removeWidget(w)
        w.deleteLater()
        self.stackedWidgets.setCurrentIndex(0)
        
        
        