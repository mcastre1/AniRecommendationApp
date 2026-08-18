from PyQt6.QtWidgets import QMainWindow

class MainWindow(QMainWindow):
    def __init__(self, initial_data):
        super().__init__()
        self.setWindowTitle('Anime Recommendation')
        print(initial_data)