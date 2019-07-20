from django.db import models
from datetime import datetime
from .account import User, AccountAdmin
from .stat import Stat
from enum import Enum

""" --------------------------------------------------------------------------------------------------------------------
------------------------------------------------------------------------------------------------------------------------
HOW TO USE

- Localisation creation from an Administrator: 
        lLocalisation = Localisation(nameFr="toto", [...])
        lLocalisation.create(lAdminAccount)

- Localisation request creation from a user: 
        lLocalisation = Localisation(nameFr="toto", [...])
        lLocalisation.request_creation(lUser)

- Category change display status from an Administrator:
        lLocalisation.show(bool, lAccount)

- Localisation modification from an Administrator only:
        lLocalisation.nameFr = "toto"
        lLocalisation.modification(lAdminAccount)

- Accept the request creation of a new category from an Administrator only:
        lLocalisationEventCreationRequest.accept(lAdminAccount)

- Refuse the request creation of a new category from an Administrator only:
        lLocalisationEventCreationRequest.accept(lAdminAccount)

------------------------------------------------------------------------------------------------------------------------
-------------------------------------------------------------------------------------------------------------------- """


""" --------------------------------------------------------------------------------------------------------------------
------------------------------------------------------------------------------------------------------------------------
Data
------------------------------------------------------------------------------------------------------------------------
-------------------------------------------------------------------------------------------------------------------- """
NameSize = 50


""" --------------------------------------------------------------------------------------------------------------------
------------------------------------------------------------------------------------------------------------------------
Class Data
------------------------------------------------------------------------------------------------------------------------
-------------------------------------------------------------------------------------------------------------------- """
class LocalisationType(Enum):
  UN = "Unknown"
  CO = "Continent"
  CU = "Country"
  TE = "Territory"
  RE = "Region"
  DE = "Department"
  CI = "City"

def typeToValue(pString):
  if type(pString) is LocalisationType:
    return pString.value

  if type(pString) is str:
    if   pString == "Type.UN":
      return LocalisationType.UN.value
    elif pString == "Type.CO":
      return LocalisationType.CO.value
    elif pString == "Type.CU":
      return LocalisationType.CU.value
    elif pString == "Type.TE":
      return LocalisationType.TE.value
    elif pString == "Type.RE":
      return LocalisationType.RE.value
    elif pString == "Type.DE":
      return LocalisationType.DE.value
    elif pString == "Type.CI":
      return LocalisationType.CI.value

  return None


""" ---------------------------------------------------------------------------------------------------------------- """
class Localisation(models.Model):
  objects = None
  nameFr        = models.CharField(max_length=NameSize, default="")
  nameEn        = models.CharField(max_length=NameSize, default="")
  code          = models.CharField(max_length=5)
  type          = models.CharField(max_length=2,
                                   choices=[(tag, tag.value) for tag in LocalisationType],
                                   default=LocalisationType.UN)
  display       = models.BooleanField(default=False)
  parent        = models.ForeignKey('self', default=None, null=True, on_delete=models.SET_NULL)

  """ ---------------------------------------------------- """
  def create(self, admin: AccountAdmin):
    # Creation in database
    self.save()
    # Creation of the log
    lDetails = "Creation of " + str(self)
    lLocalisationLog = LocalisationLog(user     = admin.user,
                                       localisation = self  ,
                                       type     = LogType.CR,
                                       details  = lDetails)
    lLocalisationLog.save()
    # Creation of the stat
    lLocalisationStat = LocalisationStat(localisation=self             ,
                                         creation_user=admin.user      ,
                                         validation_date=datetime.now(),
                                         validation_user=admin.user)
    lLocalisationStat.create()

  """ ---------------------------------------------------- """
  def modification(self, admin: AccountAdmin, details=""):
    # Save the modification in database
    self.save()
    # Creation of the log
    lDetails = "Modification of '" + str(self) + "'. " + details
    lLocalisationLog = LocalisationLog(user     = admin.user,
                                       localisation = self  ,
                                       type     = LogType.MO,
                                       details  = lDetails)
    lLocalisationLog.save()

  """ ---------------------------------------------------- """
  def show(self, display: bool, admin: AccountAdmin, details=""):
    # TODO: Check before if a parent exist and site associated exist
    self.display = display
    self.save()
    # Creation of the log
    lDetails = "Change display to " + str(self.display) + ". " + details
    lLocalisationLog = LocalisationLog(user     = admin.user,
                                       category = self      ,
                                       type     = LogType.MO,
                                       details  = lDetails)
    lLocalisationLog.save()

  """ ---------------------------------------------------- """
  # TODO: When Site will be create add site in parameter
  # def request_creation(self, user: User, pSite: Site, details=""):
  def request_creation(self, user: User, details=""):
    # Undisplay the Localisation
    self.display = False
    self.save()
    # Creation of the log
    lDetails = "Request Creation for reason '" + details + "'"
    lLocalisationLog = LocalisationLog(user         = user      ,
                                       localisation = self      ,
                                       type         = LogType.RC,
                                       details      = lDetails)
    lLocalisationLog.save()
    # Creation of the stat
    lLocalisationStat = LocalisationStat(localisation=self, creation_user=user)
    lLocalisationStat.create()
    # Creation of the event
    lLocalisationEvent = LocalisationEventCreationRequest(user 		      = user,
                                                          # TODO: site 		 = site,
                                                          site          = None,
                                                          localisation  = self)
    lLocalisationEvent.save()

  """ ---------------------------------------------------- """
  def set_parent(self, parent, admin: AccountAdmin):
    # Add Children
    self.parent = parent
    self.save()
    # Creation of the log
    lDetails = "Set Parent " + str(parent)
    lLocalisationLog = LocalisationLog(user     = admin.user,
                                       localisation = self  ,
                                       type     = LogType.MO,
                                       details  = lDetails)
    lLocalisationLog.save()

  """ ---------------------------------------------------- """
  def erase(self, admin: AccountAdmin):
    # Move Children Localisation to Parent of this Localisation
    for lChildren in Localisation.objects.filter(parent=self):
      lChildren.set_parent(self.parent, admin)
    # And delete the category
    self.delete()

  """ ---------------------------------------------------- """
  def get_logs(self):
    return LocalisationLog.objects.filter(localisation=self)

  """ ---------------------------------------------------- """
  def get_stat(self):
    return LocalisationStat.objects.get(localisation=self)

  """ ---------------------------------------------------- """
  def __str__(self):
    return "Localisation: nameFr={}, nameEn={}, code={}, type={}, display={}"\
      .format(self.nameFr, self.nameEn, self.code, typeToValue(self.type), self.display)


""" --------------------------------------------------------------------------------------------------------------------
------------------------------------------------------------------------------------------------------------------------
Class Event
------------------------------------------------------------------------------------------------------------------------
-------------------------------------------------------------------------------------------------------------------- """
class LocalisationEventCreationRequest(models.Model):
  objects = None
  date          = models.DateTimeField(default=datetime.now())
  saw           = models.BooleanField(default=False)
  user          = models.ForeignKey(User, on_delete=models.CASCADE)
  localisation  = models.ForeignKey(Localisation, on_delete=models.CASCADE)

  """ ---------------------------------------------------- """
  def accept(self, admin: AccountAdmin):
    # Creation of the log
    lDetail = "Request Accept from '" + admin.user.username + "'"
    lLocalisationLog = LocalisationLog(user         = admin.user   ,
                                       localisation = self.localisation,
                                       type         = LogType.CR   ,
                                       details      = lDetail)
    lLocalisationLog.save()
    # Complete the Stat object
    lLocalisationStat = self.localisation.get_stat()
    lLocalisationStat.validation_date = datetime.now()
    lLocalisationStat.validation_user = admin.user
    lLocalisationStat.save()
    # Display the localisation on website
    self.localisation.display = True
    self.localisation.save()
    # Delete the event
    self.delete()

  """ ---------------------------------------------------- """
  def refuse(self, admin: AccountAdmin):
    # Delete the localisation and the event (by cascade)
    self.localisation.delete()

  """ ---------------------------------------------------- """
  def __str__(self):
    return "date={}, user_email={}, site_name={}, saw={}"\
      .format(self.date, self.user.email, self.site.nameFr, self.saw)


""" --------------------------------------------------------------------------------------------------------------------
------------------------------------------------------------------------------------------------------------------------
Class Log
------------------------------------------------------------------------------------------------------------------------
-------------------------------------------------------------------------------------------------------------------- """
class LogType(Enum):
  UN = "unknown"
  RC = "creation_request"
  RM = "modification_request"
  CR = "creation"
  MO = "modification"


""" ---------------------------------------------------------------------------------------------------------------- """
class LocalisationLog(models.Model):
  objects = None
  date          = models.DateTimeField(default=datetime.now())
  user          = models.ForeignKey(User, default=None, null=True, on_delete=models.SET_NULL)
  localisation  = models.ForeignKey(Localisation, on_delete=models.CASCADE)
  type          = models.CharField(max_length=2,
                                   choices=[(tag, tag.value) for tag in LogType],
                                   default=LogType.UN)
  details       = models.TextField(default="")


""" --------------------------------------------------------------------------------------------------------------------
------------------------------------------------------------------------------------------------------------------------
Class Stat
------------------------------------------------------------------------------------------------------------------------
-------------------------------------------------------------------------------------------------------------------- """
class LocalisationStat(Stat):
  localisation = models.OneToOneField(Localisation, on_delete=models.CASCADE, primary_key=True)
