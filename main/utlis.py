from escpos.printer import Network
from .models import OrderItem
def print_kitchen_check(list):
    for order_item in list:
        menu = order_item.menu_item
        dept = menu.kitchen

        if not dept:
            return  # printer yo‘q

        printer = Network(dept.printer_ip, dept.printer_port)

        printer.text(f"--- Yangi Buyurtma ---\n")
        printer.text(f"Taom: {menu.name}\n")
        printer.text(f"Miqdor: {order_item.quantity}\n")
        printer.text(f"Buyurtma ID: {order_item.order.id}\n")
        printer.text(f"Hona: {order_item.order.room.name}\n")
        printer.text("----------------------\n")
        printer.cut()

        order_item.printed = True
        order_item.save()
