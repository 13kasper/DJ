from django.shortcuts import render
from .models import Boom
from .models import Menus
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout
from django.shortcuts import redirect
from django.db import IntegrityError
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate


def index(request):
    boo = Boom.objects.all()  # сохраняются все записи из БД
    menus = Menus.objects.all()
    return render(request, 'boom/index.html', {'boo': boo, 'links': menus})


def currentboom(request):
    return render(request, 'boom/currentboom.html')


def home(request):
    return render(request, 'boom/home.html')


def signupuser(request):
    if request.method == 'GET':
        return render(request, 'boom/signupuser.html', {'form': UserCreationForm()})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('currentboom')
            except IntegrityError:
                return render(request, 'boom/signupuser.html', {'form': UserCreationForm(),
                                                                'error': 'Такое имя позьзователя уже существует'})
        else:
            return render(request, 'boom/signupuser.html', {'form': UserCreationForm(), 'error': 'Пароли не совпадают'})


def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('index')


def loginuser(request):
    if request.method == 'GET':
        return render(request, 'boom/loginuser.html', {'form': AuthenticationForm})
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'boom/loginuser.html', {'form': AuthenticationForm,
                                                           'error': 'неверные данные для входа'})
        else:
            login(request, user)
            return redirect('currentboom')
