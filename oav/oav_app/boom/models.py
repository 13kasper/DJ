from django.db import models


class Boom(models.Model):
    title = models.CharField(max_length=100)
    price = models.CharField(max_length=100)
    articles = models.CharField(max_length=100)
    description = models.CharField(max_length=250)
    description_full = models.CharField(max_length=250)
    only = models.BooleanField(default=True)
    image = models.ImageField(upload_to='booms/images/')  # upload_to = путь к папке изображений
    rating = models.ImageField(upload_to='booms/images/', default='')  # upload_to = путь к папке изображений
    image2 = models.ImageField(upload_to='booms/images/', default='')  # upload_to = путь к папке изображений
    url = models.URLField(blank=True)  # blank=True -- отменяет обязательное заполнение

    def __str__(self):
        return self.title


class Menus(models.Model):
    link = models.CharField(max_length=20)



