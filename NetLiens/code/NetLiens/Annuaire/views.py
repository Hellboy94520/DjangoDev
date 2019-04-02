from django.shortcuts import render
from django.http import HttpResponse

from .models import *
from .models_access import *

# Create your views here.
def home(request):
  """
  lCategory = create_category("Test 1", "Test 1", "C'est un test", "This is a test")
  if lCategory is False: return HttpResponse("Erreur {} !".format(lCategory.data.nameFr))


  lCategoryChildren = create_category("Enfant 1", "Children 1", "C'est un test enfant",
                                      "This is a children test")
  if lCategoryChildren is False: return HttpResponse("Erreur {} !".format(lCategoryChildren.data.nameFr))
  lCategory.children.add(lCategoryChildren)


  lCategoryChildren2 = create_category("Enfant 2", "Children 2", "C'est un test enfant",
                                      "This is a children test")
  if lCategoryChildren2 is False: return HttpResponse("Erreur {} !".format(lCategoryChildren2.data.nameFr))
  lCategory.children.add(lCategoryChildren2)


  lCategoryChildrenChildren1 = create_category("Enfant 1-1", "Children 1-1", "C'est un test enfant",
                                      "This is a children test")
  if lCategoryChildrenChildren1 is False: return HttpResponse("Erreur {} !".format(lCategoryChildrenChildren1.data.nameFr))
  lCategoryChildren.children.add(lCategoryChildrenChildren1)


  lCategoryChildrenChildren2 = create_category("Enfant 1-2", "Children 1-2", "C'est un test enfant",
                                      "This is a children test")
  if lCategoryChildrenChildren2 is False: return HttpResponse("Erreur {} !".format(lCategoryChildrenChildren2.data.nameFr))
  lCategoryChildren.children.add(lCategoryChildrenChildren2)
  """

  lEurope = create_continent("Europe", "Europe", "EUR")
  if type(lEurope) is not LocalisationContinentData:
    return HttpResponse(lEurope)

  lAfrica = create_continent("Afrique", "Africa", "AFR")
  if type(lAfrica) is not LocalisationContinentData:
    return HttpResponse(lAfrica)

  lFrance = create_country("France", "France", "FRA", "Europe")
  if type(lFrance) is not LocalisationCountryData:
    return HttpResponse(lFrance)

  lAllemagne = create_country("Allemagne", "Germany", "GER", "Euro")
  if type(lAllemagne) is not LocalisationCountryData:
    return HttpResponse(lAllemagne)

  return HttpResponse("Bonjour !")