from django.urls import path
from .views import *

urlpatterns = [
    path('api/buy-stock/', buy_stock, name='buy-stock'),
]

