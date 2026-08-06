from PySide6.QtWidgets import QApplication
import threading
import asyncio
import sys

from UI import Dashboard
from scanner import loop as scanner_loop
from connection import EmulatorConnection, OBDConnection

CONNECTION_TYPE = "emulator"

if CONNECTION_TYPE == "emulator":
    connection = EmulatorConnection(
        host="127.0.0.1",
        port=35000
    )

elif CONNECTION_TYPE == "obd":
    connection = OBDConnection(
        port="COM8",
        baudrate=38400
    )

else:
    raise ValueError("Tipo de conexão inválido")

app = QApplication(sys.argv)

dashboard = Dashboard()
dashboard.show()

def iniciar_scanner():

    asyncio.run(
        scanner_loop(
            connection,
            lambda speed, rpm: dashboard.atualizar.emit(speed, rpm)
        )
    )

threading.Thread(
    target=iniciar_scanner,
    daemon=True
).start()

sys.exit(app.exec())