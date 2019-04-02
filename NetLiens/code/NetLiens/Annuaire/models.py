
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
#TODO: Voir si je regroupe pas tous dans CategoryData
class CategoryStat(models.Model):
  creationDate  = models.DateTimeField(default=datetime.datetime.now())
  lastModDate   = models.DateTimeField(default=datetime.datetime.now())
  lastModUser   = models.CharField(max_length=nameSizeMax, default="creation")
  last1dConsu   = models.IntegerField(default=0)
  last1mConsu   = models.IntegerField(default=0)
  last1wConsu   = models.IntegerField(default=0)
  last1dConsu   = models.IntegerField(default=0)
  

class CategoryData(models.Model):
  nameFr    = models.CharField(max_length=nameSizeMax, default="")
  nameEn    = models.CharField(max_length=nameSizeMax, default="")
  resumeFr  = models.TextField(default="")
  resumeEn  = models.TextField(default="")
  #stat      = models.OneToOneField(CategoryStat, on_delete=models.CASCADE, primary_key=True)

class Category(models.Model):
  data    = models.ForeignKey(CategoryData, related_name="CategoryData", on_delete=models.CASCADE)
  stat    = models.ForeignKey(CategoryStat, related_name="CategoryStat", on_delete=models.CASCADE)
  children= models.ManyToManyField("Category", related_name="ChildrenCategory")

  def __str__(self):
    return self.data.nameFr


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


class LocalisationCityData(models.Model):
  name          = models.CharField(max_length=nameSizeMax)
  stat          = models.OneToOneField(LocalisationStat, on_delete=models.CASCADE, primary_key=True)

  def __repr__(self):
    return "Name={}".format(self.name)


class LocalisationDepartmentData(models.Model):
  name          = models.CharField(max_length=nameSizeMax)
  code          = models.SmallIntegerField()
  children      = models.ManyToManyField(LocalisationCityData)
  stat          = models.OneToOneField(LocalisationStat, on_delete=models.CASCADE, primary_key=True)

  def __repr__(self):
    return "Name={}, number={}".format(self.name, self.number)


class LocalisationRegionData(models.Model):
  name          = models.CharField(max_length=nameSizeMax)
  code          = models.SmallIntegerField()
  children      = models.ManyToManyField(LocalisationDepartmentData)
  stat          = models.OneToOneField(LocalisationStat, on_delete=models.CASCADE, primary_key=True)

  def __repr__(self):
    return "Name={}, number={}".format(self.name, self.number)


class LocalisationCountryData(models.Model):
  nameFr        = models.CharField(max_length=nameSizeMax)
  nameEn        = models.CharField(max_length=nameSizeMax)
  code          = models.CharField(max_length=3)
  children      = models.ManyToManyField(LocalisationRegionData)
  stat          = models.OneToOneField(LocalisationStat, on_delete=models.CASCADE, primary_key=True)

  def __repr__(self):
    return "NameFr={}, code={}".format(self.nameEn, self.code)


class LocalisationContinentData(models.Model):
  nameFr        = models.CharField(max_length=nameSizeMax)
  nameEn        = models.CharField(max_length=nameSizeMax)
  code          = models.CharField(max_length=3)
  children      = models.ManyToManyField(LocalisationCountryData)
  stat          = models.OneToOneField(LocalisationStat, on_delete=models.CASCADE, primary_key=True)

  def __repr__(self):
    return "NameFr={}, code={}".format(self.nameEn, self.code)
