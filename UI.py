import asyncio
import json
import threading

import websockets

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
        layout.setContentsMargins(30,20,30,20)
        layout.setSpacing(15)

        self.velocidade = QLabel("0")
        self.velocidade.setAlignment(Qt.AlignCenter)
        self.velocidade.setFont(QFont("Arial",72,QFont.Bold))

        self.kmh = QLabel("km/h")
        self.kmh.setAlignment(Qt.AlignCenter)
        self.kmh.setFont(QFont("Arial",18))

        barras_layout = QHBoxLayout()
        barras_layout.setSpacing(3)

        self.barras = []

        for _ in range(self.SEGMENTOS):

            barra = QFrame()

            barra.setFixedSize(14,22)

            barra.setStyleSheet("""
                background:#222;
                border-radius:3px;
            """)

            barras_layout.addWidget(barra)

            self.barras.append(barra)

        self.rpm = QLabel("0 RPM")
        self.rpm.setAlignment(Qt.AlignCenter)
        self.rpm.setFont(QFont("Arial",22,QFont.Bold))

        layout.addStretch()

        layout.addWidget(self.velocidade)
        layout.addWidget(self.kmh)

        layout.addSpacing(10)

        layout.addLayout(barras_layout)

        layout.addWidget(self.rpm)

        layout.addStretch()

        self.atualizar.connect(self.receber)

    def receber(self, speed, rpm):

        self.velocidade.setText(str(speed))
        self.rpm.setText(f"{rpm:,} RPM".replace(",", "."))

        ligados = int((rpm / self.MAX_RPM) * self.SEGMENTOS)

        for i, barra in enumerate(self.barras):

            if i >= ligados:

                barra.setStyleSheet("""
                    background:#222;
                    border-radius:3px;
                """)

                continue

            if i < 14:

                cor = "#00ff66"

            elif i < 18:

                cor = "#ffd400"

            elif i < 21:

                cor = "#ff8800"

            else:

                cor = "#ff2020"

            barra.setStyleSheet(f"""
                background:{cor};
                border-radius:3px;
            """)

    def iniciar_ws(self):

        threading.Thread(
            target=lambda: asyncio.run(websocket(self)),
            daemon=True
        ).start()


async def websocket(dashboard):

    async with websockets.connect("ws://localhost:8765") as ws:

        while True:

            dados = json.loads(await ws.recv())

            dashboard.atualizar.emit(
                dados["speed"],
                dados["rpm"]
            )