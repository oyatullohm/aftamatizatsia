from django.db.models.signals import post_save
from django.dispatch import receiver
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .models import OrderItem

@receiver(post_save, sender=OrderItem)
def notify_new_order_item(sender, instance, created, **kwargs):
    if not created:
        return

    kitchen = instance.menu_item.kitchen
    order = instance.order
    chayhona = order.chayhona

    if not kitchen:
        # Menu item oshxonaga biriktirilmagan bo‘lsa xabar yubormaymiz
        return

    channel_layer = get_channel_layer()

    group_name = f"printer_group_{chayhona.id}_{kitchen.id}"

    async_to_sync(channel_layer.group_send)(
        group_name,
        {
            "type": "send_check",

            # Order maʼlumotlari
            "order_id": order.id,
            "room": order.room.name if order.room else "",
            "client": order.client_name,

            # Menu item maʼlumotlari
            "menu_item": instance.menu_item.name,
            "quantity": float(instance.quantity),

            # Printer maʼlumotlari
            "printer_ip": kitchen.printer_ip,
            "printer_port": kitchen.printer_port,

            # Oshxona bo‘limi nomi
            "kitchen_name": kitchen.name,
        }
    )
