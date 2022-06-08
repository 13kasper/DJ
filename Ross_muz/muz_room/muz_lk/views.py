from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.views.generic import ListView, DetailView, CreateView, FormView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.views import LoginView
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from .models import *

menu = [
    {'title': "Добавить песню", 'url_name': 'add_song'},
    {'title': "Регистрация", 'url_name': 'register'},
    {'title': "Войти", 'url_name': 'login'},
    {'title': "Обратная связь", 'url_name': 'contact'}
]


class MuzHome(ListView):
    model = Muz
    template_name = 'muz_lk/index.html'
    context_object_name = 'songs'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)  # Переопределение метода
        context['title'] = 'Ross_muz'
        context['cat_selected'] = 0  # выделенная категория (по умолчанию ноль)
        context['menu'] = menu
        return context

    def get_queryset(self):  # метод для фильтровки данных по выбранной категории
        return Muz.objects.select_related('cat')  # получаем данные из БД и сортируем по категориям


class MuzCategory(ListView):
    model = Muz
    template_name = 'muz_lk/index.html'
    context_object_name = 'songs'

    def get_queryset(self):  # метод для фильтровки данных по выбранной категории
        return Muz.objects.filter(cat__slug=self.kwargs['cat_slug']).select_related('cat')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)  # Переопределение метода
        context['title'] = 'Жанр - ' + str(context['songs'])
        context['cat_selected'] = 0  # выделенная категория (по умолчанию ноль)
        context['menu'] = menu
        return context


