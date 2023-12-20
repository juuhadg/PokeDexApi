from django.db import models
from django.contrib.postgres.fields import ArrayField

# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=50)


class Pokemon(models.Model):
    name = models.CharField(max_length=20)
    types = ArrayField(models.CharField(max_length=20), blank=True, null=True)
    image = models.CharField(max_length=200)
    height = models.DecimalField(max_digits=10, decimal_places=2)
    weight = models.DecimalField(max_digits=10, decimal_places=2)