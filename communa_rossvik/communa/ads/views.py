from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.contrib.auth import login, authenticate
from django.views.generic import ListView, DetailView, CreateView, FormView, DeleteView, UpdateView
from django.views.generic.edit import FormMixin
from django.urls import reverse_lazy, reverse
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.core.mail import send_mail, BadHeaderError
from django.contrib import messages
from django.http import HttpResponseRedirect, Http404
from django.core.exceptions import ObjectDoesNotExist

from .models import *
from .forms import *
from .utils import *


class HomeView(DataMixin, ListView):

    model = Product
    template_name = 'ads/index.html'
    context_object_name = 'add_list'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Все категории')
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        return Product.objects.filter(is_published=True).select_related('cat')


class CustomSuccessMessageMixin:
    @property
    def success_msg(self):
        return False

    def form_valid(self, form):
        messages.success(self.request, self.success_msg)
        return super().form_valid(form)

    def get_success_url(self):
        return '%s?id=%s' % (self.success_url, self.object.id)


class ShowAds(CustomSuccessMessageMixin, FormMixin, DetailView):
    model = Product
    form_class = CommentForm
    template_name = 'ads/ads.html'
    context_object_name = 'ads'
    slug_url_kwarg = 'ads_slug'
    success_msg = "Комментарий успешно создан, ожидайте модерации"

    def get_success_url(self, **kwargs):
        # return reverse_lazy('ads', kwargs={'pk': self.get_object().id})
        return reverse('ads', kwargs={'ads_slug': self.object.product_comment.slug})

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.product_comment = self.get_object()
        self.object.author = self.request.user
        self.object.save()
        return super().form_valid(form)

    def get_context_data(self, *, object_list=None, **kwargs):
        user_menu = menu.copy()
        if not self.request.user.is_authenticated:
            user_menu.clear()
        context = super().get_context_data(**kwargs)
        context['title'] = context['ads']
        context['menu'] = user_menu
        context['gh'] = Images.objects.all()
        return context


class AdsCategory(DataMixin, ListView):
    model = Product
    template_name = 'ads/index.html'
    context_object_name = 'add_list'
    allow_empty = False

    def get_queryset(self):
        return Product.objects.filter(cat__slug=self.kwargs['cat_slug'], is_published=True).select_related('cat')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c = Category.objects.get(slug=self.kwargs['cat_slug'])
        c_def = self.get_user_context(title='' + str(c.name), cat_selected=c.pk)
        return dict(list(context.items()) + list(c_def.items()))


@login_required
def add_ads(request):
    user_menu = menu.copy()
    if not request.user.is_authenticated:
        user_menu.clear()

    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        files = request.FILES.getlist("images")
        if form.is_valid():
            f = form.save(commit=False)
            f.author = request.user
            f.save()
            for i in files:
                Images.objects.create(product=f, images=i)
            return redirect('index')
        else:
            print(form.errors)

    context = {
        'form': ProductForm(),
        'image_form': ImageForm(),
        'menu': user_menu,
    }

    return render(request, "ads/addads.html", context)


class RegisterUser(DataMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'ads/register.html'
    success_url = reverse_lazy('login')
    success_msg = "Успешная регистрация"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Регистрация')
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('index')


class LoginUser(DataMixin, LoginView):
    form_class = AuthUserForm
    template_name = 'ads/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Авторизация')
        return dict(list(context.items()) + list(c_def.items()))


@login_required
def edit_page(request, **kwargs):
    user_menu = menu.copy()
    if not request.user.is_authenticated:
        user_menu.clear()

    template = 'ads/edit_page.html'
    context = {
        'list_product': Product.objects.all().order_by('-id'),
        'menu': user_menu,
    }
    return render(request, template, context)


@login_required
def update_page(request, pk):
    user_menu = menu.copy()
    if not request.user.is_authenticated:
        user_menu.clear()

    success = False
    try:
        get_product = Product.objects.get(pk=pk, author=request.user)
    except ObjectDoesNotExist:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    # get_product = get_object_or_404(Product, pk=pk, author=request.user)
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES, instance=get_product)
        files = request.FILES.getlist("images")
        if form.is_valid():
            f = form.save(commit=False)
            f.author = request.user
            f.save()
            success = True
            for i in files:
                Images.objects.create(product=f, images=i)

            # return redirect('index')

    images_list = Images.objects.all().order_by('-id')
    template = 'ads/update_page.html'
    context = {
        'get_product': get_product,
        'images_list': images_list,
        'form': ProductForm(instance=get_product),
        'image_form': ImageForm(),
        'title': 'Редактировать объявление',
        'success': success,
        'menu': user_menu,
    }
    return render(request, template, context)


@login_required
def delete_image(request, id):
    image = Images.objects.get(pk=id).delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    # return redirect('edit_page')


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    template_name = 'ads/edit_page.html'
    success_url = reverse_lazy('edit_page')
    success_msg = 'Запись удалена'

    # def post(self, request, *args, **kwargs):
    #     messages.success(self.request, self.success_msg)
    #     return super().post(request)

    # def get_object(self, queryset=None):
    #     """ Hook to ensure object is owned by request.user. """
    #     obj = super(ProductDeleteView, self).get_object()
    #     if not obj.author == self.request.user:
    #         return redirect('edit_page')
    #     else:
    #         return obj
    def dispatch(self, request, *args, **kwargs):
        """ Making sure that only authors can delete Articles """
        obj = self.get_object()
        if obj.author != self.request.user:
            messages.error(request, 'У вас не достаточно прав для удаления.')
            return redirect('edit_page')
        messages.success(request, 'Запись удалена.')
        return super(ProductDeleteView, self).dispatch(request, *args, **kwargs)










