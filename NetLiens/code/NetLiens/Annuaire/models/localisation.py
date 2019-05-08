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

  def create(self, pNameFr: str, pNameEn: str, pCode: str, pType: Type, pStatus: Status, pAdmin: AccountAdmin):
    # Search if the localisation does not already exist
    lResult = verification(pNameFr, pNameEn, pCode, pType, pStatus)
    if lResult is not True:
      return lResult
    # Creation
    models.Model.__init__(self)
    # Avoid to call deactivated __setattr__
    object.__setattr__(self, 'nameFr'   , pNameFr )
    object.__setattr__(self, 'nameEn'   , pNameEn )
    object.__setattr__(self, 'code'     , pCode   )
    object.__setattr__(self, 'type'     , pType   )
    object.__setattr__(self, 'status'   , pStatus )
    self.save()

    # Creation LocalisationStat andLocalisationLog associate
    LocalisationStat(self)
    LocalisationLog("{} {}".format(CreationText, repr(self)),
                    self,
                    pAdmin)
    return True

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

  def to_trash(self, pAdmin: AccountAdmin):
    # TODO: Faire le système qui va vérifier s'il faut supprimer un objet ou non dans la poubelle
    self.status = Status.TR
    self.date   = datetime.now()+timedelta(days=7)        # Date of deletion
    LocalisationLog("{} {}".format(DeletionText, repr(self)))
    # TODO: Faire le système qui va demander ou ranger les enfants

  def get_logs(self):
    return LocalisationLog.objects.filter(localisation=self)

  def get_stat(self):
    return LocalisationStat.objects.get(localisation=self)

  def __repr__(self):
    return "Localisation: nameFr={}, nameEn={}, code={}, type={}, status={}"\
      .format(self.nameFr, self.nameEn, self.code, self.type.value, self.status.value)

  # Deactivate the constructor to have the verification and the log
  def __init__(self):
    pass

  # Deactivate the modification by this way to be sure to have a log
  def __setattr__(self, key, value):
    pass

  # Deactivate the deletion by this way to avoid error
  def __del__(self):
    pass


""" ---------------------------------------------------------------------------------------------------------------- """
class LocalisationStat(Stat):
  localisation  = models.OneToOneField(Localisation, on_delete=models.CASCADE, primary_key=True)

  def __init__(self, pLoc: Localisation):
    Stat.__init__(self)
    self.localisation = pLoc
    self.save()


""" ---------------------------------------------------------------------------------------------------------------- """
class LocalisationLog(LogAdmin):
  localisation  = models.ForeignKey(Localisation, on_delete=models.CASCADE)

  def __init__(self, pModif, pLoc: Localisation, pAdmin: AccountAdmin):
    LogAdmin.__init__(self)
    self.user     = pAdmin
    self.modif    = pModif
    self.category = pLoc
    self.save()


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


# TODO: Me renseigner sur le fait de voir si c'est possible de mettre cette fonction dans le classe sachant que je peux pas avoir l'enfant en Category
" --- Add Children localisation to Parent localisation --- "
def add_children(pParent: Localisation, pChildren: Localisation, pAdmin: AccountAdmin):
  pParent.children.add(pChildren)
  pParent.save()
  LocalisationLog("Add Children {}".format(repr(pChildren)), pParent, pAdmin)
  return True



