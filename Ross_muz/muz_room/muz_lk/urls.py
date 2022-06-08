from django.urls import path
from .views import *

urlpatterns = [

    path('', MuzHome.as_view(), name='index'),
    path('category/<slug:cat_slug>/', MuzCategory.as_view(), name='category'),

]