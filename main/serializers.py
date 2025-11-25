from rest_framework import serializers
from .models import *


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'
        # depth = True
        # 
class ProductSerializer(serializers.ModelSerializer):
    total_value = serializers.ReadOnlyField()
    class Meta:
        model = Product
        fields = '__all__'

    def get_total_value(self, obj):
        return obj.total_value

# class ClientSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Client
#         fields = '__all__'
        # depth = True

class IncomeProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = IncomeProduct
        fields = '__all__'
        
class MenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = "__all__"

class OrderSerializer(serializers.ModelSerializer):
    created_at = serializers.SerializerMethodField()
    class Meta:
        model = Order
        fields = "__all__"

    def get_created_at(self,obj):
        return obj.created_at.strftime("%04d-%02d-%02d:%H:%M")
    
class OrderItemSerializer(serializers.ModelSerializer):
    # created_at = serializers.SerializerMethodField()
    class Meta:
        model = OrderItem
        fields = "__all__"


class KitchenDepartmentSerializer(serializers.ModelSerializer):
    # created_at = serializers.SerializerMethodField()
    class Meta:
        model = KitchenDepartment
        fields = "__all__"
        
class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [ 'id', 'username','phone', "is_active"]
        
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'