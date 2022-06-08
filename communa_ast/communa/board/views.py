from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.views.generic import ListView, DetailView, CreateView, FormView, TemplateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.views import LoginView
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse, HttpResponseRedirect

from .models import *
from .forms import *


class HomeView(TemplateView):
    template_name = 'board/home.html'
    model = Product
    context_object_name = 'add'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ads'] = Product.objects.all()
        return context


# class AddProductImagesView(TemplateView):
#     template_name = "add_images.html"
#
#     def post(self, request, *args, **kwargs):
#         try:
#             images = request.FILES.getlist('images')
#             product = Product.objects.get(id=self.kwargs['pk'])
#             for image in images:
#                 product_image = Images.objects.create(
#                     product=product,
#                     images=image
#                 )
#             return redirect('home')
#         except Exception as e:
#             print(e)

def create_project(request):
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        files = request.FILES.getlist("images")
        if form.is_valid():
            f = form.save(commit=False)
            f.user = request.user
            f.save()
            for i in files:
                Images.objects.create(product=f, images=i)
            return redirect('home')
        else:
            print(form.errors)
    else:
        form = ProductForm()
        imageform = ImageForm()

    return render(request, "board/add_ads.html", {"form": form, 'imageform': imageform})
