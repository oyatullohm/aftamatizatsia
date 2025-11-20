from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .models import *
from django.utils import timezone
from .serializers import *
from datetime import datetime, timedelta
from collections import defaultdict
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.decorators import api_view, permission_classes 
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
# Create your views here.

class RegisterView(APIView):
    def post(self, request):
        data = request.data
        if data.get('username') and CustomUser.objects.filter(username=data['username']).exists():
            return Response({'username': 'Bu username allaqachon ro‘yxatdan o‘tgan.'}, status=status.HTTP_400_BAD_REQUEST)
        if data.get('phone') and CustomUser.objects.filter(phone=data['phone']).exists():
            return Response({'phone': 'Bu telefon raqam allaqachon ro‘yxatdan o‘tgan.'}, status=status.HTTP_400_BAD_REQUEST)
        user = CustomUser.objects.create_user(username=data['username'],
                                              password=data['password'],
                                              phone=data['phone'])
            
        cayhana = Chayhana.objects.create(name=data.get('name'))
        Category.objects.bulk_create([
            Category(chayhana=cayhana, name="Taomlar"),
            Category(chayhana=cayhana, name="Ichimliklar"),
            Category(chayhana=cayhana, name="Shirinliklar"),
            Category(chayhana=cayhana, name="Salatlar"),
        ])

        user.chayhana = cayhana

        user.save()
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': {
                'id': user.id,
                'phone': user.phone,
                'cayhana': cayhana.name,
            }
        }, status=status.HTTP_201_CREATED)
        
 
class AfisttyantRegisterView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        data = request.data
        if data.get('username') and CustomUser.objects.filter(username=data['username']).exists():
            return Response({'username': 'Bu username allaqachon ro‘yxatdan o‘tgan.'}, status=status.HTTP_400_BAD_REQUEST)
        if data.get('phone') and CustomUser.objects.filter(phone=data['phone']).exists():
            return Response({'phone': 'Bu telefon raqam allaqachon ro‘yxatdan o‘tgan.'}, status=status.HTTP_400_BAD_REQUEST)
        user = CustomUser.objects.create_user(username=data['username'],
                                              password=data['password'],
                                              phone=data['phone'])
            
        cayhana = request.user.chayhana
        user.chayhana = cayhana

        user.save()
        return Response({
           'success':True
        }, status=status.HTTP_201_CREATED)

class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        if username is None or password is None:
            return Response({'error': 'Email and password required'}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(request, username= username, password=password)
        if user is not None:
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'phone': user.phone,
                    "is_staff":user.is_staff
                }
            }, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_ofisiant(request):
    chayhana = request.user.chayhana
    user = CustomUser.objects.filter(chayhana=chayhana)
    return Response(CustomUserSerializer(user).data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def ofisiant(request):
    active = request.data.get('active')
    id =  request.data.get('user_id')
    user = CustomUser.objects.get(id=id)
    user.is_active = bool(active)
    user.save()
    return Response({
           'success':True
        }, status=status)


# @login_required
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def category(request):
    categories = Category.objects.filter(chayhana=request.user.chayhana)
    data = [{'id': category.id, 'name': category.name} for category in categories]
    return Response(data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def chayhana(request):
    chayhana = request.user.chayhana
    data = {
        'id': chayhana.id,
        'uid': chayhana.uid,
        'name': chayhana.name,
    }
    return Response(data)



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def free_rooms(request):
    """ berilgan sanada bo'sh xonalarni qaytaradi
        date = request.GET.get("date")  YYYY-MM-DD
        va band xonalar vaqtlari bilan birga qaytaradi  
    """
    date_str = request.GET.get("date")
    if not date_str:
        date_str = timezone.now().strftime("%Y-%m-%d")
    try:
        selected_date = datetime.strptime(date_str, "%Y-%m-%d").date()
    except Exception:
        return Response({"error": "invalid date format"}, status=400)

    # Shu sanada band bo‘lgan buyurtmalar
    booked_orders = Order.objects.filter(
        chayhona=request.user.chayhana,
        arrival_time__date=selected_date,
        time_to_leave__date=selected_date
    ).select_related("room")

    # Band xonalar ID’lari
    booked_ids = {order.room_id for order in booked_orders}

    # Bo‘sh xonalar
    free_rooms = Room.objects.filter(chayhana=request.user.chayhana).exclude(id__in=booked_ids)
    free_data = RoomSerializer(free_rooms, many=True).data

    # ✅ Shu joyda biz barcha band xonalarni bitta `dict` ga jamlaymiz
    busy_dict = defaultdict(list)
    for order in booked_orders:
        busy_dict[order.room_id].append({
            "from": (order.arrival_time + timedelta(hours=5)).strftime("%H:%M"),
            "to": (order.time_to_leave + timedelta(hours=5)).strftime("%H:%M")
        })

    busy_data = []
    for room_id, times in busy_dict.items():
        room = next((r for r in booked_orders if r.room_id == room_id), None)
        if room:
            busy_data.append({
                "room": RoomSerializer(room.room).data,
                "times": times
            })

    return Response({
        "date": date_str,
        "free": free_data,
        "busy": busy_data
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def room_busy_dates(request):
    """ bu xonaga oid band kunlarni qaytaradi
        room_id = request.GET.get("room_id")    
        if not room_id:
        return Response({"error": "room_id required"}, status=400)  
    """
    room_id = request.GET.get("room_id")
    if not room_id:
        return Response({"error": "room_id required"}, status=400)

    orders = Order.objects.filter(chayhona=request.user.chayhana, room_id=room_id, finished=False).order_by("arrival_time")

    return Response(OrderSerializer(orders, many=True).data)


