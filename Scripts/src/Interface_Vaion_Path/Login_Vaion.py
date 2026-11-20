import sys
from pathlib import Path

from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QGraphicsOpacityEffect
)

from PySide6.QtGui import QPixmap
from PySide6.QtCore import (
    QPropertyAnimation,
    QEasingCurve,
    Qt,
    QTimer
)

class Interface_Vaion_Vision(QWidget):
    def __init__(self):
        super().__init__()
        self.Login_Vaion_Vision()
    def Login_Vaion_Vision(self):
        self.setWindowTitle("Login | Beta")
        self.setObjectName("Vaion_Login")
        self.setMinimumWidth(1000)
        self.setMinimumHeight(700)

        layout = QHBoxLayout(self)
        self.box_info = QWidget()
        self.box_info.setObjectName("box_info")

        self.log_vaion = QWidget()
        self.log_vaion.setObjectName("log_vaion")

        self.box_info.setStyleSheet("""
            QWidget#box_info{
                background-color:#25213B ;
            }
        """)
        


        layout.addWidget(self.box_info)
        self.log_vaion.setStyleSheet("""
            QWidget#log_vaion{
                background-color:red;
            }
        """)
        self.l
        layout.addWidget(self.log_vaion)

        layout.setStretch(0,0)
        layout.setStretch(1,0)
app = QApplication()
windows = Interface_Vaion_Vision()
windows.show()
sys.exit(app.exec())