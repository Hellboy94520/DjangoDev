from django.shortcuts import render
from django.http import HttpResponse

from .models import *

# Create your views here.
def home(request):


  lCatData = CategoryData.objects.create(nameFr="Test 1", nameEn="Tst 1")
  lCatStat = CategoryStat.objects.create()
  Category.objects.create(data=lCatData, stat=lCatStat)




  lCategoryList = Category.objects.all()
  print("Taille catégory = {}".format(len(lCategoryList)))
  for lCategory in lCategoryList:
    print("Nom de la catégory = {}".format(lCategory.data.nameFr))

  return HttpResponse("Bonjour !")