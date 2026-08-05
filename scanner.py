import asyncio

from websocket import iniciar, enviar


def converter_rpm(hex_string):
    partes = hex_string.split()

    if len(partes) < 4:
        return 0

    A = int(partes[2], 16)
    B = int(partes[3], 16)

    return ((A * 256) + B) // 4


def converter_speed(hex_string):
    partes = hex_string.split()

    if len(partes) < 3:
        return 0

    return int(partes[2], 16)


async def loop(connection):

    asyncio.create_task(iniciar())

    connection.connect()

    connection.send_command("ATZ")
    connection.send_command("ATE0")

    while True:

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

        await asyncio.sleep(0.5)