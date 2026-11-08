
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

contador_caregar = 0
class Login_Vaion_Vision(QWidget):

    def __init__(self):
        super().__init__()

        self.Animation_execute()

    def Animation_execute(self):

        # Configurações da janela
        self.setWindowTitle("Vion Vision | Beta")
        self.setFixedSize(500, 250)
        self.setObjectName("Windos_exec")
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)

        # Layout principal (vertical)
        layout_principal = QVBoxLayout(self)
        layout_principal.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout_principal.setSpacing(1)

        # ---------------------------------
        # LOGO
        # ---------------------------------

        self.imagem = QLabel()

        caminho_imagem = (
            Path(__file__).resolve().parent
            / "img"
            / "Vaion_Vision_log.png"
        )

        self.pixmap = QPixmap(str(caminho_imagem))

        self.imagem.setPixmap(
            self.pixmap.scaled(
                370,
                200,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
        )

        self.imagem.setFixedSize(370, 200)
        self.imagem.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout_principal.addWidget(
            self.imagem,
            alignment=Qt.AlignmentFlag.AlignCenter
        )

        # Animação de opacidade da logo
        self.efeito_logo = QGraphicsOpacityEffect(self.imagem)
        self.imagem.setGraphicsEffect(self.efeito_logo)

        self.animacao_logo = QPropertyAnimation(
            self.efeito_logo,
            b"opacity"
        )

        self.animacao_logo.setDuration(1500)
        self.animacao_logo.setStartValue(0.0)
        self.animacao_logo.setEndValue(1.0)
        self.animacao_logo.setEasingCurve(
            QEasingCurve.Type.InOutCubic
        )

        self.animacao_logo.start()

        # ---------------------------------
        # LOADING - TRÊS PONTOS
        # ---------------------------------

        self.layout_loading = QHBoxLayout()
        self.layout_loading.setSpacing(2)

        self.point_load = []
        self.point_effects = []

        for i in range(4):

            point_animo = QLabel("●")

            point_animo.setStyleSheet("""
                QLabel {
                    color: #130089;
                    font-size: 22px;
                }
            """)

            point_animo.setAlignment(
                Qt.AlignmentFlag.AlignCenter
            )

            # Efeito de opacidade individual
            efeito = QGraphicsOpacityEffect(point_animo)
            point_animo.setGraphicsEffect(efeito)
            efeito.setOpacity(0.2)

            self.point_load.append(point_animo)
            self.point_effects.append(efeito)

            self.layout_loading.addWidget(point_animo)

        # Centraliza os três pontos
        layout_principal.addLayout(self.layout_loading)

        # ---------------------------------
        # ANIMAÇÃO DO LOADING
        # ---------------------------------

        self.indice = 0

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.animar_loading)
        self.timer.start(500)

        # ---------------------------------
        # ESTILO DA JANELA
        # ---------------------------------

        self.setStyleSheet("""
            QWidget#Windos_exec {
                background-color: white;
            }
        """)

    def animar_loading(self):

        # Apaga todos os pontos
        for efeito in self.point_effects:
            efeito.setOpacity(0.5)

        # Destaca o ponto atual
        self.point_effects[self.indice].setOpacity(1.0)

        # Avança para o próximo ponto
        self.indice = (self.indice + 1) % 4
        
        


app = QApplication(sys.argv)

windows = Login_Vaion_Vision()
windows.show()

sys.exit(app.exec())
