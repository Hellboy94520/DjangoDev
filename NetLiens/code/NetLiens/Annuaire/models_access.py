from .models import *
from .log import *
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned

lClassName = "models_access"

""" --------------------------------------------------------------------------------------------------------------------
Category
-------------------------------------------------------------------------------------------------------------------- """
def create_category(pNameFr, pNameEn, pResumeFr, pResumeEn):
  lFunctionName = "create_category"

  if type(pNameFr) is not str:    return error_message(lClassName, lFunctionName, "pNameFr is not a str")
  if type(pNameEn) is not str:    return error_message(lClassName, lFunctionName, "pNameEn is not a str")
  if type(pResumeFr) is not str:  return error_message(lClassName, lFunctionName, "pResumeFr is not a str")
  if type(pResumeEn) is not str:  return error_message(lClassName, lFunctionName, "pResumeEn is not a str")

  lCategoryStat = CategoryStat()
  lCategoryStat.save()

  lCategory = Category()
  lCategory.nameFr   = pNameFr
  lCategory.nameEn   = pNameEn
  lCategory.resumeFr = pResumeFr
  lCategory.resumeEn = pResumeEn
  lCategory.stat     = lCategoryStat
  lCategory.save()


  return lCategory


""" --------------------------------------------------------------------------------------------------------------------
Localisation
-------------------------------------------------------------------------------------------------------------------- """
def create_continent(pNameFr, pNameEn, pCode):
  lFunctionName = "create_continent"

  if type(pNameFr) is not str: return error_message(lClassName, lFunctionName, "pNameFr is not a str")
  if type(pNameEn) is not str: return error_message(lClassName, lFunctionName, "pNameEn is not a str")
  if type(pCode)   is not str: return error_message(lClassName, lFunctionName, "pCode is not a str")
  if len(pCode) != 3         : return error_message(lClassName, lFunctionName, "pCode has not a size of 3 : {}"
                                                    .format(pCode))

  if LocalisationContinent.objects.filter(nameFr=pNameFr).count() != 0:
    return error_message(lClassName, lFunctionName, "Continent with NameFr \"{}\" already exist".format(pNameFr))
  if LocalisationContinent.objects.filter(nameEn=pNameEn).count() != 0:
    return error_message(lClassName, lFunctionName, "Continent with NameEn \"{}\" already exist".format(pNameEn))
  if LocalisationContinent.objects.filter(code=pCode).count() != 0:
    return error_message(lClassName, lFunctionName, "Continent with code \"{}\" already exist".format(pCode))

  lStat = LocalisationStat()
  lStat.save()

  lContinent = LocalisationContinent()
  lContinent.nameFr = pNameFr
  lContinent.nameEn = pNameEn
  lContinent.code   = pCode
  lContinent.stat   = lStat
  lContinent.save()

  return lContinent


""" ---------------------------------------------------------------------------------------------------------------- """
def create_country(pNameFr, pNameEn, pCode, pContinentNameFr):
  lFunctionName = "create_country"

  if type(pNameFr)          is not str: return error_message(lClassName, lFunctionName, "pNameFr is not a str")
  if type(pNameEn)          is not str: return error_message(lClassName, lFunctionName, "pNameEn is not a str")
  if type(pCode)            is not str: return error_message(lClassName, lFunctionName, "pCode is not a str")
  if len(pCode) < 3                   : return error_message(lClassName, lFunctionName, "pCode has not a size of 3 : {}"
                                                             .format(pCode))
  if type(pContinentNameFr) is not str: return error_message(lClassName, lFunctionName, "pContinentNameFr is not a str")

  if LocalisationCountry.objects.filter(nameFr=pNameFr).count() != 0:
    return error_message(lClassName, lFunctionName, "Country with NameFr \"{}\" already exist".format(pNameFr))
  if LocalisationCountry.objects.filter(nameEn=pNameFr).count() != 0:
    return error_message(lClassName, lFunctionName, "Country with NameEn \"{}\" already exist".format(pNameEn))
  if LocalisationCountry.objects.filter(code=pNameFr).count() != 0:
    return error_message(lClassName, lFunctionName, "Country with code \"{}\" already exist".format(pCode))

  try:
    lParent = LocalisationContinent.objects.get(nameFr=pContinentNameFr)
  except ObjectDoesNotExist:
    return error_message(lClassName, lFunctionName, "Impossible to find Continent with nameFr={}"
                         .format(pContinentNameFr))
  except MultipleObjectsReturned:
    return error_message(lClassName, lFunctionName, "Too much ContinentParent find ({}) with name={}"
                         .format(len(lParent), pContinentNameFr))
  except IOError as e:
    return error_message(lClassName, lFunctionName, "Unexpected error to find ContinentParent {}".format(e))

  lStat = LocalisationStat()
  lStat.save()

  lCountry = LocalisationCountry()
  lCountry.nameFr = pNameFr
  lCountry.nameEn = pNameEn
  lCountry.code   = pCode
  lCountry.stat   = lStat
  lCountry.save()

  lParent.children.add(lCountry)
  lParent.save()

  return lCountry


""" ---------------------------------------------------------------------------------------------------------------- """
def create_region(pName, pCode, pCountryNameFr):
  lFunctionName = "create_region"

  if type(pName)          is not str: return error_message(lClassName, lFunctionName, "pNameFr is not a str")
  if type(pCode)          is not str: return error_message(lClassName, lFunctionName, "pNameEn is not a str")
  if type(pCountryNameFr) is not str: return error_message(lClassName, lFunctionName, "pCountryName is not a str")

  if LocalisationRegion.objects.filter(name=pName).count() != 0:
    return error_message(lClassName, lFunctionName, "Region with Name \"{}\" already exist".format(pName))
  if LocalisationRegion.objects.filter(code=pCode).count() != 0:
    return error_message(lClassName, lFunctionName, "Region with Code \"{}\" already exist".format(pCode))

  try:
    lParent = LocalisationRegion.objects.get(name=pCountryNameFr)
  except ObjectDoesNotExist:
    return error_message(lClassName, lFunctionName, "Impossible to find Country with nameFr={}"
                         .format(pCountryNameFr))
  except MultipleObjectsReturned:
    return error_message(lClassName, lFunctionName, "Too much Country find ({}) with name={}"
                         .format(len(lParent), pCountryNameFr))
  except IOError as e:
    return error_message(lClassName, lFunctionName, "Unexpected error to find Country {}".format(e))

  lStat = LocalisationStat()
  lStat.save()

  lRegion = LocalisationRegion()
  lRegion.name = pName
  lRegion.code = pCode
  lRegion.stat = lStat
  lRegion.save()

  lParent.children.add(lRegion)
  lParent.save()
