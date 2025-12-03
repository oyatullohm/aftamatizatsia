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


class IncomeProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = IncomeProduct
        fields = '__all__'
        
class MenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = "__all__"

class MenuItemAdminSerializer(serializers.ModelSerializer):
    ingredients = serializers.SerializerMethodField()
    class Meta:
        model = MenuItem
        fields = "__all__"
    
    def get_ingredients(self, obj):
        result = []
        for item in obj.ingredients:
            try:
                product = Product.objects.get(id=item["id"])
                result.append({
                    "id": item["id"],
                    "name": product.name,
                    "unit": product.unit,
                    "count": item["quantity"]
                })
            except Product.DoesNotExist:
                result.append(item)
        return result

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

class KassaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Kassa
        fields = '__all__'

class CostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cost
        fields = '__all__'
        
        
class MobileOrderItemSerializer(serializers.Serializer):
    menu_id = serializers.IntegerField()
    quantity = serializers.IntegerField()

class MobileCreateOrderSerializer(serializers.Serializer):
    client_name = serializers.CharField(required=False, allow_blank=True)
    phone = serializers.CharField(required=False, allow_blank=True)
    room_id = serializers.IntegerField(required=False, allow_null=True)
    items = MobileOrderItemSerializer(many=True)
