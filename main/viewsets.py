
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import  IsAuthenticated , AllowAny
from .serializers import *
from rest_framework.response import Response
from rest_framework.decorators import action, permission_classes
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q
from django.utils import timezone
from rest_framework import status
from .utlis import print_kitchen_check
from datetime import date


class CategoryViewset(ModelViewSet):
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Category.objects.filter(chayhana=self.request.user.chayhana)
    
    def list(self, request, *args, **kwargs):
        serializers = CategorySerializer(self.get_queryset(),many= True)
        return Response(serializers.data)
    
    def retrieve(self, request, *args, **kwargs):
        category = self.get_queryset().get(id=kwargs['pk'])
        return Response(CategorySerializer(category).data)
    
    def update(self, request, *args, **kwargs):
        category = self.get_queryset().get(id=kwargs['pk'])
        name = request.data.get('name')
        if name:
            category.name = name
        category.save()
        return Response(CategorySerializer(category).data)
        
    
    def create(self, request, *args, **kwargs):
        chayhana = request.user.chayhana
        name = request.data.get('name')
       
        category = Category.objects.create(
            chayhana= chayhana,
            name=name,
           
        ) 
        serializers = CategorySerializer(category )
        return Response(serializers.data)


    def destroy(self, request, *args, **kwargs):
        self.get_queryset().get(id=kwargs['pk']).delete()
        return Response({'sucsess':True})

class RoomViewset(ModelViewSet):
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Room.objects.filter(chayhana=self.request.user.chayhana).select_related('chayhana')
    
    def list(self, request, *args, **kwargs):
        serializers = RoomSerializer(self.get_queryset(),many= True)
        return Response(serializers.data)
    
    def retrieve(self, request, *args, **kwargs):
        rom = self.get_queryset().get(id=kwargs['pk'])
        return Response(RoomSerializer(rom).data)
    
    def update(self, request, *args, **kwargs):
        room = self.get_queryset().get(id=kwargs['pk'])
        name = request.data.get('name')
        price = request.data.get('price')
        price_service = request.data.get('price_service')
        service_percentage = request.data.get('service_percentage')
        
        disciription = request.data.get('disciription')
        if name:
            room.name = name
        if price:
            room.price = price
        if disciription:
            room.disciription = disciription
        if service_percentage:
            room.service_percentage = bool(service_percentage)
        if price_service:
            room.price_service = price_service
        room.save()
        return Response(RoomSerializer(room).data)
        
    
    def create(self, request, *args, **kwargs):
        chayhana = request.user.chayhana
        name = request.data.get('name')
        price = request.data.get('price')
        price_service = request.data.get('price_service')
        service_percentage = request.data.get('service_percentage')
        disciription = request.data.get('disciription')
       
        room = Room.objects.create(
            chayhana= chayhana,
            name=name,
            price=price,
            disciription=disciription,
            service_percentage=service_percentage,
            price_service=price_service
        ) 
        serializers = RoomSerializer(room )
        return Response(serializers.data)


    def destroy(self, request, *args, **kwargs):
        self.get_queryset().get(id=kwargs['pk']).delete()
        return Response({'sucsess':True})

class ProductViewset(ModelViewSet):
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Product.objects.filter(chayhana=self.request.user.chayhana).select_related('chayhana')
    
    def list(self, request, *args, **kwargs):
        serializers = ProductSerializer(self.get_queryset(),many= True)
        return Response(serializers.data)
    
    def retrieve(self, request, *args, **kwargs):
        product = self.get_queryset().get(id=kwargs['pk'])
        return Response(ProductSerializer(product).data)
    
    def update(self, request, *args, **kwargs):
        product = self.get_queryset().get(id=kwargs['pk'])
        name = request.data.get('name')
        price = request.data.get('price')
        count = request.data.get('count')
        active = request.data.get('active')
        unit = request.data.get('unit')
        if name:
            product.name = name
        if price:
            product.price = price
        if count:
            product.count = count
        if unit:
            product.unit = unit
        if active:
            product.is_active = bool(active)
        product.save()
        return Response(ProductSerializer(product).data)

    def create(self, request, *args, **kwargs):
        chayhana = request.user.chayhana
        name = request.data.get('name')
        price = request.data.get('price')
        count = request.data.get('count')
        unit = request.data.get('unit')
 
        product = Product.objects.create(
            chayhana= chayhana,
            name=name,
            unit=unit,
            price=price,
            count=count
        ) 
        serializers = ProductSerializer(product )
        return Response(serializers.data)

    def destroy(self, request, *args, **kwargs):
        self.get_queryset().get(id=kwargs['pk']).delete()
        return Response({'sucsess':True})
            
class IncomeProductViewset(ModelViewSet):
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return IncomeProduct.objects.filter(chayhana=self.request.user.chayhana).select_related('chayhana','product')
    
    def list(self, request, *args, **kwargs):
        serializers = IncomeProductSerializer(self.get_queryset(),many= True)
        return Response(serializers.data) 
    
    def create(self, request, *args, **kwargs):
        chayhana = request.user.chayhana
        product_id = request.data.get('product_id')
        price = request.data.get('price')
        count = request.data.get('count')
        product = Product.objects.get(id=product_id)
        product.count += int(count)
        product.save()
        income_product = IncomeProduct.objects.create(
            chayhana= chayhana,
            product_id=product_id,
            price=price,
            count=count
        )
        
        menu_items = MenuItem.objects.filter(
        chayhana=chayhana,
        name__iexact=product.name,
        auto_count=True
        )

        for item in menu_items:
            item.count += int(count)
            item.save()


        
        serializers = IncomeProductSerializer(income_product )
        return Response(serializers.data) 
    
    def destroy(self, request, *args, **kwargs):
        income_product = self.get_queryset().get(id=kwargs['pk'])
        product = income_product.product
        product.count -= income_product.count
        product.save()
        menu_items = MenuItem.objects.filter(
        chayhana=self.user.chayhana,
        name__iexact=product.name,
        auto_count=True
        )
        for i in menu_items:
            i.count-=income_product.count()
            i.save()
        
        income_product.delete()
        return Response({'sucsess':True}) 
    
    def retrieve(self, request, *args, **kwargs):
        income_product = self.get_queryset().get(id=kwargs['pk'])
        return Response(IncomeProductSerializer(income_product).data)
    
    def update(self, request, *args, **kwargs):
        income_product = self.get_queryset().get(id=kwargs['pk'])
        price = request.data.get('price')
        count = request.data.get('count')
        product = income_product.product
        menu_items = MenuItem.objects.filter(
        chayhana=request.user.chayhana,
        name__iexact=product.name,
        auto_count=True
        )
        if count:
            product.count -= income_product.count
            product.count += int(count)
            income_product.count = count
            product.save()
            for m in menu_items:
                m.count -= income_product.count
                m.count += int(count)
                m.save()
        if price:
            income_product.price = price
        income_product.save()
        return Response(IncomeProductSerializer(income_product).data)

class MenuItemViewset(ModelViewSet):
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        return MenuItem.objects.filter(chayhana=self.request.user.chayhana).select_related('chayhana','category')
    
    def list(self, request, *args, **kwargs):
        category_id = request.GET.get('category_id')
        queryset = self.get_queryset()
        if category_id:
            queryset =queryset.filter( category_id=category_id)
        serializers = MenuItemAdminSerializer(queryset,many= True)
        return Response(serializers.data)
    
    @action(detail=False, methods=['get'])
    def list_(self, request, *args, **kwargs):
        category_id = request.GET.get('category_id')
        queryset = self.get_queryset().filter(is_active=True)
        if category_id:
            queryset =queryset.filter( category_id=category_id)
        serializers = MenuItemSerializer(queryset,many= True)
        return Response(serializers.data)
    
    def create(self, request, *args, **kwargs):
        chayhana = request.user.chayhana
        name = request.data.get('name')
        sale_price = request.data.get('sale_price')
        category_id = request.data.get('category_id')
        data = request.data.get('ingredients', [])
        kitchen_id = request.data.ger("kitchen_id")
        menu_item = MenuItem.objects.create(
            chayhana= chayhana,
            name=name,
            sale_price=sale_price,
            category_id=category_id,
            ingredients=data,
            kitchen_id = kitchen_id
        )
        
        serializers = MenuItemSerializer(menu_item )
        return Response(serializers.data)
    
    @action(detail=True, methods=['post'])
    def ingredients_add(self, request, pk=None):
        """
        bu funsiya menu item ga ingredient larni qo'shish uchun ishlatiladi
        request data da ingredients list ko'rinishida bo'ladi:
        [{"id": 1, "quantity": 2}, {"id": 3, "quantity": 0.5}]  
        """
        menu_item = self.get_queryset().get(id=pk)
        data = request.data.get('ingredients', [])
        menu_item.ingredients = data
        menu_item.save()
        return Response({
            "success":True
        })

    def retrieve(self, request, *args, **kwargs):
        menu_item = self.get_queryset().get(id=kwargs['pk'])
        product_ids = [item["id"] for item in  menu_item.ingredients]
        products_map = {
            p.id: p for p in Product.objects.filter(id__in=product_ids)
        }
        image = None
        if menu_item.image:
            image = menu_item.image.url
        
        result = [{
            "id":menu_item.id,
            "name":menu_item.name,
            "sale_price":menu_item.sale_price,
            'image':image,
            "category":menu_item.category.name,
            "is_active":menu_item.is_active
        }]
        for item in menu_item.ingredients:
            product = products_map.get(item["id"])  # xato bo'lsa None qaytadi
            if product: 
                result.append({
                    "id": product.id,
                    "name": product.name,
                    "quantity": item.get("quantity", 0)
                })
        
        return Response(result)
    
    def update(self, request, *args, **kwargs):
        menu_item = self.get_queryset().get(id=kwargs['pk'])
        name = request.data.get('name')
        sale_price = request.data.get('sale_price')
        category_id = request.data.get('category_id')
        count = request.data.get('count')
        auto_count = request.data.get('auto_count')
        image = request.data.get('image')
        kitchen_id = request.data.get('kitchen_id')
        if name:
            menu_item.name = name
        if sale_price:
            menu_item.sale_price = sale_price
        if category_id:
            menu_item.category_id = category_id
        if image:
            if menu_item.image:
                menu_item.image.delete()
            menu_item.image = image
        if auto_count:
            menu_item.auto_count = bool(auto_count)
        if count:
            menu_item.count = count
        if kitchen_id:
            menu_item.kitchen_id= kitchen_id
        menu_item.save()
        return Response(MenuItemSerializer(menu_item).data)
    
    def destroy(self, request, *args, **kwargs):
        menu_item = self.get_queryset().get(id=kwargs['pk'])
        if menu_item.image:
            menu_item.image.delete()
        menu_item.delete()
        return Response({'sucsess':True})
    
    @action(detail=True, methods=['post'])
    def set_active(self, request, pk=None):
        menu_item = self.get_queryset().get(id=pk)
        is_active = request.data.get('is_active')
        if is_active is not None:
            menu_item.is_active = bool(is_active)
            menu_item.save()
        return Response(MenuItemSerializer(menu_item).data)

class OrderViewset(ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = OrderSerializer
    def get_queryset(self):
        return Order.objects.filter(chayhona=self.request.user.chayhona, finished=False).select_related(
            'chayhona','room'
        ).prefetch_related('items')
    
    @action(detail=True, methods=['get'])
    @permission_classes([AllowAny])
    def summa(self, request, pk=None):
        order = Order.objects.get(id=pk)
        return Response({"total_summa": order.total_summa})
    
    def list(self, request, *args, **kwargs):
        qs = self.get_queryset()
        phone = request.GET.get("phone")
        client_name = request.GET.get("client_name")
        room_id = request.GET.get("room_id")
        finished = request.GET.get("finished")
        date_from = request.GET.get("date_from")  # 2025-11-07
        date_to = request.GET.get("date_to")      # 2025-11-10
        arrival_from = request.GET.get("arrival_from")
        arrival_to = request.GET.get("arrival_to")
        leave_from = request.GET.get("leave_from")
        leave_to = request.GET.get("leave_to")

        # ✅ Customer bo‘yicha filtr
        if client_name:
            qs = qs.filter(client_name=client_name)
        if phone:
            qs = qs.filter(phone__icontains=phone)

        # ✅ Room bo‘yicha filtr
        if room_id:
            qs = qs.filter(room_id=room_id)

        # ✅ finished bo‘yicha filtr (true/false)
        if finished is not None:
            if finished.lower() in ["true", "1"]:
                qs = qs.filter(finished=True)
            elif finished.lower() in ["false", "0"]:
                qs = qs.filter(finished=False)
        # ✅ created_at bo‘yicha sana oralig‘i
        if date_from:
            qs = qs.filter(created_at__date__gte=date_from)

        if date_to:
            qs = qs.filter(created_at__date__lte=date_to)

        # ✅ arrival_time bo‘yicha filtr (datetime)
        if arrival_from:
            qs = qs.filter(arrival_time__gte=arrival_from)

        if arrival_to:
            qs = qs.filter(arrival_time__lte=arrival_to)

        # ✅ leave_time bo‘yicha filtr
        if leave_from:
            qs = qs.filter(time_to_leave__gte=leave_from)

        if leave_to:
            qs = qs.filter(time_to_leave__lte=leave_to)

        serializer = OrderSerializer(qs, many=True)
        return Response(serializer.data)
    
    def create(self, request, *args, **kwargs):
        data = request.data
        
        room_id = data.get("room")
        phone = data.get("phone ", "")
        client_name = data.get("name", "")
        arrival_time = data.get("arrival_time")
        time_to_leave = data.get("time_to_leave")


        if not time_to_leave:
            return Response({"error": "time_to_leave is required"}, status=400)

        # ✅ Agar arrival_time kelmasa – hozirgi vaqtni olamiz
        if not arrival_time:
            arrival_time = timezone.now()

        # ✅ Modelga mos formatga o‘tkazamiz
        arrival_time = timezone.make_aware(
            timezone.datetime.fromisoformat(str(arrival_time))
        )

        time_to_leave = timezone.make_aware(
            timezone.datetime.fromisoformat(str(time_to_leave))
        )

        # ✅ Xona bandligini tekshirish
        conflicts = Order.objects.filter(
            room_id=room_id,
            finished=False,  # Active orders only
            arrival_time__lt=time_to_leave,
            time_to_leave__gt=arrival_time
        )

        if conflicts.exists():
            # ✅ Band xonani qaytarish
            return Response(
                {"error": "Bu vaqtda xona band. Iltimos boshqa vaqt tanlang."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # ✅ CREATE malumot yaratish
        serializer = self.get_serializer(data={
            "room": room_id,
            # "customer": customer_id,
            'client_name': client_name,
            'phone': phone,
            "arrival_time": arrival_time,
            "time_to_leave": time_to_leave,
            "chayhona": request.user.chayhana.id
        })

        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        data = request.data
        client_name = data.get('name')
        phone = data.get('phone')
        room = data.get('room')
        arrival_time = data.get('arrival_time')
        time_to_leave = data.get('time_to_leave')
        update_at  = timezone.datetime()
        order = self.get_queryset().get(id=kwargs['pk'])
        if client_name:
            order.client_name = client_name
        if phone:
            order.phone = phone
        if room:
            order.room = room
        if arrival_time:
            order.arrival_time = arrival_time
        if time_to_leave:
            order.time_to_leave = time_to_leave
        order.update_at = update_at
        order.save()
        return Response({
            OrderSerializer(order).data
        })

    @action(detail=True, methods=['post'])
    def finished(self, request, pk=None):
        payments = request.data.get('payments', [])   # bir nechta to‘lov
        
        if not payments:
            return Response({"error": "Payments bo‘sh bo‘lishi mumkin emas"}, status=400)

        order = self.get_queryset().get(id=pk)

        # Afitsiantni aniqlaymiz
        item = order.items.filter(cancel=False).first()
        if not item or not item.afisttyant:
            return Response({"error": "Afitsiant topilmadi."}, status=400)
        user = item.afisttyant

        # Orderni tugatamiz
        order.finished = True
        order.save()

        # IncomeUser
        today = date.today()
        income_user, created = IncomeUser.objects.get_or_create(
            chayhona=order.chayhona,
            user=user,
            date=today,
        )

        # Service hisoblash
        service_sum = order.calculate_service()

        # IncomeItemUser
        income_item, created = IncomeItemUser.objects.get_or_create(
            income=income_user,
            order=order,
            defaults={"summa": service_sum}
        )

        if created:
            income_user.add_summa(service_sum)

        # 🔥 Kassa bo‘yicha to‘lovlarni qo‘shish
        total_payment = 0

        for p in payments:
            kassa_id = p.get('kassa_id')
            summa = p.get('summa')

            if not kassa_id or not summa:
                return Response({"error": "Har bir paymentda kassa_id va summa bo‘lishi kerak"}, status=400)

            try:
                kassa = Kassa.objects.get(id=kassa_id)
            except Kassa.DoesNotExist:
                return Response({"error": f"Kassa topilmadi: {kassa_id}"}, status=404)

            kassa.balance += summa
            kassa.save()
            total_payment += summa

        return Response({
            "success": True,
            "order_total": order.total_summa,
            "paid_sum": total_payment,
            "service_sum": service_sum,
            "income_user_total": income_user.total_summa,
            "message": "Order yakunlandi va to‘lovlar bir nechta kassaga bo‘lindi"
        })

            
    @action(detail=True, methods=['post'])
    def cancel(self,request, pk=None):
        order = self.get_queryset().get(id=pk)
        order.cancel = True
        order.finished = True
        order.save()

        return Response({
            "success":True
        })

        
    def destroy(self, request, *args, **kwargs):
        return Response({
            "success":False
        })

class OrderItemViewset(ModelViewSet):
    permission_classes =[ IsAuthenticated]
    def get_queryset(self,order_id):
        return  OrderItem.objects.filter(
            chayhona=self.request.user.chayhana,
            order_id=order_id
        ).select_related('chayhona', 'order', 'menu_item')
    
    def list(self, request, *args, **kwargs):
        order_id = request.GET.get('order-id')
        queryset = self.get_queryset(order_id)
        return Response(
            OrderItemSerializer(queryset, many=True).data
        )
    
    def create(self, request, *args, **kwargs):
        data = request.data

        order_id = data.get("order_id")
        menu_item_id = data.get("menu_item_id")
        quantity = data.get("quantity")

        if not order_id:
            return Response({"error": "order_id required"}, status=400)

        if not menu_item_id:
            return Response({"error": "menu_item_id required"}, status=400)

        # quantity string bo'lib keladi → int ga o'tkazamiz
        try:
            quantity = int(quantity)
        except:
            quantity = 1

        # Itemni yaratamiz yoki topamiz
        item, created = OrderItem.objects.get_or_create(
            chayhona=request.user.chayhona,
            order_id=order_id,
            menu_item_id=menu_item_id,
            defaults={"quantity": quantity}
        )

        # qancha qo‘shildi — eski bo‘lsa qo‘shamiz
        added_quantity = quantity
        if not created:
            item.quantity += quantity
            item.save()

        # 🔥 Omborni yangilash (minus qilish)
        menu_item = item.menu_item

        for ingredient in menu_item.ingredients:
            product_id = ingredient.get("id")
            konsum = ingredient.get("quantity")   # 1 porsiya uchun sarf

            try:
                product = Product.objects.get(id=product_id, chayhona=request.user.chayhona)
            except Product.DoesNotExist:
                continue  # Product topilmasa skip

            minus_amount = konsum * added_quantity
            product.count -= minus_amount
            product.save()
        print_kitchen_check(item)
        return Response(OrderItemSerializer(item).data, status=201)

    def retrieve(self, request, order_id, pk):
        item = self.get_queryset(order_id).get(id=pk)
        return Response({
            OrderItemSerializer(item).data
        })
    
    def update(self, request, order_id, pk):
        data = request.data
        quantity = data.get('quantity')
        item = self.get_queryset(order_id).get(id=pk)
        if quantity:
            # qancha o'zgardi
            added_quantity = int(quantity) - item.quantity
            item.quantity = int(quantity)
            item.save()

            # 🔥 Omborni yangilash (minus qilish)
            menu_item = item.menu_item

            for ingredient in menu_item.ingredients:
                product_id = ingredient.get("id")
                konsum = ingredient.get("quantity")   # 1 porsiya uchun sarf

                try:
                    product = Product.objects.get(id=product_id, chayhona=request.user.chayhona)
                except Product.DoesNotExist:
                    continue  # Product topilmasa skip

                minus_amount = konsum * added_quantity
                product.count -= minus_amount
                product.save()
        return Response({
            OrderItemSerializer(item).data
        }) 
    @action(detail=True,methods=['post'])
    def cancel(self,request, order_id, pk):
        item = self.get_queryset(order_id).get(id=pk)
        menu_item = item.menu_item
        added_quantity  = item.quantity
        for ingredient in menu_item.ingredients:
            product_id = ingredient.get("id")
            konsum = ingredient.get("quantity")
            
            try:
                product = Product.objects.get(id=product_id, chayhona=request.user.chayhona)
            except Product.DoesNotExist:
                continue  # Product topilmasa skip

            minus_amount = konsum * added_quantity
            product.count += minus_amount
            product.save()
        return Response({
            "success":True
        })

    def destroy(self, request, *args, **kwargs):
        return Response({
            'success':False
        })

class KitchenDepartmentViewset(ModelViewSet):
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return KitchenDepartment.objects.filter(chayhana=self.request.user.chayhana)
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        return Response({
            KitchenDepartmentSerializer(queryset, many=True).data
        })
    
    def retrieve(self, request, *args, **kwargs):
        printer = self.get_queryset().get(id=kwargs['pk'])
        return Response(KitchenDepartmentSerializer(printer).data)
    
    def update(self, request, *args, **kwargs):
        data = request.data
        name = data.get('name')
        printer_ip = data.get('printer_ip')
        printer_port = data.get('printer_port')
        printer = self.get_queryset().get(id=kwargs['pk'])
        
        if name:
            printer.name = name
        if printer_ip:
            printer.printer_ip =printer_ip
        if printer_port:
            printer.printer_port = printer_port
        printer.save()
        
        return Response(KitchenDepartmentSerializer(printer).data)
    
    def create(self, request, *args, **kwargs):
        data = request.data
        name = data.get('name')
        printer_ip = data.get('printer_ip')
        printer_port = data.get('printer_port')
        printer =  KitchenDepartment.objects.create(
            chayhana = request.user.chayhana,
            name = name,
            printer_ip = printer_ip,
            printer_port = printer_port
        )
        return Response(KitchenDepartmentSerializer(printer).data)
    
    def destroy(self, request, *args, **kwargs):
        self.get_queryset().get(id=kwargs['pk']).delete()
        return Response({
            'success':True
        })

class KassaViewset(ModelViewSet):
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Kassa.objects.filter(chayhona=self.request.user.chayhana)
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        return Response({
            KassaSerializer(queryset, many=True).data
        })
    
    def retrieve(self, request, *args, **kwargs):
        kassa = self.get_queryset().get(id=kwargs['pk'])
        return Response(KassaSerializer(kassa).data)
    
    def update(self, request, *args, **kwargs):
        data = request.data
        name = data.get('name')
        initial_amount = data.get('initial_amount')
        kassa = self.get_queryset().get(id=kwargs['pk'])
        
        if name:
            kassa.name = name
        if initial_amount:
            kassa.initial_amount = initial_amount
        kassa.save()
        
        return Response(KassaSerializer(kassa).data)
    
    def create(self, request, *args, **kwargs):
        data = request.data
        name = data.get('name')
        initial_amount = data.get('initial_amount')
        kassa =  Kassa.objects.create(
            chayhona = request.user.chayhana,
            name = name,
            initial_amount = initial_amount
        )
        return Response(KassaSerializer(kassa).data)
    
    def destroy(self, request, *args, **kwargs):
        self.get_queryset().get(id=kwargs['pk']).delete()
        return Response({
            'success':True
        }) 

class CostViewset(ModelViewSet):
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Cost.objects.filter(chayhona=self.request.user.chayhana)
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        return Response({
            CostSerializer(queryset, many=True).data
        })
    
    def retrieve(self, request, *args, **kwargs):
        cost = self.get_queryset().get(id=kwargs['pk'])
        return Response(CostSerializer(cost).data)
    
    def update(self, request, *args, **kwargs):
        data = request.data
        name = data.get('name')
        amount = data.get('amount')
        cost = self.get_queryset().get(id=kwargs['pk'])
        
        if name:
            cost.name = name
        if amount:
            cost.amount = amount
        cost.save()
        
        return Response(CostSerializer(cost).data)
    
    def create(self, request, *args, **kwargs):
        data = request.data
        name = data.get('name')
        amount = data.get('amount')
        cost =  Cost.objects.create(
            chayhona = request.user.chayhana,
            name = name,
            amount = amount
        )
        return Response(CostSerializer(cost).data)
    
    def destroy(self, request, *args, **kwargs):
        self.get_queryset().get(id=kwargs['pk']).delete()
        return Response({
            'success':True
        })
