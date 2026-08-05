from PySide6.QtWidgets import QApplication
import threading
import asyncio
import sys
import time

from UI import Dashboard
from scanner import loop as scanner_loop
from connection import EmulatorConnection, OBDConnection

CONNECTION_TYPE = "obd"

if CONNECTION_TYPE == "emulator":
    connection = EmulatorConnection(
        host="127.0.0.1",
        port=35000
    )
elif CONNECTION_TYPE == "obd":
    connection = OBDConnection(
        port="COM5",
        baudrate=38400
    )
else:
    raise ValueError(f"Tipo de conexão inválido: {CONNECTION_TYPE}")

def iniciar_scanner():
    asyncio.run(scanner_loop(connection))

app = QApplication(sys.argv)

dashboard = Dashboard()
dashboard.show()

threading.Thread(
    target=iniciar_scanner,
    daemon=True
).start()

time.sleep(0.5)

dashboard.iniciar_ws()

sys.exit(app.exec())