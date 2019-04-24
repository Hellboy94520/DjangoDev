from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.core.validators import validate_email
from datetime import datetime, timedelta
from uuid import uuid4
from .log import *

UserMaxSize     = 100
CategorySize    = 100
PaypalRefSize   = 20
SiteTitleSize   = 50

lClassName = "models"


""" --------------------------------------------------------------------------------------------------------------------
------------------------------------------------------------------------------------------------------------------------
Category data
------------------------------------------------------------------------------------------------------------------------
-------------------------------------------------------------------------------------------------------------------- """


class CategoryStat(models.Model):
    creationDate  = models.DateTimeField(default=datetime.now())
    creationUser  = models.CharField(max_length=CategorySize, default="creation")
    lastModDate   = models.DateTimeField(default=datetime.now())
    lastModUser   = models.CharField(max_length=CategorySize, default="")
    last1yConsu   = models.IntegerField(default=0)
    last1mConsu   = models.IntegerField(default=0)
    last1wConsu   = models.IntegerField(default=0)
    last1dConsu   = models.IntegerField(default=0)


class CategoryData(models.Model):
    nameFr    = models.CharField(max_length=UserMaxSize, default="")
    nameEn    = models.CharField(max_length=UserMaxSize, default="")
    resumeFr  = models.TextField(max_length=50, default="")
    resumeEn  = models.TextField(max_length=50, default="")
    stat      = models.OneToOneField(CategoryStat, on_delete=models.CASCADE, primary_key=True)
    children  = models.ManyToManyField('self', related_name='ChildrenCategory')

    class Meta:
      abstract = True


class Category(CategoryData):

    def __repr__(self):
        return "Category: {} - {}".format(self.nameFr, self.nameEn)


class CategoryUnactive(CategoryData):

    def __repr__(self):
        return "CategoryUnactive: {} - {}".format(self.nameFr, self.nameEn)


""" --------------------------------------------------------------------------------------------------------------------
Category functions
-------------------------------------------------------------------------------------------------------------------- """


" --- Creation of category --- "
def create_category(pNameFr, pNameEn, pResumeFr, pResumeEn, pShow=True):

  lFunctionName = "create_category"
  if type(pNameFr)   is not str:    return error_message(lClassName, lFunctionName, "pNameFr is not a str"  )
  if type(pNameEn)   is not str:    return error_message(lClassName, lFunctionName, "pNameEn is not a str"  )
  if type(pResumeFr) is not str:    return error_message(lClassName, lFunctionName, "pResumeFr is not a str")
  if type(pResumeEn) is not str:    return error_message(lClassName, lFunctionName, "pResumeEn is not a str")
  if type(pShow)     is not bool:   return error_message(lClassName, lFunctionName, "pShow is not a boolean")

  lCategoryStat = CategoryStat()
  lCategoryStat.save()

  if pShow is True: lCategory = Category()
  else            : lCategory = CategoryUnactive()

  lCategory.nameFr   = pNameFr
  lCategory.nameEn   = pNameEn
  lCategory.resumeFr = pResumeFr
  lCategory.resumeEn = pResumeEn
  lCategory.stat     = lCategoryStat
  lCategory.save()
  return lCategory


" --- Get the much see category --- "
def get_much_see_category(pTimePeriod, pQuantity, pReverse=False):

  lFunctionName = "get_much_see_category"

  if type(pTimePeriod) is not str:    return error_message(lClassName, lFunctionName, "pTimePeriod is not a str")
  if type(pQuantity)   is not int:    return error_message(lClassName, lFunctionName, "pQuantity is not an integer")
  if type(pReverse)    is not bool:   return error_message(lClassName, lFunctionName, "pReverse is not a boolean")

  if pReverse is True: lParam = "-" + pTimePeriod
  else:                lParam = pTimePeriod

  try:
    categoryStatList = CategoryStat.objects.order_by(lParam)[0:pQuantity]
  except IOError as e:
    return error_message(lClassName, lFunctionName, e)

  categoryList = []

  for categoryStat in categoryStatList:
    categoryList.append(Category.objects.get(stat_id=categoryStat.id))

  return categoryList


""" --------------------------------------------------------------------------------------------------------------------
------------------------------------------------------------------------------------------------------------------------
Localisation data
------------------------------------------------------------------------------------------------------------------------
-------------------------------------------------------------------------------------------------------------------- """


class LocalisationStat(models.Model):
    creationDate  = models.DateTimeField(default=datetime.now())
    creationUser  = models.CharField(max_length=UserMaxSize, default="creation")
    lastModDate   = models.DateTimeField(default=datetime.now())
    lastModUser   = models.CharField(max_length=UserMaxSize, default="")
    last1yConsu   = models.IntegerField(default=0)
    last1mConsu   = models.IntegerField(default=0)
    last1wConsu   = models.IntegerField(default=0)
    last1dConsu   = models.IntegerField(default=0)


class LocalisationCity(models.Model):
    name          = models.CharField(max_length=UserMaxSize)
    stat          = models.OneToOneField(LocalisationStat, on_delete=models.CASCADE, primary_key=True)

    def __repr__(self):
        return "LocalisationCity : {}".format(self.name)


class LocalisationDepartment(models.Model):
    name          = models.CharField(max_length=UserMaxSize)
    code          = models.SmallIntegerField()
    children      = models.ManyToManyField(LocalisationCity)
    stat          = models.OneToOneField(LocalisationStat, on_delete=models.CASCADE, primary_key=True)

    def __repr__(self):
        return "LocalisationDepartment : {}".format(self.name)


class LocalisationRegion(models.Model):
    name          = models.CharField(max_length=UserMaxSize)
    code          = models.SmallIntegerField()
    children      = models.ManyToManyField(LocalisationDepartment)
    stat          = models.OneToOneField(LocalisationStat, on_delete=models.CASCADE, primary_key=True)

    def __repr__(self):
        return "LocalisationRegion : {}".format(self.name)


class LocalisationCountry(models.Model):
    nameFr        = models.CharField(max_length=UserMaxSize)
    nameEn        = models.CharField(max_length=UserMaxSize)
    code          = models.CharField(max_length=3, unique=True)
    children      = models.ManyToManyField(LocalisationRegion)
    stat          = models.OneToOneField(LocalisationStat, on_delete=models.CASCADE, primary_key=True)

    def __repr__(self):
        return "LocalisationCountry : {} - {}".format(self.nameFr, self.nameEn)


class LocalisationContinent(models.Model):
    nameFr        = models.CharField(max_length=UserMaxSize, unique=True)
    nameEn        = models.CharField(max_length=UserMaxSize, unique=True)
    code          = models.CharField(max_length=3, unique=True)
    children      = models.ManyToManyField(LocalisationCountry)
    stat          = models.OneToOneField(LocalisationStat, on_delete=models.CASCADE, primary_key=True)

    def __repr__(self):
        return "LocalisationContinent : {} - {}".format(self.nameFr, self.nameEn)


""" --------------------------------------------------------------------------------------------------------------------
Localisation functions
-------------------------------------------------------------------------------------------------------------------- """


" --- Creation of a continent  --- "
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


" --- Creation of a country  --- "
def create_country(pNameFr, pNameEn, pCode, pContinentNameFr=None):

  lFunctionName = "create_country"

  if type(pNameFr)          is not str: return error_message(lClassName, lFunctionName, "pNameFr is not a str")
  if type(pNameEn)          is not str: return error_message(lClassName, lFunctionName, "pNameEn is not a str")
  if type(pCode)            is not str: return error_message(lClassName, lFunctionName, "pCode is not a str")
  if len(pCode) != 3                  : return error_message(lClassName, lFunctionName, "pCode has not a size of 3 : {}"
                                                             .format(pCode))
  if type(pContinentNameFr) is not str: return error_message(lClassName, lFunctionName, "pContinentNameFr is not a str")

  if LocalisationCountry.objects.filter(nameFr=pNameFr).count() != 0:
    return error_message(lClassName, lFunctionName, "Country with NameFr \"{}\" already exist".format(pNameFr))
  if LocalisationCountry.objects.filter(nameEn=pNameFr).count() != 0:
    return error_message(lClassName, lFunctionName, "Country with NameEn \"{}\" already exist".format(pNameEn))
  if LocalisationCountry.objects.filter(code=pNameFr).count() != 0:
    return error_message(lClassName, lFunctionName, "Country with code \"{}\" already exist".format(pCode))

  lParent = None
  if pContinentNameFr != "":
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

  if lParent is not None:
    lParent.children.add(lCountry)
    lParent.save()

  return lCountry


" --- Creation of a region  --- "
def create_region(pName, pCode, pCountryNameFr):

  lFunctionName = "create_region"

  if type(pName)          is not str: return error_message(lClassName, lFunctionName, "pNameFr is not a str")
  if type(pCode)          is not str: return error_message(lClassName, lFunctionName, "pCode is not a str")
  if len(pCode) != 2                : return error_message(lClassName, lFunctionName, "pCode has not a size of 2 : {}"
                                                           .format(pCode))
  if type(pCountryNameFr) is not str: return error_message(lClassName, lFunctionName, "pCountryName is not a str")

  if LocalisationRegion.objects.filter(name=pName).count() != 0:
    return error_message(lClassName, lFunctionName, "Region with Name \"{}\" already exist".format(pName))
  if LocalisationRegion.objects.filter(code=pCode).count() != 0:
    return error_message(lClassName, lFunctionName, "Region with Code \"{}\" already exist".format(pCode))

  lParent = None
  if pCountryNameFr != "":
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

  if lParent is not None:
    lParent.children.add(lRegion)
    lParent.save()

  return lRegion


" --- Creation of a department  --- "
def create_department(pName, pCode, pRegionName):

  lFunctionName = "create_departement"

  if type(pName)          is not str: return error_message(lClassName, lFunctionName, "pName is not a str")
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


" --- Creation of a city  --- "
def create_city(pName, pDepartmentName):

  lFunctionName = "create_city"

  if type(pName)          is not str: return error_message(lClassName, lFunctionName, "pName is not a str")
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

  return lCity


""" --------------------------------------------------------------------------------------------------------------------
------------------------------------------------------------------------------------------------------------------------
Localisation data
------------------------------------------------------------------------------------------------------------------------
-------------------------------------------------------------------------------------------------------------------- """


class NLPurchase(models.Model):
    # 01, 02, 03, etc...
    level         = models.PositiveSmallIntegerField()
    quantity      = models.PositiveSmallIntegerField()

    def __repr__(self):
        return "NLPurchase : {} - {}".format(self.level, self.quantity)


class PaypalPayment(models.Model):
    reference     = models.CharField(max_length=PaypalRefSize)

    def __repr__(self):
        return "PaypalPayment : {}".format(self.reference)


class Payment(models.Model):
    reference     = models.CharField(max_length=20)
    sum           = models.DecimalField(max_digits=7, decimal_places=2)
    datetime      = models.DateTimeField()
    purchase      = models.ForeignKey(NLPurchase, on_delete=models.CASCADE)
    details       = models.TextField()

    UNKNOWN   = 'UN'
    GIFT      = 'GI'
    REFERENCE = 'RE'
    PAYPAL    = 'PP'
    TYPE_PAYMENT = ( (UNKNOWN   , 'null'        ),
                     (GIFT      , 'Gift'        ),
                     (REFERENCE , 'Reference'   ),
                     (PAYPAL    , 'Paypal'      )
                    )
    type          = models.CharField(max_length=2, choices=TYPE_PAYMENT, default=UNKNOWN)
    paypal        = models.ForeignKey(PaypalPayment, null=True, on_delete=models.CASCADE)

    def __repr__(self):
        return "Payment : type={} - reference={} - sum={}".format(self.type, self.reference, self.sum)


""" --------------------------------------------------------------------------------------------------------------------
Payment functions
-------------------------------------------------------------------------------------------------------------------- """


" --- Check Payment --- "
def check_payment(pFunctionName, pReference, pDetails, pDate, pSum, pNLDict, pPaypalRef):

  if type(pReference)    is not str: return error_message(lClassName, pFunctionName, "pUsername is not a str")
  if type(pDetails)      is not str: return error_message(lClassName, pFunctionName, "pDetails is not a datetime")
  if type(pDate)         is not datetime: return error_message(lClassName, pFunctionName, "pDate is not a datetime")
  if type(pSum)          is not int: return error_message(lClassName, pFunctionName, "pSum is not an integer")
  if type(pNLDict)       is not dict: return error_message(lClassName, pFunctionName, "pNLDict is not a dictionnary")
  if type(pPaypalRef)    is not str: return error_message(lClassName, pFunctionName, "pPaypalRef is not a str")

  return True


" --- Add Paypal Payment --- "
def create_paypal_payment(pReference, pDetails, pDate, pSum, pNLDict, pPaypalRef):
    lFunctionName = "create_paypal_payment"

    result = check_payment(lFunctionName, pReference, pDetails, pDate, pSum, pNLDict, pPaypalRef)
    if result is not True:
        return result

    lPaypalPayment = PaypalPayment()
    lPaypalPayment.reference = pPaypalRef
    lPaypalPayment.save()

    lPayment = Payment()
    lPayment.reference = pReference
    lPayment.datetime = pDate
    lPayment.sum = pSum
    lPayment.type = Payment.PAYPAL
    lPayment.details = pDetails

    for nl, quantity in pNLDict.items():
        lNLPurcharse = NLPurchase()
        lNLPurcharse.level = nl
        lNLPurcharse.quantity = quantity
        lNLPurcharse.save()

        lPayment.purchase.add(lNLPurcharse)

    lPayment.save()

    return lPayment


" --- Add Gift Payment --- "
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

  return lPayment


""" --------------------------------------------------------------------------------------------------------------------
------------------------------------------------------------------------------------------------------------------------
Message data
------------------------------------------------------------------------------------------------------------------------
-------------------------------------------------------------------------------------------------------------------- """


class MessageData(models.Model):
    UNKNOWN   = 'UN'
    UNREAD    = 'UR'
    READ      = 'RE'
    STATUS = ( (UNKNOWN   , 'null'   ),
                       (UNREAD    , 'Unread' ),
                       (READ      , 'Read'   ),
                     )

    status        = models.TextField(max_length=2, choices=STATUS, default=UNKNOWN)
    sender        = models.EmailField()
    recipient     = models.EmailField()
    datetime      = models.DateTimeField()
    content       = models.TextField()

    def __repr__(self):
        return "MessageData : sendBy={}, recipient={}, date={}".format(self.sender, self.recipient, self.datetime)


class Message(models.Model):
    subject       = models.CharField(max_length=100)
    messages      = models.ForeignKey(MessageData, on_delete=models.CASCADE)

    def __repr__(self):
        return "Message : {}".format(self.subject)


""" --------------------------------------------------------------------------------------------------------------------
Message functions
-------------------------------------------------------------------------------------------------------------------- """


" --- Verification --- "
def check_message(pFunctionName, pSender, pRecipient, pDatetime, pContent):

  if type(pDatetime)   is not datetime: return error_message(lClassName, pFunctionName, "pDatetime is not a datetime")
  if type(pContent)    is not str:      return error_message(lClassName, pFunctionName, "pContent is not a str")
  try:
    validate_email(pSender)
  except validate_email.ValidationError:
    return error_message(lClassName, pFunctionName, "pSender is not an email ")
  try:
    validate_email(pRecipient)
  except validate_email.ValidationError:
    return error_message(lClassName, pFunctionName, "pRecipient is not an email")

  return True


" --- Creation of a new message --- "
def create_message(pSubject, pSender, pRecipient, pDatetime, pContent):

  lFunctionName = "create_message"

  if type(pSubject)    is not str: return error_message(lClassName, lFunctionName, "pSubject is not a str")
  result = check_message(lFunctionName, pSender, pRecipient, pDatetime, pContent)
  if result is not True:
    return result

  lMessData = MessageData()
  lMessData.status    = MessageData.UNREAD
  lMessData.sender    = pSender
  lMessData.recipient = pRecipient
  lMessData.datetime  = pDatetime
  lMessData.content   = pContent
  lMessData.save()

  lMessage = Message()
  lMessage.subject = pSubject
  lMessage.messages.add(lMessData)
  lMessage.save()

  return lMessage


" --- Add new message --- "
def add_message(pMessage, pSender, pRecipient, pDatetime, pContent):

  lFunctionName = "add_message"
  result = check_message(lFunctionName, pSender, pRecipient, pDatetime, pContent)
  if result is not True:
    return result

  lMessData = MessageData()
  lMessData.status    = MessageData.UNREAD
  lMessData.sender    = pSender
  lMessData.recipient = pRecipient
  lMessData.datetime  = pDatetime
  lMessData.content   = pContent
  lMessData.save()

  pMessage.message.add(lMessData)
  pMessage.save()

  return pMessage


" --- Change status message to read --- "
def move_to_read(pMessage):

  lFunctionName = "move_to_read"
  if type(pMessage) is not MessageData: return error_message(lClassName, lFunctionName, "pMessage is not a MessageData")

  pMessage.status   = MessageData.READ
  pMessage.save()

  return pMessage


""" --------------------------------------------------------------------------------------------------------------------
------------------------------------------------------------------------------------------------------------------------
Notification data
------------------------------------------------------------------------------------------------------------------------
-------------------------------------------------------------------------------------------------------------------- """


class NotificationCustomer(models.Model):
    UNKNOWN     = 'UN'
    MESSAGE     = 'NM'
    REPORT      = 'NR'
    OPINION     = 'NO'
    TITLE_POSSIBILITY = ( (UNKNOWN    , 'null'     ),
                          (MESSAGE    , 'New Message' ),
                          (REPORT     , 'New Report'  ),
                          (OPINION    , 'New Opinion' )
                        )

    title         = models.CharField(max_length=2, choices=TITLE_POSSIBILITY, default=UNKNOWN)
    content       = models.TextField(max_length=50, default="")

    def __repr__(self):
        return "NotificationCustomer : {} - {}".format(self.title, self.content)


class NotificationAdmin(models.Model):
    UNKNOWN     = 'UN'
    MESSAGE     = 'NM'
    REPORT      = 'NR'
    VALIDATION  = 'NV'
    ERROR       = 'ER'
    TITLE_POSSIBILITY = ( (UNKNOWN    , 'null'            ),
                          (MESSAGE    , 'New Message'     ),
                          (REPORT     , 'New Report'      ),
                          (VALIDATION , 'New Validation'  ),
                          (ERROR      , 'New Error'       )
                        )

    title         = models.CharField(max_length=2, choices=TITLE_POSSIBILITY, default=UNKNOWN)
    content       = models.TextField(max_length=50, default="")

    def __repr__(self):
        return "NotificationAdmin : {} - {}".format(self.title, self.content)


""" --------------------------------------------------------------------------------------------------------------------
------------------------------------------------------------------------------------------------------------------------
Site data
------------------------------------------------------------------------------------------------------------------------
-------------------------------------------------------------------------------------------------------------------- """


class SiteStat(models.Model):
    creationDate  = models.DateTimeField(default=datetime.now())
    creationUser  = models.CharField(max_length=UserMaxSize, default="creation")
    lastModDate   = models.DateTimeField(default=datetime.now())
    lastModUser   = models.CharField(max_length=UserMaxSize, default="null")
    last1yConnect = models.IntegerField(default=0)
    last1mConnect = models.IntegerField(default=0)
    last1wConnect = models.IntegerField(default=0)
    last1dConnect = models.IntegerField(default=0)


class Opinion(models.Model):
    sender        = models.CharField(max_length=UserMaxSize, default="null")
    rate          = models.DecimalField(max_digits=3, decimal_places=2)
    content       = models.TextField(default="")

    def __repr__(self):
        return "Opinion : sendBy={}, rate={}, text={}".format(self.sender, self.rate, self.content)


class Report(models.Model):
    # TODO: A compléter selon ce qu'il est possible de reporter
    UNKNOWN     = 'UN'
    COPYRIGHT   = 'CO'
    TITLE_POSSIBILITY = ( (UNKNOWN      , 'null'        ),
                          (COPYRIGHT    , 'Copyright'   )
                        )
    sender        = models.CharField(max_length=UserMaxSize, default="null")
    title         = models.CharField(max_length=2, choices=TITLE_POSSIBILITY, default=UNKNOWN)
    content       = models.TextField(max_length=50)
    date          = models.DateTimeField(default=datetime.now())

    def __repr__(self):
        return "Report : sendBy={}, date={}, title={}, content={}".format(self.sender, self.date, self.title,
                                                                          self.content)


class Site(models.Model):
    title         = models.TextField(max_length=50)
    content       = models.TextField()
    link          = models.SlugField()
    nllevel       = models.PositiveSmallIntegerField(default=0)
    # pictures      = models.ForeignKey(models.ImageField(upload_to='site_pictures',
    #                                                         default='site_pictures/default/no_image.png'))
    category      = models.ForeignKey(Category, null=True, on_delete=models.SET_NULL)
    opinions      = models.ForeignKey(Opinion,  null=True, on_delete=models.CASCADE)
    report        = models.ForeignKey(Report,   null=True, on_delete=models.CASCADE)
    stat          = models.OneToOneField(SiteStat, on_delete=models.CASCADE, primary_key=True)
    
    def __repr__(self):
        return "Site : "


""" --------------------------------------------------------------------------------------------------------------------
------------------------------------------------------------------------------------------------------------------------
Account data
------------------------------------------------------------------------------------------------------------------------
-------------------------------------------------------------------------------------------------------------------- """


class AccountActivation(models.Model):
    link          = models.SlugField(default=uuid4(), max_length=20, unique=True)
    expiration    = models.DateTimeField(default=datetime.now()+timedelta(days=7))


class Account(models.Model):
    # TODO: Voir pour les permissions
    """ link OneToOne to the User model (username, first_name, last_name, email, password, is_staff, is_active,
    is_superuser, last_login, date_joined, user_permissions, groups """
    user          = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

    company       = models.CharField(max_length=50)
    activation    = models.ForeignKey(AccountActivation     , null=True, on_delete=models.CASCADE)
    sites         = models.ForeignKey(Site                  , null=True, on_delete=models.CASCADE)
    messages      = models.ManyToManyField(Message)
    notification  = models.ForeignKey(NotificationCustomer  , null=True, on_delete=models.CASCADE)
    payment       = models.ForeignKey(Payment               , null=True, on_delete=models.CASCADE)


""" --------------------------------------------------------------------------------------------------------------------
Account functions
-------------------------------------------------------------------------------------------------------------------- """


" --- Validation of user data --- "
def check_user_data(pFunctionName, pUsername, pEmail, pPassword, pFirstName, pLastName, pCompany):

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


" --- Creation of a user account --- "
def create_user_account(pUsername, pEmail, pPassword, pFirstName, pLastName, pCompany):

  lFunctionName = "create_user_account"

  result = check_user_data(lFunctionName, pUsername, pEmail, pPassword, pFirstName, pLastName, pCompany)
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


" --- Creation of a validator account --- "
def create_valid_account(pUsername, pEmail, pPassword, pFirstName, pLastName):

  lFunctionName = "create_valid_account"

  result = check_user_data(lFunctionName, pUsername, pEmail, pPassword, pFirstName, pLastName, "")
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


" --- Creation of an admin account --- "
def create_admin_account(pUsername, pEmail, pPassword, pFirstName, pLastName):

  lFunctionName = "create_valid_account"

  result = check_user_data(lFunctionName, pUsername, pEmail, pPassword, pFirstName, pLastName, "")
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
