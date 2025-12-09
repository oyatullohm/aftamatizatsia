from channels.generic.websocket import AsyncJsonWebsocketConsumer

class KitchenOrderConsumer(AsyncJsonWebsocketConsumer):
    """Oshxona buyurtmalarini boshqarish uchun WebSocket consumer.
    
    Ushbu consumer ma'lum bir oshxona bo'limiga tegishli buyurtmalarni qabul qiladi va
    ularni tegishli guruhga yuboradi.
       Args:
        AsyncJsonWebsocketConsumer: Django Channels kutubxonasidan kelgan asinxron
        JSON WebSocket consumer.
    Methods:
        connect: WebSocket ulanishini qabul qiladi va guruhga qo'shadi.
        disconnect: WebSocket ulanishini uzadi va guruhdan olib tashlaydi.
        receive_json: JSON formatidagi xabarlarni qabul qiladi va guruhga yuboradi.
        order_message: Guruhdan kelgan xabarlarni WebSocket orqali yuboradi.
        send_check: Buyurtma ma'lumotlarini printerga yuborish uchun ishlatiladi.
        1-> connect(self):
        2-> disconnect(self, close_code):   
        3-> receive_json(self, content):
        4-> order_message(self, event):
        5-> send_check(self, event):
    """
    async def connect(self):
        self.department_id = self.scope["url_route"]["kwargs"]["department_id"]
        self.group_name = f"kitchen_{self.department_id}"

        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive_json(self, content):
        await self.channel_layer.group_send(
            self.group_name,
            {
                "type": "order_message",
                "message": content,
            }
        )

    async def order_message(self, event):
        await self.send_json(event["message"])

    async def send_check(self, event):
        await self.send_json({
            "order_id": event["order_id"],
            "room": event["room"],
            "client": event["client"],
            "menu_item": event["menu_item"],
            "quantity": event["quantity"],
            "printer_ip": event["printer_ip"],
            "printer_port": event["printer_port"],
            "kitchen_name": event["kitchen_name"],
        })
