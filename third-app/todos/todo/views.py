from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError  # ошибка сохранения пользователя в БД
from .forms import TodoForm
from .models import Todo


def home(request):
    return render(request, 'todo/home.html')


def signupuser(request):
    if request.method == 'GET':
        return render(request, 'todo/signupuser.html', {'form': UserCreationForm()})
    else:
        if request.POST['password1'] == request.POST['password2']:  # если в методе пост, пароли совпадают
            try:
                user = User.objects.create_user(request.POST['username'],
                                                password=request.POST['password1'])  # создаем пользователя
                user.save()  # сохраняем пользователя
                login(request, user)  # логиним пользователя
                return redirect('currenttodos')  # перенаправляем на страницу

            except IntegrityError:  # ошибка сохранения пользователя в БД, отправляем на страницу входа
                return render(request, 'todo/signupuser.html', {'form': UserCreationForm(), 'error': 'Такое имя/'
                                                                                                     ' пользователя уже существует, задайте другое'})
        else:
            return render(request, 'todo/signupuser.html', {'form': UserCreationForm(), 'error': 'Пароли не совпадают'})


def currenttodos(request):
    todos = Todo.objects.filter(user=request.user, date_completed_isnull=True)
    return render(request, 'todo/currenttodos.html', {'todos': todos})


def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')


def loginuser(request):
    if request.method == 'GET':
        return render(request, 'todo/loginuser.html', {'form': AuthenticationForm})
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'todo/loginuser.html',
                          {'form': AuthenticationForm(), 'error': 'неверные данные для входа'})
        else:
            login(request, user)
            return redirect('currenttodos')


def createtodo(request):
    if request.method == 'GET':
        return render(request, 'todo/createtodo.html', {'form': TodoForm()})
    else:
        try:
            form = TodoForm(request.POST)
            new_todo = form.save(commit=False)
            new_todo.user = request.user
            new_todo.save()
            return redirect('currenttodos')
        except ValueError:
            return render(request, 'todo/createtodo.html', {'form': TodoForm(), 'error': 'Переданы неверные данные'})
