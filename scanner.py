import asyncio


def extrair_pid(hex_string, pid):
    partes = hex_string.replace("\r", " ").split()

    try:
        index = partes.index("41")

        if partes[index + 1].upper() != pid:
            return None

        return partes[index + 2:]

    except (ValueError, IndexError):
        return None


def converter_rpm(hex_string):
    dados = extrair_pid(hex_string, "0C")

    if not dados or len(dados) < 2:
        return 0

    A = int(dados[0], 16)
    B = int(dados[1], 16)

    return ((A * 256) + B) // 4


def converter_speed(hex_string):
    dados = extrair_pid(hex_string, "0D")

    if not dados:
        return 0

    return int(dados[0], 16)


async def loop(connection, callback):
    connection.connect()

    while True:

        rpm = converter_rpm(
            connection.send_command("010C")
        )

        speed = converter_speed(
            connection.send_command("010D")
        )

        callback(speed, rpm)

        await asyncio.sleep(0.05)