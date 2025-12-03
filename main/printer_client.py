import asyncio
import websockets
import json
from escpos.printer import Network

async def listen():
    uri = "ws://yourserver.com/ws/printer/"

    while True:
        try:
            async with websockets.connect(uri) as websocket:
                print("Connected to server...")

                while True:
                    msg = await websocket.recv()
                    data = json.loads(msg)

                    printer_ip = data["printer_ip"]
                    printer_port = data["printer_port"]

                    p = Network(printer_ip, printer_port)

                    p.text("----- YANGI BUYURTMA -----\n")
                    p.text(f"Buyurtma ID: {data['order_id']}\n")
                    p.text(f"Xona: {data['room']}\n")
                    p.text(f"Taom: {data['menu_item']}\n")
                    p.text(f"Soni: {data['quantity']}\n")
                    p.text(f"Oshxona: {data['kitchen_name']}\n")
                    p.text("---------------------------\n")
                    p.cut()

        except Exception as e:
            print("Xato:", e)
            await asyncio.sleep(3)

asyncio.run(listen())
