from django.db import models
from datetime import datetime
from .account import AccountAdmin
from .communs import Log, Stat, CreationText, ModificationText
from enum import Enum

from django.dispatch import receiver

""" --------------------------------------------------------------------------------------------------------------------
------------------------------------------------------------------------------------------------------------------------
Data
------------------------------------------------------------------------------------------------------------------------
-------------------------------------------------------------------------------------------------------------------- """
CategoryTitleSize    = 100


""" ---------------------------------------------------------------------------------------------------------------- """
class Status(Enum):
  UN = "Unknown"
  AC = "Active"    # Show on the website
  UA = "Unactive"  # Unshow on the website and preserve the data
  DE = "Delete"   # Put the data in the trash


""" ---------------------------------------------------------------------------------------------------------------- """


class Category(models.Model):
  nameFr    = models.CharField(max_length=CategoryTitleSize, default="")
  nameEn    = models.CharField(max_length=CategoryTitleSize, default="")
  resumeFr  = models.TextField(max_length=50, default="")
  resumeEn  = models.TextField(max_length=50, default="")
  status    = models.CharField(max_length=2,
                               choices=[(tag, tag.value) for tag in Status],
                               default=Status.UN)
  children  = models.ManyToManyField('self', related_name='childrenCategory')

  def __repr__(self):
    return "Category : nameFr={}, nameEn={}, resumeFr={}, resumeEn={}, status={}"\
      .format(self.nameFr, self.nameEn, self.resumeFr, self.resumeEn, self.status.value)


class CategoryStat(Stat):
  category    = models.OneToOneField(Category, on_delete=models.CASCADE, primary_key=True)


class CategoryLog(Log):
  category     = models.ForeignKey(Category     , on_delete=models.CASCADE)


""" --------------------------------------------------------------------------------------------------------------------
------------------------------------------------------------------------------------------------------------------------
Functions
------------------------------------------------------------------------------------------------------------------------
-------------------------------------------------------------------------------------------------------------------- """
" --- Creation of stat --- "
def create_stat(pCategory: Category):
  lCategory = CategoryStat()
  lCategory.category = pCategory
  lCategory.save()
  return lCategory


" --- Creation of log --- "
def create_log(pUser: AccountAdmin, pModification: str, pCategory: Category):
  lLog = CategoryLog()
  lLog.date       = datetime.now()
  lLog.modif      = pModification
  lLog.user       = pUser
  lLog.category   = pCategory
  lLog.save()
  return lLog


" --- Creation of category --- "
def create(pNameFr: str, pNameEn: str, pResumeFr: str, pResumeEn: str, pStatus: Status, pUser: AccountAdmin):

  lCategory = Category()
  lCategory.nameFr   = pNameFr
  lCategory.nameEn   = pNameEn
  lCategory.resumeFr = pResumeFr
  lCategory.resumeEn = pResumeEn
  lCategory.status   = pStatus
  lCategory.save()

  create_stat(lCategory)
  create_log(pUser, "{} {}".format(CreationText, repr(lCategory)), lCategory)

  return lCategory


" --- Modification of category --- "
def modif(pCategory: Category, pNameFr: str, pNameEn: str, pResumeFr: str, pResumeEn: str, pStatus: Status,
          pUser: AccountAdmin):

  lLog = ModificationText
  lModif = False

  if pNameFr and pNameFr != pCategory.nameFr:
    lLog += " nameFr: {},".format(pNameFr)
    pCategory.nameFr  = pNameFr
    lModif = True

  if pNameEn and pNameEn != pCategory.nameEn:
    lLog += " nameEn: {},".format(pNameEn)
    pCategory.nameEn  = pNameEn
    lModif = True

  if pResumeFr and pResumeFr != pCategory.resumeFr:
    lLog += " resumeFr: {},".format(pResumeFr)
    pCategory.resumeFr  = pResumeFr
    lModif = True

  if pResumeEn and pResumeEn != pCategory.resumeEn:
    lLog += " resumeEn: {},".format(pResumeEn)
    pCategory.resumeEn = pResumeEn
    lModif = True

  if pStatus != Status.UN and pStatus != pCategory.status:
    lLog += " status : {},".format(pStatus)
    pCategory.status = pStatus
    lModif = True

  # If any modification has been done
  if not lModif: return False
  # Else
  pCategory.save()
  create_log(pUser, lLog, pCategory)
  return pCategory


" --- Add Children category to Parent category --- "
def add_children(pParent: Category, pChildren: Category, pUser: AccountAdmin):
  pParent.children.add(pChildren)
  pParent.save()
  create_log(pUser, "Add Children {}".format(repr(pChildren)))
  return True


" --- Get logs associate to category --- "
def get_logs(pCategory: Category):
  return CategoryLog.objects.filter(category=pCategory)


" --- Get stat associate to category --- "
def get_stat(pCategory: Category):
  lResult = CategoryStat.objects.filter(category=pCategory)
  if len(lResult) != 1:
    return "Error : Any or too many results !"
  return lResult[0]


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
