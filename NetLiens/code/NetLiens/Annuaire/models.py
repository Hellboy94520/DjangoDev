
from django.db import models
import datetime

# Create your models here.

""" --------------------------------------------------------------------------------------------------------------------
Category
-------------------------------------------------------------------------------------------------------------------- """
class CategoryData(models.Model):
  nameFr    = models.CharField(max_length=100, default="")
  nameEn    = models.CharField(max_length=100, default="")
  resume    = models.TextField(default="")

  def __str__(self):
    return self.nameFr

class CategoryStat(models.Model):
  creationDate  = models.DateTimeField(default=datetime.datetime.now())
  lastModDate   = models.DateTimeField(default=datetime.datetime.now())
  lastModUser   = models.CharField(max_length=100, default="default")
  last1dConsu   = models.IntegerField(default=0)
  last1mConsu   = models.IntegerField(default=0)
  last1wConsu   = models.IntegerField(default=0)
  last1dConsu   = models.IntegerField(default=0)

  def __str__(self):
    return self.creationDate

class Category(models.Model):
  status  = models.BooleanField(default=False)
  data    = models.OneToOneField(CategoryData, on_delete=models.CASCADE, primary_key=True)
  stat    = models.ForeignKey(CategoryStat, on_delete=models.CASCADE)

  def __str__(self):
    return self.status