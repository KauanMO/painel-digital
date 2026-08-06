from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QFrame
)

class Dashboard(QWidget):
    atualizar = Signal(int, int)

    MAX_RPM = 8000
    SEGMENTOS = 24

    STYLE_OFF = """
        background:#222;
        border-radius:3px;
    """

    STYLE_GREEN = """
        background:#00ff66;
        border-radius:3px;
    """

    STYLE_YELLOW = """
        background:#ffd400;
        border-radius:3px;
    """

    STYLE_ORANGE = """
        background:#ff8800;
        border-radius:3px;
    """

    STYLE_RED = """
        background:#ff2020;
        border-radius:3px;
    """

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Dashboard")
        self.setFixedSize(480, 320)

        self.setStyleSheet("""
            QWidget{
                background:#090909;
                color:white;
            }
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 20, 30, 20)
        layout.setSpacing(15)

        self.velocidade = QLabel("0")
        self.velocidade.setAlignment(Qt.AlignCenter)
        self.velocidade.setFont(QFont("Arial", 72, QFont.Bold))

        self.kmh = QLabel("km/h")
        self.kmh.setAlignment(Qt.AlignCenter)
        self.kmh.setFont(QFont("Arial", 18))

        barras_layout = QHBoxLayout()
        barras_layout.setSpacing(3)

        self.barras = []
        self.estado_barras = []

        for _ in range(self.SEGMENTOS):

            barra = QFrame()
            barra.setFixedSize(14, 22)
            barra.setStyleSheet(self.STYLE_OFF)

            barras_layout.addWidget(barra)

            self.barras.append(barra)
            self.estado_barras.append(self.STYLE_OFF)

        self.rpm = QLabel("0 RPM")
        self.rpm.setAlignment(Qt.AlignCenter)
        self.rpm.setFont(QFont("Arial", 22, QFont.Bold))

        layout.addStretch()

        layout.addWidget(self.velocidade)
        layout.addWidget(self.kmh)

        layout.addSpacing(10)

        layout.addLayout(barras_layout)

        layout.addWidget(self.rpm)

        layout.addStretch()

        self.ultimo_speed = None
        self.ultimo_rpm = None

        self.atualizar.connect(self.receber)

    def receber(self, speed, rpm):
        if speed == self.ultimo_speed and rpm == self.ultimo_rpm:
            return

        self.ultimo_speed = speed
        self.ultimo_rpm = rpm

        self.velocidade.setText(str(speed))
        self.rpm.setText(f"{rpm:,} RPM".replace(",", "."))

        ligados = int((rpm / self.MAX_RPM) * self.SEGMENTOS)
        ligados = max(0, min(ligados, self.SEGMENTOS))

        for i, barra in enumerate(self.barras):

            if i >= ligados:
                estilo = self.STYLE_OFF

            elif i < 14:
                estilo = self.STYLE_GREEN

            elif i < 18:
                estilo = self.STYLE_YELLOW

            elif i < 21:
                estilo = self.STYLE_ORANGE

            else:
                estilo = self.STYLE_RED

            if estilo != self.estado_barras[i]:
                barra.setStyleSheet(estilo)
                self.estado_barras[i] = estilo