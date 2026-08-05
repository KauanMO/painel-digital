import asyncio

from websocket import iniciar, enviar


def converter_rpm(hex_string):
    partes = hex_string.split()

    try:
        index = partes.index("41")

        # PID 0C
        if partes[index + 1] != "0C":
            return 0

        A = int(partes[index + 2], 16)
        B = int(partes[index + 3], 16)

        return ((A * 256) + B) // 4

    except Exception:
        return 0



def converter_speed(hex_string):
    partes = hex_string.split()

    try:
        index = partes.index("41")

        # PID 0D
        if partes[index + 1] != "0D":
            return 0

        return int(partes[index + 2], 16)

    except Exception:
        return 0


async def loop(connection):
    connection.connect()

    connection.send_command("ATZ")
    connection.send_command("ATE0")

    while True:
        rpm_raw = connection.send_command("010C")
        speed_raw = connection.send_command("010D")

        print("RPM RAW:", repr(rpm_raw))
        print("SPEED RAW:", repr(speed_raw))

        rpm = converter_rpm(
            connection.send_command("010C")
        )

        speed = converter_speed(
            connection.send_command("010D")
        )

        print(rpm, speed)

        await enviar({
            "rpm": rpm,
            "speed": speed
        })

        await asyncio.sleep(0.1)