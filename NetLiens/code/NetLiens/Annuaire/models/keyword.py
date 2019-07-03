from django.db import models


""" --------------------------------------------------------------------------------------------------------------------
------------------------------------------------------------------------------------------------------------------------
Class
------------------------------------------------------------------------------------------------------------------------
-------------------------------------------------------------------------------------------------------------------- """
class Keyword(models.Model):
	objects = None
	nameFr = models.CharField(max_length=20, unique=True, default="")
	nameEn = models.CharField(max_length=20, unique=True, default="")


""" --------------------------------------------------------------------------------------------------------------------
------------------------------------------------------------------------------------------------------------------------
Functions
------------------------------------------------------------------------------------------------------------------------
-------------------------------------------------------------------------------------------------------------------- """
def create_new_keyword(pWord: str):
	# Lower the string
	lWord = pWord.lower()

	# Search if the keyword already exist or not
	lResult = Keyword.objects.filter(nameFr=lWord)

	# If already exist
	if lResult.count() == 1: return lResult[0]

	# If not
	lKeyword = Keyword()
	lKeyword.nameFr = lWord
	lKeyword.nameEn = lWord
	lKeyword.save()
	return lKeyword


""" ---------------------------------------------------------------------------------------------------------------- """
def is_exist(pWord: str):
	# Lower the string
	pWord = pWord.lower()

	# Search if the keyword already exist or not
	lResult = Keyword.objects.filter(nameFr=pWord)
	if lResult.count() == 1:
		return lResult[0]
	return None
