from django.shortcuts import render
from .models import Boom
from .models import Menus


def index(request):
    boo = Boom.objects.all()  # сохраняются все записи из БД
    menus = Menus.objects.all()
    return render(request, 'boom/index.html', {'boo': boo, 'links': menus})
