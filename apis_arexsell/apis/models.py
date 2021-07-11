from django.db import models

# Create your models here.


class User(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20)
    password = models.CharField(max_length=100)
    email = models.EmailField()


class Product(models.Model):
    id = models.AutoField(primary_key=True)
    value = models.FloatField()
    amount = models.IntegerField()
    name = models.CharField(max_length=30)
