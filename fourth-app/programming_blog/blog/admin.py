from django.contrib import admin
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django.utils.safestring import mark_safe
from django import forms

from .models import Blog
from .models import Category


class BlogAdminForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = Blog
        fields = '__all__'


class BlogAdmin(admin.ModelAdmin):
    form = BlogAdminForm
    """для перевода транслитом slug (путь ссылки)"""
    prepopulated_fields = {"slug": ('title',)}
    """устанавливаем в админке отображение полей"""
    list_display = ('id', 'title', 'time_created', 'get_html_photo', 'is_published')
    """Список отображаемых ссылок"""
    list_display_links = ('id', 'title')
    """Добавление поиска"""
    search_fields = ('title', 'content')
    """Редактируем чекбоксы (вкл/выкл)"""
    list_editable = ('is_published',)
    """Фильтрация в админке"""
    list_filter = ('is_published', 'time_created')
    """Какие поля хотим видеть """
    fields = ('title', 'slug', 'cat', 'content', 'photo', 'get_html_photo', 'is_published', 'time_created', 'time_update')
    """Поля для чтения"""
    readonly_fields = ('get_html_photo', 'time_created', 'time_update')
    """Добавляем панель управления наверх"""
    save_on_top = True

    """Для отображения фотографий в админке"""
    def get_html_photo(self, object):
        if object.photo:
            return mark_safe(f"<img src='{object.photo.url}' width='50'>")

    """меняем в админке название методу"""
    get_html_photo.short_description = 'Миниатюра'


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ('name',)}
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('name',)


admin.site.register(Blog, BlogAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.site_header = 'админ панель Росс'
