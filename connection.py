import socket
import serial
import time

class EmulatorConnection:
    def __init__(self, host="127.0.0.1", port=35000):
        self.host = host
        self.port = port
        self.sock = None

    def connect(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.host, self.port))


    def send_command(self, command):
        self.serial.write((command + "\r").encode())

        time.sleep(0.1)

        resposta = bytearray()

        while True:
            b = self.serial.read(1)

            if not b:
                break

            if b == b">":
                break

            resposta.extend(b)

        return resposta.decode(errors="ignore").strip()

    def close(self):
        if self.sock:
            self.sock.close()

class OBDConnection:
    def __init__(self, port="COM5", baudrate=38400):
        self.port = port
        self.baudrate = baudrate
        self.serial = None

    def connect(self):
        self.serial = serial.Serial(
            self.port,
            baudrate=self.baudrate,
            timeout=1
        )
        
        self.send_command("ATZ")
        self.send_command("ATE0")
        self.send_command("ATL0")
        self.send_command("ATS0")
        self.send_command("ATH0")

    def send_command(self, command):
        self.serial.reset_input_buffer()

        self.serial.write((command + "\r").encode())

        resposta = bytearray()

        while True:
            b = self.serial.read(1)

            if not b:
                break

            if b == b">":
                break

            resposta.extend(b)

        return resposta.decode(errors="ignore").strip()

    def close(self):
        if self.serial:
            self.serial.close()