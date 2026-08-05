import asyncio
import json
import websockets

clientes = set()

async def handler(ws):
    clientes.add(ws)
    print("Cliente conectado")

    try:
        await ws.wait_closed()
    finally:
        clientes.remove(ws)
        print("Cliente desconectado")


async def enviar(dados):
    if not clientes:
        return

    mensagem = json.dumps(dados)

    await asyncio.gather(
        *(cliente.send(mensagem) for cliente in clientes)
    )


async def iniciar():
    servidor = await websockets.serve(handler, "localhost", 8765)

    print("WebSocket iniciado")

    await servidor.wait_closed()