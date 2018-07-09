from django.db import models

# Create your models here.
class ReverseIP(models.Model):
    dbl_latitude = models.FloatField()
    dbl_longitude = models.FloatField()
    txt_address = models.TextField()
    dat_created = models.DateField()
