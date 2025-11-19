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
    def __str__(self):
        return f"{self.username}"

class Room(models.Model):
    chayhana = models.ForeignKey(Chayhana, on_delete=models.CASCADE) 
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=14, decimal_places=0)
    price_service = models.DecimalField(max_digits=14, decimal_places=0, default=0)
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
    is_active = models.BooleanField(default=True)
    kitchen = models.ForeignKey(
        KitchenDepartment,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="Qaysi oshxona bo‘limi tayyorlaydi?"
    )
    def __str__(self):
        return self.name




    def __str__(self):
        return f"{self.name} - {self.role}"

class Order(models.Model): #buyurtma uchun
    chayhona = models.ForeignKey(Chayhana, on_delete=models.CASCADE)
    # customer = models.ForeignKey(Client, on_delete=models.CASCADE, null=True, blank=True)
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
        summa = self.menu_item.sale_price * self.quantity
        servise = self.order.room.price_service
        room_sum = self.order.room.price
        return summa + servise + room_sum