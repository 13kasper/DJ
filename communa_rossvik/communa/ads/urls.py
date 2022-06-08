from django.urls import path, include
from django.contrib.auth import views as auth_views
from .views import *
from . import views


urlpatterns = [
    path('', HomeView.as_view(), name='index'),
    path('ads/<slug:ads_slug>', ShowAds.as_view(), name='ads'),
    path('category/<slug:cat_slug>', AdsCategory.as_view(), name='category'),
    path('addads/', views.add_ads, name='add_ads'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='ads/logout.html'), name='logout'),
    path('edit-page', views.edit_page, name='edit_page'),
    path('update-page/<int:pk>', views.update_page, name='update_page'),
    path('delete-image/<int:id>', views.delete_image, name="delete_image"),
    path('delete-page/<int:pk>', ProductDeleteView.as_view(), name="delete_page"),

]
