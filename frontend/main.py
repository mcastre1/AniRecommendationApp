import sys
from PyQt6.QtWidgets import QApplication
from ui.MainWindow import MainWindow
from core.api import fetch_data

app = QApplication(sys.argv)

initial_data = fetch_data()
window = MainWindow(initial_data=initial_data)
window.showMaximized()

sys.exit(app.exec())