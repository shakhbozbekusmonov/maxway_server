from django.db import models

from common.models import Media, BaseModel


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Product(BaseModel):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    desc = models.TextField()
    price = models.FloatField()

    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    image = models.ForeignKey(Media, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

