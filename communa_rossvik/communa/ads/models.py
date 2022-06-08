from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


class Product(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Владелец объявления', blank=True, null=True)
    title = models.CharField(max_length=255, verbose_name='Название')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="Символьный код (на английском)")
    content = models.TextField(blank=True, verbose_name='Описание')
    price = models.CharField(max_length=20, verbose_name='Цена')
    photo = models.ImageField(upload_to="photos/%Y/%m/%d/", blank=True, verbose_name='Обложка')
    time_created = models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')
    time_update = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    is_published = models.BooleanField(default=True, verbose_name='Опубликовано')
    cat = models.ForeignKey('Category', on_delete=models.PROTECT, verbose_name='Категория')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('ads', kwargs={'ads_slug': self.slug})

    class Meta:
        """Переводим админку на русский"""
        verbose_name = "Объявление"
        verbose_name_plural = "Объявления"
        ordering = ['-time_created']  # сортировка объявлений


class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True, verbose_name='Категория')
    slug = models.SlugField(max_length=100, unique=True, db_index=True, verbose_name='URL')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_slug': self.slug})

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class Images(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE, null=True, blank=True, verbose_name='Альбом')
    images = models.ImageField(upload_to='images/%Y/%m/%d/', verbose_name='Фотоальбом', blank=True)

    def __str__(self):
        return self.images

    class Meta:
        verbose_name = "Фотоальбом"
        verbose_name_plural = "Фотоальбомы"


class Comments(models.Model):
    product_comment = models.ForeignKey('Product', on_delete=models.CASCADE, null=True, blank=True, verbose_name='key',
                                        related_name='comments_product')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор комментария', blank=True,
                               null=True)
    time_created = models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')
    text = models.TextField(verbose_name="Текст комментария")
    status = models.BooleanField(verbose_name="Видимость статьи", default=False)

    def __str__(self):
        return self.author

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"

