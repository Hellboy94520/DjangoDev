from django.db import models
from datetime import datetime
from enum import Enum
from .account import AccountAdmin
from .communs import Log, Stat, CreationText, ModificationText


""" --------------------------------------------------------------------------------------------------------------------
------------------------------------------------------------------------------------------------------------------------
Data
------------------------------------------------------------------------------------------------------------------------
-------------------------------------------------------------------------------------------------------------------- """
lNameSize = 50


""" ---------------------------------------------------------------------------------------------------------------- """
class Type(Enum):
  UN = "Unknown"
  CO = "Continent"
  CU = "Country"
  RE = "Region"
  DE = "Department"
  CI = "City"


class Status(Enum):
  UN = "Unknown"
  AC = "Active"
  UA = "Unactive"


""" ---------------------------------------------------------------------------------------------------------------- """
class Localisation(models.Model):
  nameFr        = models.CharField(max_length=lNameSize)
  nameEn        = models.CharField(max_length=lNameSize)
  code          = models.CharField(max_length=5)
  type          = models.CharField(max_length=2,
                                   choices=[(tag, tag.value) for tag in Type],
                                   default=Type.UN)
  status        = models.CharField(max_length=2,
                                   choices=[(tag, tag.value) for tag in Status],
                                   default=Status.UN)
  children      = models.ManyToManyField('self', related_name="childrenLocalisation")

  def __repr__(self):
    return "Localisation: nameFr={}, nameEn={}, code={}, type={}, status={}"\
      .format(self.nameFr, self.nameEn, self.code, self.type.value, self.status.value)


class LocalisationStat(Stat):
  localisation  = models.OneToOneField(Localisation, on_delete=models.CASCADE, primary_key=True)


class LocalisationLog(Log):
  localisation  = models.ForeignKey(Localisation, on_delete=models.CASCADE)


""" --------------------------------------------------------------------------------------------------------------------
------------------------------------------------------------------------------------------------------------------------
Functions
------------------------------------------------------------------------------------------------------------------------
-------------------------------------------------------------------------------------------------------------------- """
" --- Creation of stat  --- "
def create_stat(pLocalisation: Localisation):
  lStat = LocalisationStat()
  lStat.localisation = pLocalisation
  lStat.save()
  return lStat


" --- Creation of a log  --- "
def create_log(pUser: AccountAdmin, pModification: str, pLocalisation: Localisation):
  lLog = LocalisationLog()
  lLog.date         = datetime.now()
  lLog.modif        = pModification
  lLog.user         = pUser
  lLog.localisation = pLocalisation
  lLog.save()
  return lLog


" --- Creation of a localisation  --- "
def create(pNameFr: str, pNameEn: str, pCode: str, pType: Type, pStatus: Status,
           pUser: AccountAdmin):

  if Localisation.objects.filter(nameFr=pNameFr, type=pType, status=pStatus).count() != 0:
    return "nameFr: Already exist"
  if Localisation.objects.filter(nameEn=pNameEn, type=pType, status=pStatus).count() != 0:
    return "nameEn: Already exist"
  if Localisation.objects.filter(code=pCode    , type=pType, status=pStatus).count() != 0:
    return "code: Already exist"

  lLoc = Localisation()
  lLoc.nameFr = pNameFr
  lLoc.nameEn = pNameEn
  lLoc.code   = pCode
  lLoc.type   = pType
  lLoc.status = pStatus
  lLoc.save()

  create_stat(lLoc)
  create_log(pUser, "{} {}".format(CreationText, repr(lLoc)), lLoc)

  return lLoc


" --- Modification of a localisation  --- "
def modif(pLocalisation: Localisation, pNameFr: str, pNameEn: str, pCode: str, pType: Type,
          pStatus: Status, pUser: AccountAdmin):

  lLog = ModificationText
  lModif = False

  if pNameFr and pNameFr != pLocalisation.nameFr:
    lLog += " nameFr: {}".format(pNameFr)
    pLocalisation.nameFr = pNameFr
    lModif = True

  if pNameEn and pNameEn != pLocalisation.nameEn:
    lLog += " nameEn: {}".format(pNameEn)
    pLocalisation.nameEn = pNameEn
    lModif = True

  if pCode and pCode != pLocalisation.code:
    lLog += " code: {}".format(pCode)
    pLocalisation.code = pCode
    lModif = True

  if pType != Type.UN and pType != pLocalisation.type:
    lLog += " type: {}".format(pType)
    pLocalisation.type = pType
    lModif = True

  if pStatus != Status.UN and pStatus != pLocalisation.status:
    lLog += " status: {}".format(pStatus)
    pLocalisation.status = pStatus
    lModif = True

  # If any modification has been done
  if not lModif: return False
  # Else
  pLocalisation.save()
  create_log(pUser, lLog, pLocalisation)
  return True


" --- Add Children localisation to Parent localisation --- "
def add_children(pParent: Localisation, pChildren: Localisation, pUser: AccountAdmin):
  pParent.children.add(pChildren)
  pParent.save()
  create_log(pUser, "Add Children {}".format(repr(pChildren)))
  return True


" --- Get logs associate to Localisation --- "
def get_logs(pLocalisation: Localisation):
  return LocalisationLog.objects.filter(localisation=pLocalisation)


" --- Get stat associate to Localisation --- "
def get_stat(pLocalisation: Localisation):
  lResult = LocalisationStat.objects.filter(localisation=pLocalisation)
  if lResult.count() != 1:
    return "Error : Any or too many results !"
  return lResult[0]


" --- Add One Consultation --- "
def add_oneconsult(pLocalisation: Localisation):
  # Search stat associate to Localisation
  lStat = get_stat(pLocalisation)
  if len(lStat) != 1: return "Error: Stat not found"

  # If Available
  lStat = lStat[0]
  lStat.last1yConsu += 1
  lStat.last1mConsu += 1
  lStat.last1wConsu += 1
  lStat.last1dConsu += 1
  lStat.save()

  return True


