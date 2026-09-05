from PyQt6.QtWidgets import QHBoxLayout, QPushButton, QVBoxLayout, QSizePolicy, QScrollArea, QWidget, QGridLayout
from PyQt6.QtCore import pyqtSignal, Qt

from widgets.Card import Card

class LikedAnimes(QWidget):
    backToMainSignal = pyqtSignal()
    deleteAnimeSignal = pyqtSignal(int)
    
    def __init__(self, liked_animes):
        super().__init__()
        
        self.liked_animes = liked_animes
        print(len(self.liked_animes))
        
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
        self.grid = QGridLayout()
        content.setLayout(self.grid)
        
        scroll.setWidget(content)
        
        main_layout.addWidget(self.topContainer)
        main_layout.addWidget(scroll)
        
        self.populateAnimeGrid(self.grid)
        self.setLayout(main_layout)
        
    def populateAnimeGrid(self, grid):
        for i, anime in enumerate(self.liked_animes):
            widget = Card(anime['mal_id'], anime['title'], anime['images'], deleteable=True)
            widget.deleteClicked.connect(self.deleteAnimeFromLiked)
            grid.addWidget(widget, i // 5, i % 5)
            
    def deleteAnimeFromLiked(self, anime_id):
        self.liked_animes = [anime for anime in self.liked_animes if anime['mal_id'] != anime_id]
        self.deleteAnimeSignal.emit(anime_id)
        self.clearGrid()  # Clear the grid layout
        self.populateAnimeGrid(self.grid)  # Repopulate the grid with the updated list
        print(f"Deleted anime with ID: {anime_id}. Remaining liked animes: {len(self.liked_animes)}")
        
    def clearGrid(self):
        while self.grid.count():
            item = self.grid.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()