import asyncio


def extrair_pid(hex_string, pid):
    hex_string = normalizar_hex(hex_string)

    partes = hex_string.split()

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

def normalizar_hex(hex_string):
    hex_string = hex_string.replace(" ", "")
    return " ".join(
        hex_string[i:i+2]
        for i in range(0, len(hex_string), 2)
    )

async def loop(connection, callback):
    connection.connect()

    while True:

        raw_rpm = connection.send_command("010C")
        rpm = converter_rpm(raw_rpm)

        raw_speed = connection.send_command("010D")
        speed = converter_speed(raw_speed)

        print(f"raw_rpm: {raw_rpm} | raw_speed: {raw_speed}")
        print(f"rpm: {rpm} | speed: {speed}")

        callback(speed, rpm)

        await asyncio.sleep(1)