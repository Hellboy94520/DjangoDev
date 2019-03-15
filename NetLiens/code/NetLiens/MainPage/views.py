import logging

"Get an instance of a logger"
logger = logging.getLogger(__name__)

from django.shortcuts import render, redirect, get_object_or_404, Http404
from .forms import ContactForm, SearchForm
from .models import AnnuCats, AnnuSite, AnnuSiteAppartient

""" --------------------------------------------------------------------------------------------------------------------
Homepage
-------------------------------------------------------------------------------------------------------------------- """
def home(request):
  """ Get the 5 most category consulted """
  muchSeeList = [get_object_or_404(AnnuCats, cat_id=280),   # Voyage et Tourisme
                 get_object_or_404(AnnuCats, cat_id=286),   # Hébergement vacances
                 get_object_or_404(AnnuCats, cat_id=45),    # Gastronomie et Boissons
                 get_object_or_404(AnnuCats, cat_id=105),   # Auto-Moto
                 get_object_or_404(AnnuCats, cat_id=1812)]  # Animaux
  """ ------------ """
  return render(request, 'homepage.html', {'muchCatList': muchSeeList})

""" --------------------------------------------------------------------------------------------------------------------
Search
-------------------------------------------------------------------------------------------------------------------- """
def search(request):
  form = SearchForm(request.POST or None)

  return render(request, 'search.html', locals())

""" --------------------------------------------------------------------------------------------------------------------
Authentication page
-------------------------------------------------------------------------------------------------------------------- """
def signup(request):

  """ ------------ """
  return render(request, 'signup.html')



""" --------------------------------------------------------------------------------------------------------------------
Display categories
-------------------------------------------------------------------------------------------------------------------- """
def all_category(request):
  """ Get all primary category """
  categoryList = AnnuCats.objects.filter(cat_parent__contains=0)

  """ ------------ """
  return render(request, 'category.html', {'mainCategory': "Toutes les categories", 'categoryList': categoryList})


""" ---------------------------------------------------------------------------------------------------------------- """
def category(request, name_category):
  """ Get MainCategory and Subcategory """
  mainCategory = get_object_or_404(AnnuCats, cat_name=name_category)
  categoryList = AnnuCats.objects.filter(cat_parent=mainCategory.cat_id)

  """ Get Sites of MainCategory """
  # Search occurences between category id and site_id
  mainSiteAppCategoryList = AnnuSiteAppartient.objects.filter(app_cat_id=mainCategory.cat_id)

  # Get all sites match with category_id
  mainSiteCategoryList = []
  for mainSiteAppCategory in mainSiteAppCategoryList:
    mainSiteCategoryList.append(get_object_or_404(AnnuSite, site_id=mainSiteAppCategory.app_site_id))
  mainSiteCategoryList = mainSiteCategoryList[0:5]

  """ ------------ """
  return render(request, 'category.html', {'mainCategory': mainCategory.cat_name, 'categoryList': categoryList,
                                           'siteList': mainSiteCategoryList})



""" --------------------------------------------------------------------------------------------------------------------
Contact page
-------------------------------------------------------------------------------------------------------------------- """
def contact(request):
  form = ContactForm(request.POST or None)
  if form.is_valid():
    # cleaned_data est un dictionnaire contenant les informations de request
    name = form.cleaned_data['name']
    family_name = form.cleaned_data['family_name']
    email = form.cleaned_data['email']
    message = form.cleaned_data['message']
    copy = form.cleaned_data['message']

    #TODO : Send an email
    send = True
  else:
    send = False

  """ ------------ """
  return render(request, 'contact.html', locals())