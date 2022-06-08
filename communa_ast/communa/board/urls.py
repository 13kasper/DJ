from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from .views import *
from . import views

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    # path('add_ads', AddAds.as_view(), name='add_ads'),
    path('add_ads/', views.create_project),

]