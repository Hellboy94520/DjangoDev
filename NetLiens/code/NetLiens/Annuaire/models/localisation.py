from django.db import models
from datetime import datetime, timedelta
from enum import Enum
from .account import AccountAdmin
from .communs import Status, LogAdmin, Stat, CreationText, ModificationText, DeletionText


""" --------------------------------------------------------------------------------------------------------------------
------------------------------------------------------------------------------------------------------------------------
Data
------------------------------------------------------------------------------------------------------------------------
-------------------------------------------------------------------------------------------------------------------- """
NameSize = 50


""" --------------------------------------------------------------------------------------------------------------------
------------------------------------------------------------------------------------------------------------------------
Enum
------------------------------------------------------------------------------------------------------------------------
-------------------------------------------------------------------------------------------------------------------- """
class Type(Enum):
  UN = "Unknown"
  CO = "Continent"
  CU = "Country"
  RE = "Region"
  DE = "Department"
  CI = "City"


""" --------------------------------------------------------------------------------------------------------------------
------------------------------------------------------------------------------------------------------------------------
Class
------------------------------------------------------------------------------------------------------------------------
-------------------------------------------------------------------------------------------------------------------- """
class Localisation(models.Model):
  nameFr        = models.CharField(max_length=NameSize)
  nameEn        = models.CharField(max_length=NameSize)
  code          = models.CharField(max_length=5)
  type          = models.CharField(max_length=2,
                                   choices=[(tag, tag.value) for tag in Type],
                                   default=Type.UN)
  status        = models.CharField(max_length=2,
                                   choices=[(tag, tag.value) for tag in Status],
                                   default=Status.UN)
  children      = models.ManyToManyField('self', related_name="childrenLocalisation")

  def modif(self, pNameFr: str, pNameEn: str, pCode: str, pType: Type, pStatus: Status, pAdmin: AccountAdmin):
    # Search if the localisation does not already exist
    lResult = verification(pNameFr, pNameEn, pCode, pType, pStatus)
    if lResult is not True:
      return lResult
    # Prepare the log
    lLog   = ModificationText
    # Modification only if it is
    if pNameFr and pNameFr != self.nameFr:
      lLog += " nameFr: {},".format(pNameFr)
      object.__setattr__(self, 'nameFr', pNameFr)
    if pNameEn and pNameEn != self.nameEn:
      lLog += " nameEn: {},".format(pNameEn)
      object.__setattr__(self, 'nameEn', pNameEn)
    if pCode and pCode!= self.code:
      lLog += " code: {},".format(pCode)
      object.__setattr__(self, 'code', pCode)
    if pType and pType != self.type:
      lLog += " type: {},".format(str(pType))
      object.__setattr__(self, 'type', pType)
    if pStatus and pStatus != self.pStatus:
      lLog += " status: {},".format(str(pStatus))
      object.__setattr__(self, 'status', pStatus)
    # Save the data
    if lLog == ModificationText: return False   # If any modification has been done
    self.save()
    LocalisationLog(lLog, self, pAdmin)


  def get_logs(self):
    return LocalisationLog.objects.filter(localisation=self)

  def get_stat(self):
    return LocalisationStat.objects.get(localisation=self)

  def __repr__(self):
    return "Localisation: nameFr={}, nameEn={}, code={}, type={}, status={}"\
      .format(self.nameFr, self.nameEn, self.code, self.type.value, self.status.value)


""" ---------------------------------------------------------------------------------------------------------------- """
class LocalisationStat(Stat):
  localisation  = models.OneToOneField(Localisation, on_delete=models.CASCADE, primary_key=True)


""" ---------------------------------------------------------------------------------------------------------------- """
class LocalisationLog(LogAdmin):
  localisation  = models.ForeignKey(Localisation, on_delete=models.CASCADE)


""" --------------------------------------------------------------------------------------------------------------------
------------------------------------------------------------------------------------------------------------------------
Functions
------------------------------------------------------------------------------------------------------------------------
-------------------------------------------------------------------------------------------------------------------- """
def verification(pNameFr: str, pNameEn: str, pCode: str, pType: Type, pStatus: Status, pUser: AccountAdmin):
  if Localisation.objects.filter(nameFr=pNameFr, type=pType, status=pStatus).count() != 0:
    return "nameFr: Already exist"
  if Localisation.objects.filter(nameEn=pNameEn, type=pType, status=pStatus).count() != 0:
    return "nameEn: Already exist"
  if Localisation.objects.filter(code=pCode, type=pType, status=pStatus).count() != 0:
    return "code: Already exist"

  return True

def create_localisation_stat(pLocalisation: Localisation):
  lStat = LocalisationStat()
  lStat.localisation = pLocalisation
  lStat.save()

def create_localisation_log(pModif: str, pLoc: Localisation, pAdmin: AccountAdmin):
  lLog = LocalisationLog()
  lLog.user         = pAdmin
  lLog.localisation = pLoc
  lLog.modif        = pModif
  lLog.save()

def create_localisation(pNameFr: str, pNameEn: str, pCode: str, pType: Type, pStatus: Status, pAdmin: AccountAdmin):
  lLoc = Localisation()
  lLoc.nameFr = pNameFr
  lLoc.nameEn = pNameEn
  lLoc.code   = pCode
  lLoc.type   = pType
  lLoc.status = pStatus
  lLoc.save()

  # Creation of CategoryStat link to Category
  create_localisation_stat(lLoc)

  # Creation of CategoryLog link to Category
  create_localisation_log("{}{}".format(CreationText, repr(lLoc)), lLoc, pAdmin)

  return lLoc


" -------------------------------------------------------------------------------------------------------------------- "
def modif_localisation(pLocalisation: Localisation, pNameFr: str, pNameEn: str, pCode: str, pType: Type,
                       pStatus: Status, pAdmin: AccountAdmin):
  # Modification of the data
  pLocalisation.nameFr  = pNameFr
  pLocalisation.nameEn  = pNameEn
  pLocalisation.code    = pCode
  pLocalisation.type    = pType
  pLocalisation.status  = pStatus

  # Save the data
  pLocalisation.save()

  # Creation of the modification log
  create_localisation_log("{}{}".format(ModificationText, repr(pLocalisation)), pLocalisation, pAdmin)

  return True


" -------------------------------------------------------------------------------------------------------------------- "
def add_children(pParent: Localisation, pChildren: Localisation, pAdmin: AccountAdmin):
  pParent.children.add(pChildren)
  pParent.save()
  LocalisationLog("Add Children {}".format(repr(pChildren)), pParent, pAdmin)
  return True




