from PyQt6.QtWidgets import QMainWindow, QGridLayout, QPushButton, QWidget, QVBoxLayout, QScrollArea, QStackedWidget, QHBoxLayout
from widgets.LikedAnimes import LikedAnimes
from widgets.Card import Card
from widgets.AnimeInfo import AnimeInfo
from widgets.Recommendations import Recommendations
from functools import partial
from PyQt6.QtGui import QAction

class MainWindow(QMainWindow):
    def __init__(self, initial_data):
        super().__init__()
        self.viewable_animes = initial_data
        self.likedAnimes = []
        self.pages = {}
        self.current_page = 1
        
        self.modifyMenuBar()
        
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
        
        # Number pages buttons on the bottom
        bottom_layout = QHBoxLayout()
        for i in range(1, 10):
            button = QPushButton(str(i))
            button.clicked.connect(partial(self.changePage, i))
            bottom_layout.addWidget(button)
        
        main_layout.addLayout(bottom_layout)
        
        # Content widget inside scroll area
        content = QWidget()
        grid = QGridLayout()
        content.setLayout(grid)
        
        scroll.setWidget(content)
        
        self.populateAnimeGrid(grid)
    
    def populateAnimeGrid(self, grid):
         # Create and add cards to the grid        
        for i, anime in enumerate(self.viewable_animes):
            widget = Card(anime['mal_id'], anime['title'], anime['images'])
            widget.clicked.connect(partial(self.showAnimeInfo, anime))
            grid.addWidget(widget, i // 5, i % 5)

    def changePage(self, page_number):
        print(f"Changing to page {page_number}")
            
    def showAnimeInfo(self, data):
        w = AnimeInfo(data)
        w.backToMainSignal.connect(self.goBack)
        w.likedAnimeSignal.connect(self.likedAnime)
        self.stackedWidgets.addWidget(w)
        self.stackedWidgets.setCurrentIndex(1)
        self.menuBar().hide()
        
    def showLikedAnimes(self):
        w = LikedAnimes(self.likedAnimes)
        w.backToMainSignal.connect(self.goBack)
        w.deleteAnimeSignal.connect(self.deleteAnimeFromLiked)
        self.stackedWidgets.addWidget(w)
        self.stackedWidgets.setCurrentIndex(1)
        self.menuBar().hide()
        
    def showRecommendations(self):
        w = Recommendations(self.likedAnimes)
        w.backToMainSignal.connect(self.goBack)
        self.stackedWidgets.addWidget(w)
        self.stackedWidgets.setCurrentIndex(1)
        self.menuBar().hide()
        
    def deleteAnimeFromLiked(self, anime_id):
        self.likedAnimes = [anime for anime in self.likedAnimes if anime['mal_id'] != anime_id]
        
    def goBack(self):
        w = self.stackedWidgets.widget(1)
        self.stackedWidgets.removeWidget(w)
        w.deleteLater()
        self.stackedWidgets.setCurrentIndex(0)
        self.menuBar().show()
        
    def likedAnime(self, data):
        if data not in self.likedAnimes:
            self.likedAnimes.append(data)
        
    def modifyMenuBar(self):
        menuBar = self.menuBar()
        menuBar.clear()
        file_menu = menuBar.addMenu("File")
        recommend_action = QAction("Recommend Animes", self)
        recommend_action.triggered.connect(lambda: self.showRecommendations())
        
        liked_action = QAction("Liked Animes", self)
        liked_action.triggered.connect(lambda: self.showLikedAnimes())
        
        self.menuBar().addAction(recommend_action)
        file_menu.addAction(liked_action)