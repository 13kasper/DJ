from .models import *
from django.db.models import Count


menu = [
    {'title': "Добавить статью", 'url_name': 'add_page'},
    # {'title': "Регистрация", 'url_name': 'register'},
    # {'title': "Войти", 'url_name': 'login'},
    {'title': "Обратная связь", 'url_name': 'contact'}
]


class DataMixin:
    paginate_by = 3

    def get_user_context(self, **kwargs):
        context = kwargs
        # cats = Category.objects.all()
        """Что бы отображались только рабочие категории
        добавляем функцию агрегирования для отбора категорий"""
        cats = Category.objects.annotate(Count('blog'))

        """Создаем копию меню"""
        user_menu = menu.copy()
        """Если пользователь не авторизован удаляем пункт меню по индексу"""
        if not self.request.user.is_authenticated:
            user_menu.pop(0)

        context['menu'] = user_menu
        context['cats'] = cats

        if 'cat_selected' not in context:
            context['cat_selected'] = 0
        return context

