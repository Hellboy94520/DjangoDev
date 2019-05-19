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
  objects = None
  nameFr    = models.CharField(max_length=CategoryTitleSize, default="")
  nameEn    = models.CharField(max_length=CategoryTitleSize, default="")
  resumeFr  = models.TextField(max_length=50, default="")
  resumeEn  = models.TextField(max_length=50, default="")
  status    = models.CharField(max_length=2,
                               choices=[(tag, tag.value) for tag in Status],
                               default=Status.UN)
  children  = models.ManyToManyField('self', related_name='childrenCategory')
  date      = models.DateField(default=datetime.now())    # Creation Date

  def get_logs(self):
    return CategoryLog.objects.filter(category=self)

  def get_stat(self):
    return CategoryStat.objects.get(category=self)

  def __repr__(self):
    return "Category : nameFr={}, nameEn={}, resumeFr={}, resumeEn={}, status={}, date={}"\
      .format(self.nameFr, self.nameEn, self.resumeFr, self.resumeEn, str(self.status), self.date)


""" ---------------------------------------------------------------------------------------------------------------- """
class CategoryStat(Stat):
  category    = models.OneToOneField(Category, on_delete=models.CASCADE, primary_key=True)


""" ---------------------------------------------------------------------------------------------------------------- """
class CategoryLog(LogAdmin):
  category     = models.ForeignKey(Category  , on_delete=models.CASCADE)


""" --------------------------------------------------------------------------------------------------------------------
------------------------------------------------------------------------------------------------------------------------
Class Functions
------------------------------------------------------------------------------------------------------------------------
-------------------------------------------------------------------------------------------------------------------- """
" -------------------------------------------------------------------------------------------------------------------- "
def create_category_stat(pCategory: Category):
  lStat = CategoryStat()
  lStat.category = pCategory
  lStat.save()

def create_category_log(pModif: str, pCategory: Category, pAdmin: AccountAdmin):
  lLog = CategoryLog()
  lLog.modif = pModif
  lLog.category = pCategory
  lLog.user = pAdmin
  lLog.save()

def create_category(pNameFr: str, pNameEn: str, pResumeFr: str, pResumeEn: str, pStatus: Status, pAdmin: AccountAdmin):
  # Creation of the category
  lCategory = Category()
  lCategory.nameFr = pNameFr
  lCategory.nameEn = pNameEn
  lCategory.resumeFr = pResumeFr
  lCategory.resumeEn = pResumeEn
  lCategory.status = pStatus
  lCategory.save()

  # Creation of CategoryStat link to Category
  create_category_stat(lCategory)

  # Creation of CategoryLog link to Category
  create_category_log("{}{}".format(CreationText, repr(lCategory)), lCategory, pAdmin)

  # Return the new Category
  return lCategory


" -------------------------------------------------------------------------------------------------------------------- "
def modif_category(pCategory: Category, pAdmin: AccountAdmin, pNameFr="", pNameEn="", pResumeFr="", pResumeEn=""):
  # Modification of the data
  if pNameFr:   pCategory.nameFr = pNameFr
  if pNameEn:   pCategory.nameEn = pNameEn
  if pResumeFr: pCategory.resumeFr = pResumeFr
  if pResumeEn: pCategory.resumeEn = pResumeEn

  # Save the data
  pCategory.save()
  
  # Creation of the modification log
  create_category_log("{}{}".format(ModificationText, repr(pCategory)), pCategory, pAdmin)
  return True

def modif_category_status(pCategory: Category, pStatus: Status, pAdmin: AccountAdmin):
  # TODO
  pass


" -------------------------------------------------------------------------------------------------------------------- "
def add_children(pParent: Category, pChildren: Category, pUser: AccountAdmin):
  pParent.children.add(pChildren)
  pParent.save()
  CategoryLog("Add Children {}".format(repr(pChildren)), pParent, pUser)
  return True


""" --------------------------------------------------------------------------------------------------------------------
------------------------------------------------------------------------------------------------------------------------
Database Functions
------------------------------------------------------------------------------------------------------------------------
-------------------------------------------------------------------------------------------------------------------- """
" --- Get the much see category --- "
def get_much_see_category(pTimePeriod: str, pQuantity: int, pReverse: bool):

  if pReverse is True: lParam = "-" + pTimePeriod
  else:                lParam = pTimePeriod

  try:
    categoryStatList = CategoryStat.objects.order_by(lParam)[0:pQuantity]
  except IOError as e:
    return "error: {}".format(e)

  categoryList = []

  for categoryStat in categoryStatList:
    categoryList.append(categoryStat.category)

  return categoryList
