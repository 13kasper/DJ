from django.db import models


class Skills(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=250)
    image = models.ImageField(upload_to='skills/images/')  # upload_to = путь к папке изображений
    url = models.URLField(blank=True)  # blank=True -- отменяет обязательное заполнение

    def __str__(self):
        return self.title
