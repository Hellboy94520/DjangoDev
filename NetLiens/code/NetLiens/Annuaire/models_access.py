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
  if type(pCode)          is not str: return error_message(lClassName, lFunctionName, "pCode is not a str")
  if type(pCountryNameFr) is not str: return error_message(lClassName, lFunctionName, "pCountryName is not a str")

  if LocalisationRegion.objects.filter(name=pName).count() != 0:
    return error_message(lClassName, lFunctionName, "Region with Name \"{}\" already exist".format(pName))
  if LocalisationRegion.objects.filter(code=pCode).count() != 0:
    return error_message(lClassName, lFunctionName, "Region with Code \"{}\" already exist".format(pCode))

  try:
    lParent = LocalisationCountry.objects.get(nameFr=pCountryNameFr)
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

  return lRegion


""" ---------------------------------------------------------------------------------------------------------------- """


def create_departement(pName, pCode, pRegionName):

  lFunctionName = "create_departement"

  if type(pName)          is not str: return error_message(lClassName, lFunctionName, "pNameFr is not a str")
  if type(pCode)          is not str: return error_message(lClassName, lFunctionName, "pCode is not a str")
  if type(pRegionName)    is not str: return error_message(lClassName, lFunctionName, "pRegionName is not a str")

  if LocalisationRegion.objects.filter(name=pName).count() != 0:
    return error_message(lClassName, lFunctionName, "Departement with Name \"{}\" already exist".format(pName))
  if LocalisationRegion.objects.filter(code=pCode).count() != 0:
    return error_message(lClassName, lFunctionName, "Departement with Code \"{}\" already exist".format(pCode))

  try:
    lParent = LocalisationRegion.objects.get(name=pRegionName)
  except ObjectDoesNotExist:
    return error_message(lClassName, lFunctionName, "Impossible to find the region name={}".format(pRegionName))
  except MultipleObjectsReturned:
    return error_message(lClassName, lFunctionName, "Too much Region find ({}) with name={}"
                         .format(len(lParent), pRegionName))
  except IOError as e:
    return error_message(lClassName, lFunctionName, "Unexpected error to find Region {}".format(e))

  lStat = LocalisationStat()
  lStat.save()

  lDepartement = LocalisationDepartment()
  lDepartement.name = pName
  lDepartement.code = pCode
  lDepartement.stat = lStat
  lDepartement.save()

  lParent.children.add(lDepartement)
  lParent.save()

  return lDepartement


""" ---------------------------------------------------------------------------------------------------------------- """


def create_city(pName, pDepartmentName):

  lFunctionName = "create_city"

  if type(pName)          is not str: return error_message(lClassName, lFunctionName, "pNameFr is not a str")
  if type(pDepartmentName)is not str: return error_message(lClassName, lFunctionName, "pDepartmentName is not a str")

  if LocalisationCity.objects.filter(name=pName).count() != 0:
    return error_message(lClassName, lFunctionName, "City with name={} already exist".format(pName))

  try:
    lParent = LocalisationRegion.objects.get(name=pDepartmentName)
  except ObjectDoesNotExist:
    return error_message(lClassName, lFunctionName, "Impossible to find the Department name={}".format(pDepartmentName))
  except MultipleObjectsReturned:
    return error_message(lClassName, lFunctionName, "Too much Department find ({}) with name={}"
                         .format(len(lParent), pDepartmentName))
  except IOError as e:
    return error_message(lClassName, lFunctionName, "Unexpected error to find Department {}".format(e))

  lStat = LocalisationStat()
  lStat.save()

  lCity = LocalisationCity()
  lCity.name = pName
  lCity.save()

  lParent.children.save(lCity)
  lParent.save()


""" --------------------------------------------------------------------------------------------------------------------
Payment
-------------------------------------------------------------------------------------------------------------------- """


def check_payment(pFunctionName, pReference, pDetails, pDate, pSum, pNLDict, pPaypalRef):

  if type(pReference)    is not str: return error_message(lClassName, pFunctionName, "pUsername is not a str")
  if type(pDetails)      is not str: return error_message(lClassName, pFunctionName, "pDetails is not a datetime")
  if type(pDate)         is not datetime: return error_message(lClassName, pFunctionName, "pDate is not a datetime")
  if type(pSum)          is not int: return error_message(lClassName, pFunctionName, "pSum is not an integer")
  if type(pNLDict)       is not dict: return error_message(lClassName, pFunctionName, "pNLDict is not a dictionnary")
  if type(pPaypalRef)    is not str: return error_message(lClassName, pFunctionName, "pPaypalRef is not a str")

  return True


""" ---------------------------------------------------------------------------------------------------------------- """


def create_paypal_payment(pReference, pDetails, pDate, pSum, pNLDict, pPaypalRef):

  lFunctionName = "create_paypal_payment"

  result = check_payment(lFunctionName, pReference, pDetails, pDate, pSum, pNLDict, pPaypalRef)
  if result is not True:
    return result

  lPaypalPayment = PaypalPayment()
  lPaypalPayment.reference  = pPaypalRef
  lPaypalPayment.save()

  lPayment = Payment()
  lPayment.reference  = pReference
  lPayment.datetime   = pDate
  lPayment.sum        = pSum
  lPayment.type       = Payment.PAYPAL
  lPayment.details    = pDetails

  for nl, quantity in pNLDict.items():
    lNLPurcharse = NLPurchase()
    lNLPurcharse.level    = nl
    lNLPurcharse.quantity = quantity
    lNLPurcharse.save()
    
    lPayment.purchase.add(lNLPurcharse)

  lPayment.save()


""" ---------------------------------------------------------------------------------------------------------------- """


def create_gift_payment(pReference, pDetails, pDate, pSum, pNLDict):

  lFunctionName = "create_gift_payment"

  result = check_payment(lFunctionName, pReference, pDetails, pDate, pSum, pNLDict, "")
  if result is not True:
    return result

  lPayment = Payment()
  lPayment.reference  = pReference
  lPayment.datetime   = pDate
  lPayment.sum        = pSum
  lPayment.type       = Payment.GIFT
  lPayment.details    = pDetails

  for nl, quantity in pNLDict.items():
    lNLPurcharse = NLPurchase()
    lNLPurcharse.level = nl
    lNLPurcharse.quantity = quantity
    lNLPurcharse.save()

    lPayment.purchase.add(lNLPurcharse)

  lPayment.save()


""" --------------------------------------------------------------------------------------------------------------------
Account
-------------------------------------------------------------------------------------------------------------------- """


def check_account_data(pFunctionName, pUsername, pEmail, pPassword, pFirstName, pLastName, pCompany):

  if type(pUsername)    is not str: return error_message(lClassName, pFunctionName, "pUsername is not a str")
  if type(pEmail)       is not str: return error_message(lClassName, pFunctionName, "pEmail is not a str")
  if type(pPassword)    is not str: return error_message(lClassName, pFunctionName, "pPassword is not a str")
  if type(pFirstName)   is not str: return error_message(lClassName, pFunctionName, "pFirstName is not a str")
  if type(pLastName)    is not str: return error_message(lClassName, pFunctionName, "pLastName is not a str")
  if type(pCompany)     is not str: return error_message(lClassName, pFunctionName, "pCompany is not a str")

  if User.objects.filter(username=pUsername).exists() :
    return error_message(lClassName, pFunctionName, "Username already exists")
  if User.objects.filter(email=pEmail).exists() :
    return error_message(lClassName, pFunctionName, "Email already exists")

  return True


""" ---------------------------------------------------------------------------------------------------------------- """


def create_user_account(pUsername, pEmail, pPassword, pFirstName, pLastName, pCompany):

  lFunctionName = "create_user_account"

  result = check_account_data(lFunctionName, pUsername, pEmail, pPassword, pFirstName, pLastName, pCompany)
  if result is not True:
    return result

  try:
    user  = User.objects.create_user(pUsername, pEmail, pPassword)
  except IOError as e:
    return error_message(lClassName, lFunctionName, "Impossible to create User : {}".format(e))

  user.first_name, user.last_name = pFirstName, pLastName
  user.is_staff, user.is_active, is_superuser = False, False, False  # Account unactivate until the email confirmation
  user.save()

  lActivation = AccountActivation()
  lActivation.save()

  lAccount = Account()
  lAccount.user       = user
  lAccount.company    = pCompany
  lAccount.activation = lActivation
  lAccount.save()


""" ---------------------------------------------------------------------------------------------------------------- """


def create_valid_account(pUsername, pEmail, pPassword, pFirstName, pLastName):

  lFunctionName = "create_valid_account"

  result = check_account_data(lFunctionName, pUsername, pEmail, pPassword, pFirstName, pLastName, "")
  if result is not True:
    return result

  try:
    user = User.objects.create_user(pUsername, pEmail, pPassword)
  except IOError as e:
    return error_message(lClassName, lFunctionName, "Impossible to create User : {}".format(e))

  user.first_name, user.last_name = pFirstName, pLastName
  user.is_staff, user.is_active, is_superuser = True, True, False  # No need verification mail
  user.save()

  lAccount = Account()
  lAccount.user = user
  lAccount.save()


""" ---------------------------------------------------------------------------------------------------------------- """


def create_admin_account(pUsername, pEmail, pPassword, pFirstName, pLastName):

  lFunctionName = "create_valid_account"

  result = check_account_data(lFunctionName, pUsername, pEmail, pPassword, pFirstName, pLastName, "")
  if result is not True:
    return result

  try:
    user = User.objects.create_user(pUsername, pEmail, pPassword)
  except IOError as e:
    return error_message(lClassName, lFunctionName, "Impossible to create User : {}".format(e))

  user.first_name, user.last_name = pFirstName, pLastName
  user.is_staff, user.is_active, is_superuser = True, True, True  # No need verification mail
  user.save()

  lAccount = Account()
  lAccount.user = user
  lAccount.save()
