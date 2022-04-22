from django.forms import ModelForm
from .models import Todo


class TodoForm(ModelForm):
    class Meta:  # обычно дополняется служебная информация
        model = Todo
        fields = ['title', 'memo', 'important']
