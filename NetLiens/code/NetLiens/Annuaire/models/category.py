from django.db import models
from datetime import datetime, timedelta
from .account import AccountAdmin
from .communs import Status, LogAdmin, Stat, CreationText, ModificationText, DeletionText

""" --------------------------------------------------------------------------------------------------------------------
------------------------------------------------------------------------------------------------------------------------
Data
------------------------------------------------------------------------------------------------------------------------
-------------------------------------------------------------------------------------------------------------------- """
CategoryTitleSize    = 100


""" --------------------------------------------------------------------------------------------------------------------
------------------------------------------------------------------------------------------------------------------------
Class
------------------------------------------------------------------------------------------------------------------------
-------------------------------------------------------------------------------------------------------------------- """
class Category(models.Model):
  nameFr    = models.CharField(max_length=CategoryTitleSize, default="")
  nameEn    = models.CharField(max_length=CategoryTitleSize, default="")
  resumeFr  = models.TextField(max_length=50, default="")
  resumeEn  = models.TextField(max_length=50, default="")
  status    = models.CharField(max_length=2,
                               choices=[(tag, tag.value) for tag in Status],
                               default=Status.UN)
  children  = models.ManyToManyField('self', related_name='childrenCategory')
  date      = models.DateField(default=datetime.now())    # Creation Date

  " --- Constructor --- "
  def __init__(self, pNameFr: str, pNameEn: str, pResumeFr: str, pResumeEn: str, pStatus: Status, pAdmin: AccountAdmin):
    models.Model.__init__(self)
    # Avoid to call deactivated __setattr__
    object.__setattr__(self, 'nameFr'   , pNameFr   )
    object.__setattr__(self, 'nameEn'   , pNameEn   )
    object.__setattr__(self, 'resumeFr' , pResumeFr )
    object.__setattr__(self, 'resumeEn' , pResumeEn )
    object.__setattr__(self, 'status'   , pStatus   )
    self.save()
    # Creation CategoryStat and CategoryLog associate
    CategoryStat(self)
    CategoryLog("{} {}".format(CreationText, repr(self)), self, pAdmin)

  def modif(self, pNameFr: str, pNameEn: str, pResumeFr: str, pResumeEn: str, pStatus: Status, pAdmin: AccountAdmin):
    lLog = ModificationText
    # Modification only if it is
    if pNameFr and pNameFr != self.nameFr:
      lLog += " nameFr: {},".format(pNameFr)
      self.nameFr = pNameFr
    if pNameEn and pNameEn != self.nameEn:
      lLog += " nameEn: {},".format(pNameEn)
      self.nameEn = pNameEn
    if pResumeFr and pResumeFr != self.resumeFr:
      lLog += " resumeFr: {},".format(pResumeFr)
      self.resumeFr = pResumeFr
    if pResumeEn and pResumeEn != self.resumeEn:
      lLog += " resumeEn: {},".format(pResumeEn)
      self.resumeEn = pResumeEn
    if pStatus != Status.UN and pStatus != self.status:
      lLog += " status : {},".format(pStatus)
      self.status = pStatus
    # Save the data
    if lLog == ModificationText: return False   # If any modification has been done
    self.save()
    CategoryLog(lLog, self, pAdmin)

  def to_trash(self, pAdmin: AccountAdmin):
    # TODO: Faire le système qui va vérifier s'il faut supprimer un objet ou non dans la poubelle
    self.status = Status.TR
    self.date   = datetime.now()+timedelta(days=7)        # Date of deletion
    CategoryLog("{} {}".format(DeletionText, repr(self)), self, pAdmin)
    # TODO: Faire le système qui va déplacer les sites qui avait cette catégory par celle parent

  def get_logs(self):
    return CategoryLog.objects.filter(category=self)

  def get_stat(self):
    return CategoryStat.objects.get(category=self)

  def __repr__(self):
    return "Category : nameFr={}, nameEn={}, resumeFr={}, resumeEn={}, status={}, date={}"\
      .format(self.nameFr, self.nameEn, self.resumeFr, self.resumeEn, self.status.value, self.date)

  # Deactivate the modification by this way to be sure to have a log
  def __setattr__(self, key, value):
    pass

  # Deactivate the deletion to have personnal system
  def __del__(self):
    pass


""" ---------------------------------------------------------------------------------------------------------------- """
class CategoryStat(Stat):
  category    = models.OneToOneField(Category, on_delete=models.CASCADE, primary_key=True)

  def __init__(self, pCategory: Category):
    Stat.__init__(self)
    self.category = pCategory
    self.save()


""" ---------------------------------------------------------------------------------------------------------------- """
class CategoryLog(LogAdmin):
  category     = models.ForeignKey(Category  , on_delete=models.CASCADE)

  def __init__(self, pModif: str, pCategory: Category, pAdmin: AccountAdmin):
    LogAdmin.__init__(self)
    self.user     = pAdmin
    self.modif    = pModif
    self.category = pCategory
    self.save()


""" --------------------------------------------------------------------------------------------------------------------
------------------------------------------------------------------------------------------------------------------------
Functions
------------------------------------------------------------------------------------------------------------------------
-------------------------------------------------------------------------------------------------------------------- """
# TODO: Me renseigner sur le fait de voir si c'est possible de mettre cette fonction dans le classe sachant que je peux pas avoir l'enfant en Category
" --- Add Children category to Parent category --- "
def add_children(pParent: Category, pChildren: Category, pUser: AccountAdmin):
  pParent.children.add(pChildren)
  pParent.save()
  CategoryLog("Add Children {}".format(repr(pChildren)), pParent, pUser)
  return True


" --- Get the much see category --- "
def get_much_see(pTimePeriod: str, pQuantity: int, pReverse: bool):

  if pReverse is True: lParam = "-" + pTimePeriod
  else:                lParam = pTimePeriod

  try:
    categoryStatList = CategoryStat.objects.order_by(lParam)[0:pQuantity]
  except IOError as e:
    return "error: {}".format(e)

  categoryList = []

  for categoryStat in categoryStatList:
    categoryList.append(Category.objects.get(stat_id=categoryStat.id))

  return categoryList
