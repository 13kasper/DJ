from .models import *
from django.db.models import Count
from .forms import *

menu = [
    {'title': "Добавить объявление", 'url_name': 'add_ads'},
    {'title': "Мои объявления", 'url_name': 'edit_page'},
    # {'title': "Регистрация", 'url_name': 'register'},
    # {'title': "Войти", 'url_name': 'login'},
]


class DataMixin:
    paginate_by = 3

    def get_user_context(self, **kwargs):
        context = kwargs
        cats = Category.objects.annotate(Count('product'))
        form_class = CommentForm
        # gh = Images.objects.all()

        user_menu = menu.copy()
        if not self.request.user.is_authenticated:
            user_menu.clear()

        context['menu'] = user_menu
        context['cats'] = cats
        context['form_class'] = form_class

        if 'cat_selected' not in context:
            context['cat_selected'] = 0
        return context
