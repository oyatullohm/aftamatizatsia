from django.contrib.auth.models import AbstractUser
from django.db import models
import random

def generate_uid():
    return random.randint(1000000000, 9999999999)


class Chayhana(models.Model):
    uid = models.BigIntegerField(unique=True, default=generate_uid)
    name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name

class CustomUser(AbstractUser):
    chayhana = models.ForeignKey(Chayhana, on_delete=models.CASCADE,null=True,blank=True) 
    phone = models.CharField(max_length=13)
    role = models.CharField(max_length=50, default='ofisiant')  # ofisiant, admin, oshpaz, boshqaruvchi
    def __str__(self):
        return f"{self.username}"

class Room(models.Model):
    chayhana = models.ForeignKey(Chayhana, on_delete=models.CASCADE) 
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=14, decimal_places=0)
    price_service = models.DecimalField(max_digits=14, decimal_places=0, default=0)
    service_percentage = models.BooleanField(default=False)
    disciription = models.CharField(max_length=150, null=True, blank=True)
    def __str__(self):
        return self.name

class KitchenDepartment(models.Model):
    chayhana = models.ForeignKey(Chayhana, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    printer_ip = models.GenericIPAddressField()  # printer IP manzili
    printer_port = models.IntegerField(default=9100)  # ESC/POS default port

    def __str__(self):
        return self.name

class Category(models.Model):
    chayhana = models.ForeignKey(Chayhana, on_delete=models.CASCADE) 
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name

class Product(models.Model):# ombor uchun
    chayhana = models.ForeignKey(Chayhana, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    unit = models.CharField(max_length=20, default='kg')  # kg, dona, litr
    count = models.DecimalField(max_digits=14, decimal_places=0, default=0)
    price = models.DecimalField(max_digits=14, decimal_places=0, default=0)  # ombor narxi
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} ({self.count}{self.unit})"

    @property
    def total_value(self):
        return self.count * self.price

class IncomeProduct(models.Model): # kirim uchun
    chayhana = models.ForeignKey(Chayhana, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    count = models.DecimalField(max_digits=14, decimal_places=0)
    price = models.DecimalField(max_digits=14, decimal_places=0)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.product.name} - {self.count}{self.product.unit}"

    @property
    def total(self):
        return self.count * self.price

class MenuItem(models.Model): # menyu uchun
    chayhana = models.ForeignKey(Chayhana, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    sale_price = models.DecimalField(max_digits=14, decimal_places=0)
    image = models.ImageField(upload_to='menu_items/', null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    ingredients = models.JSONField(default=list)#[{"id": 1, "quantity": 2}, {"id": 3, "quantity": 0.5}]
    count = models.DecimalField(max_digits=14, decimal_places=0, default=0)  # nechtaligini kuzatish uchun
    auto_count = models.BooleanField(default=False) 
    is_active = models.BooleanField(default=True)
    is_rejected = models.BooleanField(default=False)
    reason_reject = models.CharField(max_length=255, null=True, blank=True)
    kitchen = models.ForeignKey(
        KitchenDepartment,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="Qaysi oshxona bo‘limi tayyorlaydi?"
    )
    def __str__(self):
        return self.name

class Order(models.Model): #buyurtma uchun
    chayhona = models.ForeignKey(Chayhana, on_delete=models.CASCADE)
    client_name = models.CharField(max_length=100, default='', blank=True)
    phone = models.CharField(max_length=15, default='', blank=True)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(null=True, blank=True)
    arrival_time = models.DateTimeField(null=True, blank=True)
    time_to_leave = models.DateTimeField(null=True, blank=True)
    finished = models.BooleanField(default=False)
    cancel = models.BooleanField(default=False)

    def __str__(self):
        return f"Order {self.id}"

    def calculate_service(self):
        room = self.room

        if room.service_percentage:
            return (self.total_summa * room.price_service) / 100
        else:
            return room.price_service

    
    @property
    def total_summa(self):
    # 1) Buyurtma itemlari summasi
        items_sum = sum(i.total for i in self.items.filter(cancel=False))

        # 2) Xona summasi
        room_price = self.room.price if self.room else 0

        # 3) Servis hisoblash
        if self.room:
            if self.room.service_percentage:
                # price_service = foiz masalan: 10 → %10
                service_price = (room_price * self.room.price_service) / 100
            else:
                # Odatdagi summa
                service_price = self.room.price_service
        else:
            service_price = 0

        # Yakuniy summa
        return items_sum + room_price + service_price
    
    @property
    def receipt(self):
        lines = []
        lines.append("------ BUYURTMA CHEKI ------\n")

        # Itemlar
        for item in self.items.filter(cancel=False):
            line = f"{item.menu_item.name} x {item.quantity} = {item.total:,}".replace(",", " ")
            lines.append(line)

        lines.append("\n-"*25)

        # Xona narxi
        room_price = self.room.price if self.room else 0
        lines.append(f"Xona narxi: {room_price:,}".replace(",", " "))

        # Servis
        if self.room:
            if self.room.service_percentage:
                # Foiz
                service_price = (room_price * self.room.price_service) / 100
                lines.append(
                    f"Servis ({self.room.price_service}%): {int(service_price):,}".replace(",", " ")
                )
            else:
                # Oddiy summa
                service_price = self.room.price_service
                lines.append(
                    f"Servis: {service_price:,}".replace(",", " ")
                )
        else:
            service_price = 0

        # Umumiy summa
        total = self.total_summa
        lines.append("-"*25)
        lines.append(f"Umumiy summa: {int(total):,}".replace(",", " "))
        lines.append("-"*25)

        return "\n".join(lines)

class OrderItem(models.Model):# buyurtma tarkibi
    chayhona = models.ForeignKey(Chayhana, on_delete=models.CASCADE)
    afisttyant = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)  
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=10, decimal_places=0, default=0)
    cancel = models.BooleanField(default=False)
    

    @property
    def total(self):
        if self.cancel:
            return 0
        return self.menu_item.sale_price * self.quantity

class IncomeUser(models.Model):
    chayhona = models.ForeignKey(Chayhana, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    total_summa = models.DecimalField(max_digits=14, decimal_places=0, default=0)

    def add_summa(self, amount):
        self.total_summa += amount
        self.save()
    @property
    def total_sum(self):
        items = self.items.filter(cancel=False)
        return sum([i.menu_item.sale_price * i.quantity for i in items])

class IncomeItemUser(models.Model):
    income = models.ForeignKey(IncomeUser, on_delete=models.CASCADE)
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    summa = models.DecimalField(max_digits=14, decimal_places=0)  # faqat shu orderdan service puli

class Kassa(models.Model):
    chayhona = models.ForeignKey(Chayhana, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    balance = models.DecimalField(max_digits=14, decimal_places=0, default=0)

class Cost(models.Model):
    chayhona = models.ForeignKey(Chayhana, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=14, decimal_places=0)
    date = models.DateField(auto_now_add=True)
    def __str__(self):
        return f"{self.name} - {self.amount}"
