from django.urls import path
from . import views

urlpatterns = [
  path('', views.home, name='accueil'),
	path('search', views.search, name='search'),
	path('signup', views.signup),
	path('category', views.all_category),
	path('category/<name_category>', views.category, name='accueil'),
	path('contact', views.contact, name='contact'),
]