
from rest_framework.routers import DefaultRouter
from django.urls import path
from .views import *
from .viewsets import *
router = DefaultRouter()

router.register(r'room', RoomViewset, basename='room')
router.register(r'product', ProductViewset, basename='product')
router.register(r'menu', MenuItemViewset, basename='menu')
router.register(r'income', IncomeProductViewset, basename='income')
router.register(r'order', OrderViewset, basename='order')
router.register(r'item', OrderItemViewset, basename='item')
router.register(r'category',CategoryViewset, basename='categoyy')
router.register(r'printer',KitchenDepartmentViewset, basename='printer')
router.register(r'kassa',KassaViewset, basename='kassa')
router.register(r'cost',CostViewset, basename='cost')


urlpatterns = [
   path('register/', RegisterView.as_view(), name='register'),
   path('ofisiant/register/', AfisttyantRegisterView.as_view(), name='hodim'),
   path('get-ofisiant/', get_ofisiant, name='hodimlar'),
   path('ofisiant/', ofisiant, name='hodim'),
   path('user/', get_user, name='user'),
   path('login/',LoginView.as_view(), name='login'),
   
   # path('category/', category, name='category'),
   path('chayhana/', chayhana, name='chayhana'),
   # path('afisttant/', afisttant, name='afisttant'),
   path('free-rooms/', free_rooms, name='free_rooms'),
   path('room-busy-dates/', room_busy_dates, name='room_busy_dates'),
   path('url/', url, name='url'),
   
   path('menu-client/<int:pk>/', menu, name='menu-client'),
   path('shot/<int:id>/', shot, name='shot'),

   
]
urlpatterns+=router.urls