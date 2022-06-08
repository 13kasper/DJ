from django.contrib import admin
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms

from .models import *


class MuzAdmin(admin.ModelAdmin):
    """для подключения slug"""
    prepopulated_fields = {"slug": ('author',)}  # подключаем slug
    list_display = ('id', "author", "song", "time_created")  # отображаемые пункты в админке
    list_display_links = ("id", 'author')  # отображаемые пункты в админке c ссылками
    search_fields = ('author', 'song')  # добавляем поле поиска
    # list_editable = ('song',)  # для редактирования в общем списке (пример чек боксы ( снять с публикации))
    list_filter = ('time_created',)  # фильтр по параметрам


class CategoryAdmin(admin.ModelAdmin):
    """для подключения slug"""
    prepopulated_fields = {"slug": ('name',)}
    list_display = ('id', "name")  # отображаемые пункты в админке
    list_display_links = ("id", 'name')  # отображаемые пункты в админке c ссылками
    search_fields = ('name',)  # добавляем поле поиска


admin.site.register(Muz, MuzAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.site_header = 'Админ панель Россвик'
