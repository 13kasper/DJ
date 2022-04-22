from django.shortcuts import render
from django.http import HttpResponse
import random
# Create your views here.


def home(request):  # в request приходят данные из action с  html
    lst = list(range(6, 15))
    return render(request, "generator/home.html", {'lst': lst})


def password(request):
    char = [chr(i) for i in range(97, 123)]

    if request.GET.get('uppercase'):
        char.extend([chr(i) for i in range(65, 91)])

    if request.GET.get('numbers'):
        char.extend([chr(i) for i in range(48, 58)])

    if request.GET.get('special'):
        char.extend([chr(i) for i in range(33, 48)])

    length = int(request.GET.get('length', 12))  # request.GET.get - строка получения данных
    psw = ''
    for i in range(length):
        psw += random.choice(char)
    return render(request, 'generator/password.html', {'password': psw})


def about(request):  # в request приходят данные из action с  html
    # author = request.GET.get('author')
    # post = request.GET.get('post')
    author = 'Andrei Osipov'
    post = 'Выберите в выпадающем списке длину пароля, рекомендуемая длина пароля 12 символов, ' \
           'активируйте необходимые пункты для создания сложного пароля,' \
           ' пароль может включать буквы в верхнем регистре,' \
           'спецсимволы и цифры'

    return render(request, "generator/about.html", {'author': author, 'post': post})



