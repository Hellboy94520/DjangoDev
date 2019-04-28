from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404, Http404

from .models import category, account, localisation

#from .porting import launch_conversion

import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.
def home(request):

  categoryList = get_much_see_category("last1mConsu", 6, True)

  return render(request, 'homepage.html', {'pCategoryList': categoryList})


# TODO: Temporary to have objects
def create_example_category(request):

  if account.AccountAdmin.objects.filter().count() == 0:
    lAccount = account.create_admin("Hellboy", "Alex", "Delahaye", "alexandre.delahaye@free.fr", "toto", True)
    if type(lAccount) is not account.AccountAdmin:
      return HttpResponse(lAccount)
  else:
    lAccount = account.AccountAdmin.objects.filter(username="Hellboy")[0]

  lValidAccount = account.create_valid("Valid", "Alex", "Delahaye", "valid@free.fr", "toto", True, lAccount)
  if type(lAccount) is not account.AccountAdmin:
    return HttpResponse(lValidAccount)



  return HttpResponse("Creation des categories effectuées")

def delete_category(request):
  """
  lCategory = Category.objects.filter(nameFr="Audi")

  lCategory.delete()
  """
  return HttpResponse("Delete Audi Category")


def conversion(request):
  """
  logger.debug("[Porting] Starting...")

  lresult = launch_conversion()

  logger.debug("[Porting] Done")

  return HttpResponse(lresult)"""
  return HttpResponse("OK")
