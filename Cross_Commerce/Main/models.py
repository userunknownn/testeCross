from django.db import models

# Create your models here.

class Numbers(models.Model):

    number = models.DecimalField(decimal_places=25, max_digits=10000)
