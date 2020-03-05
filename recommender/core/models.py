from django.db import models

# Create your models here.

class UserModel(models.Model):
    name = models.CharField('Nombre', max_length=60)