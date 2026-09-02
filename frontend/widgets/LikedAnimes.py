from PyQt6.QtWidgets import QVBoxLayout, QScrollArea, QWidget, QGridLayout

class LikedAnimes:
    def __init__(self, liked_animes):
        super().__init__()
        
        self.liked_animes = liked_animes
        
        main_layout = QVBoxLayout()
    
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        
        content = QWidget()
        grid = QGridLayout()
        content.setLayout(grid)
        
        scroll.setWidget(content)
        
        main_layout.addWidget(scroll)