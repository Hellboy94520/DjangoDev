
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
import datetime

nameSizeMax = 100
userSizeMax = 100


# Create your models here.

""" --------------------------------------------------------------------------------------------------------------------
Category
-------------------------------------------------------------------------------------------------------------------- """
class CategoryStat(models.Model):
  creationDate  = models.DateTimeField(default=datetime.datetime.now())
  lastModDate   = models.DateTimeField(default=datetime.datetime.now())
  lastModUser   = models.CharField(max_length=nameSizeMax, default="creation")
  last1dConsu   = models.IntegerField(default=0)
  last1mConsu   = models.IntegerField(default=0)
  last1wConsu   = models.IntegerField(default=0)
  last1dConsu   = models.IntegerField(default=0)
  

class Category(models.Model):
  nameFr    = models.CharField(max_length=nameSizeMax, default="")
  nameEn    = models.CharField(max_length=nameSizeMax, default="")
  resumeFr  = models.TextField(default="")
  resumeEn  = models.TextField(default="")
  stat      = models.OneToOneField(CategoryStat, on_delete=models.CASCADE, primary_key=True)
  children  = models.ManyToManyField('self', related_name='ChildrenCategory')



""" --------------------------------------------------------------------------------------------------------------------
Localisation
-------------------------------------------------------------------------------------------------------------------- """
class LocalisationStat(models.Model):
  creationDate  = models.DateTimeField(default=datetime.datetime.now())
  lastModDate   = models.DateTimeField(default=datetime.datetime.now())
  lastModUser   = models.CharField(max_length=userSizeMax, default="default")
  last1dConsu   = models.IntegerField(default=0)
  last1mConsu   = models.IntegerField(default=0)
  last1wConsu   = models.IntegerField(default=0)
  last1dConsu   = models.IntegerField(default=0)


class LocalisationCity(models.Model):
  name          = models.CharField(max_length=nameSizeMax)
  stat          = models.OneToOneField(LocalisationStat, on_delete=models.CASCADE, primary_key=True)

  def __repr__(self):
    return "Name={}".format(self.name)


class LocalisationDepartment(models.Model):
  name          = models.CharField(max_length=nameSizeMax)
  code          = models.SmallIntegerField()
  children      = models.ManyToManyField(LocalisationCity)
  stat          = models.OneToOneField(LocalisationStat, on_delete=models.CASCADE, primary_key=True)

  def __repr__(self):
    return "Name={}, number={}".format(self.name, self.number)


class LocalisationRegion(models.Model):
  name          = models.CharField(max_length=nameSizeMax)
  code          = models.SmallIntegerField()
  children      = models.ManyToManyField(LocalisationDepartment)
  stat          = models.OneToOneField(LocalisationStat, on_delete=models.CASCADE, primary_key=True)

  def __repr__(self):
    return "Name={}, number={}".format(self.name, self.number)


class LocalisationCountry(models.Model):
  nameFr        = models.CharField(max_length=nameSizeMax)
  nameEn        = models.CharField(max_length=nameSizeMax)
  code          = models.CharField(max_length=3)
  children      = models.ManyToManyField(LocalisationRegion)
  stat          = models.OneToOneField(LocalisationStat, on_delete=models.CASCADE, primary_key=True)

  def __repr__(self):
    return "NameFr={}, code={}".format(self.nameEn, self.code)


class LocalisationContinent(models.Model):
  nameFr        = models.CharField(max_length=nameSizeMax)
  nameEn        = models.CharField(max_length=nameSizeMax)
  code          = models.CharField(max_length=3)
  children      = models.ManyToManyField(LocalisationCountry)
  stat          = models.OneToOneField(LocalisationStat, on_delete=models.CASCADE, primary_key=True)

  def __repr__(self):
    return "NameFr={}, code={}".format(self.nameEn, self.code)
