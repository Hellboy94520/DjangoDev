from django.urls import path
from . import views

urlpatterns = [
  path('', views.home, name='accueil'),

  #TODO: Pour exemple, a supprimer plus tard
  path('create_category', views.create_example_category),
  path('delete_category', views.delete_category),
  path('conversion', views.conversion)
]
