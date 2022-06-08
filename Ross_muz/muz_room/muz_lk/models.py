from django.db import models
from django.urls import reverse


class Muz(models.Model):
    author = models.CharField(max_length=100, verbose_name='Автор')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")
    song = models.CharField(max_length=100, verbose_name='Название песни')
    audio_file = models.FileField(upload_to='mp3/')
    time_created = models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')
    cat = models.ForeignKey('Category', on_delete=models.PROTECT, verbose_name='Категория')

    def __str__(self):
        return self.author

    class Meta:
        """Переводим админку на русский"""
        verbose_name = "Песня"
        verbose_name_plural = "Песни"
        ordering = ['-time_created']  # сортировка новостей


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


