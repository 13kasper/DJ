from django.apps import AppConfig


class BlogConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'blog'
    """Переводим разделы в админке"""
    verbose_name = "Блог новостей"
