from django.urls import path, include
from .views import exchange

urlpatterns = [
    path('', exchange, name='index'),
]
