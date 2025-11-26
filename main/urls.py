
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
router.register(r'planmenue',DailyMenuPlanViewset, basename='planmenue')

urlpatterns = [
   path('register/', RegisterView.as_view(), name='register'),
   path('ofisiant/register/', AfisttyantRegisterView.as_view(), name='hodim'),
   path('get-ofisiant/', get_ofisiant, name='hodimlar'),
   path('ofisiant/', ofisiant, name='hodim'),
   path('login/',LoginView.as_view(), name='login'),
   
   # path('category/', category, name='category'),
   path('chayhana/', chayhana, name='chayhana'),
   # path('afisttant/', afisttant, name='afisttant'),
   path('free-rooms/', free_rooms, name='free_rooms'),
   path('room-busy-dates/', room_busy_dates, name='room_busy_dates'),
   
]
urlpatterns+=router.urls