from django.db import models
from datetime import datetime
from .account import AccountAdmin
from enum import Enum


""" --------------------------------------------------------------------------------------------------------------------
------------------------------------------------------------------------------------------------------------------------
Data
------------------------------------------------------------------------------------------------------------------------
-------------------------------------------------------------------------------------------------------------------- """


""" ---------------------------------------------------------------------------------------------------------------- """
CreationText      = "Creation: "
ModificationText  = "Modification: "
DeletionText      = "Deletion: "


""" --------------------------------------------------------------------------------------------------------------------
------------------------------------------------------------------------------------------------------------------------
Enum
------------------------------------------------------------------------------------------------------------------------
-------------------------------------------------------------------------------------------------------------------- """
class Status(Enum):
  UN = "Unknown"
  AC = "Active"     # Show on the website
  UA = "Unactive"   # Unshow on the website and preserve the data
  TR = "Trash"      # Put the data in the trash and delete after a time


""" --------------------------------------------------------------------------------------------------------------------
------------------------------------------------------------------------------------------------------------------------
Class
------------------------------------------------------------------------------------------------------------------------
-------------------------------------------------------------------------------------------------------------------- """
class Log(models.Model):
	date = models.DateTimeField(default=datetime.now())
	modif = models.TextField()

	class Meta:
		abstract = True


class LogAdmin(Log):
	user   = models.ForeignKey(AccountAdmin, on_delete=models.SET_NULL, null=True)

	class Meta:
		abstract = True

"""
class LogAll(Log):
	user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

	class Meta:
		abstract = True
"""

""" ---------------------------------------------------------------------------------------------------------------- """
class Stat(models.Model):
  last1yConsu = models.IntegerField(default=0)
  last1mConsu = models.IntegerField(default=0)
  last1wConsu = models.IntegerField(default=0)
  last1dConsu = models.IntegerField(default=0)

  class Meta:
    abstract = True

  def add_oneview(self):
	  self.last1dConsu += 1
	  self.last1wConsu += 1
	  self.last1mConsu += 1
	  self.last1yConsu += 1
	  self.save()
