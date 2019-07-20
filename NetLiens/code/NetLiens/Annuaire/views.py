from django.shortcuts import render
from django.http import HttpResponse
# from django.shortcuts import render, redirect, get_object_or_404, Http404
from .models import Category
from .models import User
from .models import Localisation, LocalisationType
from .porting import main_portage

from .test.models_test import run


#from .porting import launch_conversion

import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.
def home(request):
  # categoryList = category.get_much_see_category("last1mConsu", 6, True)
  # return render(request, 'homepage.html', {'pCategoryList': categoryList})
  return HttpResponse("ok")


def test(request):
  run()



  return HttpResponse("Test OK")


# TODO: Temporary to have objects
def create_example_category(request):
  #
  # if account.AccountAdmin.objects.filter().count() == 0:
  #   lAccount = account.create_admin("Hellboy", "Alex", "Delahaye", "alexandre.delahaye@free.fr", "toto", True)
  #   if type(lAccount) is not account.AccountAdmin:
  #     return HttpResponse(lAccount)
  # else:
  #   lAccount = account.AccountAdmin.objects.filter(username="Hellboy")[0]
  #
  # lValidAccount = account.create_valid("Valid", "Alex", "Delahaye", "valid@free.fr", "toto", True, lAccount)
  # if type(lAccount) is not account.AccountAdmin:
  #   return HttpResponse(lValidAccount)
  return HttpResponse("Creation des categories effectuées")

def delete_category(request):
  # lCategory = Category.objects.filter(nameFr="Audi")
  # lCategory.delete()
  return HttpResponse("Delete Audi Category")


def conversion(request):
  logger.debug("[Porting] Starting...")

  main_portage.launch_conversion()

  lResponse  = "Total Category: {}<br/>".format(Category.objects.count())
  lResponse += "- Category Show   : {}<br/>".format(len(Category.objects.filter(display=True )))
  lResponse += "- Category Unshow : {}<br/>".format(len(Category.objects.filter(display=False)))
  for lCategory in Category.objects.filter(display=False):
    for lLog in lCategory.get_logs():
      lResponse += "-- Category '{}' is not show'<br/>".format(lCategory.nameFr)
  lResponse += "Total Localisation: {}<br/>".format(Localisation.objects.count())
  lResponse += "- Continent: {}<br/>".format(len(Localisation.objects.filter(type=LocalisationType.CO)))
  lResponse += "- Country  : {}<br/>".format(len(Localisation.objects.filter(type=LocalisationType.CU)))
  lResponse += "- RegionFr : {}<br/>".format(len(Localisation.objects.filter(type=LocalisationType.RE)))
  lResponse += "- DepartFr : {}<br/>".format(len(Localisation.objects.filter(type=LocalisationType.DE)))
  lResponse += "- CitiesFr : {}<br/>".format(len(Localisation.objects.filter(type=LocalisationType.CI)))

  logger.debug("[Porting] Done\n {}".format(lResponse) )

  return HttpResponse(lResponse)

def reset(request):
  User.objects.all().delete()
  Category.objects.all().delete()
  Localisation.objects.all().delete()

  return HttpResponse("Database is clean")
