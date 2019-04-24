from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404, Http404

from .models import *
from .models_access import *

from .porting import launch_conversion

import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)



# Create your views here.
def home(request):

  categoryList = get_much_see_category("last1mConsu", 6, True)

  return render(request, 'homepage.html', {'pCategoryList': categoryList})


# TODO: Temporary to have objects
def create_example_category(request):

  Audi   = create_category("Audi", "Audi", "", "")
  Audi.stat.last1mConsu = 8
  Audi.stat.save()

  BMW  = create_category("BMW", "BMW", "", "")
  BMW.stat.last1mConsu = 10
  BMW.stat.save()

  A6  = create_category("A6", "A6", "", "")
  A3 = create_category("A3", "A3", "", "")

  Audi.children.add(A6)
  Audi.children.add(A3)
  Audi.save()

  Serie1 = create_category("Serie 1", "Serie 1", "", "")
  Serie2 = create_category("Serie 2", "Serie 2", "", "")

  BMW.children.add(Serie1)
  BMW.children.add(Serie2)

  lCategory = create_category("Automobile", "Automobile", "", "")
  lCategory.children.add(Audi)
  lCategory.children.add(BMW)

  print(len(Category.objects.all()))

  return HttpResponse("Creation des categories effectuées")

def delete_category(request):

  lCategory = Category.objects.filter(nameFr="Audi")

  lCategory.delete()

  return HttpResponse("Delete Audi Category")


def conversion(request):
  logger.debug("[Porting] Starting...")

  lresult = launch_conversion()

  logger.debug("[Porting] Done")
  return HttpResponse(lresult)
