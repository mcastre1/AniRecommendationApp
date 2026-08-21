from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt

class Card(QWidget):
    def __init__(self, id:str, title: str, img: str):
        super().__init__()
        
        # Class attributes    
        self.title = title
        self.id = id
        self.img = img
        
        # Layout
        layout = QVBoxLayout()
        layout.setContentsMargins(12,12,12,12) # Margins from all sides
        layout.setSpacing(5)

        
        # Title Label
        self.title_label = QLabel(self.title)
        self.title_label.setWordWrap(True)
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.title_label.setStyleSheet("""
            font-size: 16px;
            font-weight: bold;
            color: #000;
        """)
        
        
        # Adding all widgets to the layout
        layout.addWidget(self.title_label)
        
        # We set the widget's layout
        self.setLayout(layout)
        
        # Setting this widget'ss style
        self.setStyleSheet("""
            QWidget {
                background: #ffffff;
                border: 1px solid #dcdcdc;
                border-radius: 10px;
            }
            QWidget:hover {
                border: 1px solid #a0a0a0;
                background: #f7f7f7;
            }
        """)
        
        # Setting minimum and max width
        self.setMinimumWidth(200)
        self.setMaximumWidth(250)
        
        #Setting minimum and max height
        self.setMinimumHeight(350)
        self.setMaximumHeight(400)