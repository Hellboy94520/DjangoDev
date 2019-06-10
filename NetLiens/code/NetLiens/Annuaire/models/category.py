from django.db import models
from datetime import datetime
from .account import User, AccountAdmin
from .stat import Stat
from .site import Site
from enum import Enum

""" --------------------------------------------------------------------------------------------------------------------
------------------------------------------------------------------------------------------------------------------------
HOW TO USE

- Category creation from an Administrator: 
        lCategory = Category(nameFr="toto", [...])
        lCategory.create(lAdminAccount)
        
- Category request creation from a user: 
        lCategory = Category(nameFr="toto", [...])
        lCategory.request_creation(lUser)
        
- Category change display status from an Administrator:
        lCategory.show(bool, lAccount)
        
- Category modification from an Administrator only:
        lCategory.nameFr = "toto"
        lCategory.modification(lAdminAccount)
        
- Category deletion from an Administrator only:
        lCategory.erase(lAccountAdmin)
        
- Accept the request creation of a new category from an Administrator only:
        lCategoryEventCreationRequest.accept(lAdminAccount)
        
- Refuse the request creation of a new category from an Administrator only:
        lCategoryEventCreationRequest.accept(lAdminAccount)
        
------------------------------------------------------------------------------------------------------------------------
-------------------------------------------------------------------------------------------------------------------- """


""" --------------------------------------------------------------------------------------------------------------------
------------------------------------------------------------------------------------------------------------------------
Data
------------------------------------------------------------------------------------------------------------------------
-------------------------------------------------------------------------------------------------------------------- """
# TODO: Define size with portage and display
CategoryNameSize    = 100
CategoryResumeSize  = 100


""" --------------------------------------------------------------------------------------------------------------------
------------------------------------------------------------------------------------------------------------------------
Class Data
------------------------------------------------------------------------------------------------------------------------
-------------------------------------------------------------------------------------------------------------------- """
class Category(models.Model):
  objects = None
  nameFr    = models.CharField(max_length=CategoryNameSize,    default="")
  nameEn    = models.CharField(max_length=CategoryNameSize,    default="")
  resumeFr  = models.CharField(max_length=CategoryResumeSize,  default="")
  resumeEn  = models.CharField(max_length=CategoryResumeSize,  default="")
  display   = models.BooleanField(default=False)
  parent    = models.ForeignKey('self', default=None, null=True, on_delete=models.SET_NULL)

  """ ---------------------------------------------------- """
  def create(self, admin: AccountAdmin):
    # Creation in database
    self.save()
    # Creation of the log
    lDetails = "Creation of " + str(self)
    lCategoryLog = CategoryLog(user     = admin.user,
                               category = self       ,
                               type     = LogType.CR ,
                               details  = lDetails)
    lCategoryLog.save()
    # Creation of the stat
    lCategoryStat = CategoryStat(category=self                 ,
                                 creation_user=admin.user     ,
                                 validation_date=datetime.now(),
                                 validation_user=admin.user)
    lCategoryStat.create()

  """ ---------------------------------------------------- """
  def modification(self, admin: AccountAdmin, details=""):
    # Save the modification in database
    self.save()
    # Creation of the log
    lDetails = "Modification of '" + str(self) + "'. " + details
    lCategoryLog = CategoryLog(user     = admin.user,
                               category = self       ,
                               type     = LogType.MO  ,
                               details  = lDetails)
    lCategoryLog.save()

  """ ---------------------------------------------------- """
  def show(self, display: bool, admin: AccountAdmin, details=""):
    # TODO: Check before if a parent exist and site associated exist
    self.display = display
    self.save()
    # Creation of the log
    lDetails = "Change display to " + str(self.display) + ". " + details
    lCategoryLog = CategoryLog(user     = admin.user,
                               category = self      ,
                               type     = LogType.MO,
                               details  = lDetails)
    lCategoryLog.save()



  """ ---------------------------------------------------- """
  # TODO: When Site will be create add site in parameter
  # def request_creation(self, user: User, pSite: Site, details=""):
  def request_creation(self, user: User, details=""):
    # Undisplay the Category
    self.display = False
    self.save()
    # Creation of the log
    lDetails = "Request Creation for reason '" + details + "'"
    lCategoryLog = CategoryLog(user     = user      ,
                               category = self      ,
                               type     = LogType.RC,
                               details  = lDetails)
    lCategoryLog.save()
    # Creation of the stat
    lCategoryStat = CategoryStat(category=self, creation_user=user)
    lCategoryStat.create()
    # Creation of the event
    lCategoryEvent = CategoryEventCreationRequest(user 		 = user,
                                                  # TODO: site 		 = site,
                                                  site = None,
                                                  category = self)
    lCategoryEvent.save()

  """ ---------------------------------------------------- """
  def set_parent(self, parent, admin: AccountAdmin):
    # Add Children
    self.parent = parent
    self.save()
    # Creation of the log
    lDetails = "Set Parent " + str(parent)
    lCategoryLog = CategoryLog(user     = admin.user,
                               category = self      ,
                               type     = LogType.MO,
                               details  = lDetails)
    lCategoryLog.save()

  """ ---------------------------------------------------- """
  def erase(self, admin: AccountAdmin):
    # Move Children Category to Parent of this Category
    for lChildren in Category.objects.filter(parent=self):
      lChildren.set_parent(self.parent, admin)
    # And delete the category
    self.delete()

  """ ---------------------------------------------------- """
  def get_logs(self):
    return CategoryLog.objects.filter(category=self)

  """ ---------------------------------------------------- """
  def get_stat(self):
    return CategoryStat.objects.get(category=self)

  """ ---------------------------------------------------- """
  def __str__(self):
    return "Category : nameFr={}, nameEn={}, resumeFr={}, resumeEn={}, status={}"\
      .format(self.nameFr, self.nameEn, self.resumeFr, self.resumeEn, str(self.display))


""" --------------------------------------------------------------------------------------------------------------------
------------------------------------------------------------------------------------------------------------------------
Class Event
------------------------------------------------------------------------------------------------------------------------
-------------------------------------------------------------------------------------------------------------------- """
class CategoryEventCreationRequest(models.Model):
  objects = None
  date     = models.DateTimeField(default=datetime.now())
  saw      = models.BooleanField(default=False)
  user     = models.ForeignKey(User, on_delete=models.CASCADE)
  site     = models.ForeignKey(Site, on_delete=models.CASCADE)
  category = models.ForeignKey(Category, on_delete=models.CASCADE)

  """ ---------------------------------------------------- """
  def accept(self, admin: AccountAdmin):
    # Creation of the log
    lDetail = "Request Accept from '" + admin.user.username + "'"
    lCategoryLog = CategoryLog(user     = admin.user   ,
                               category = self.category,
                               type     = LogType.CR   ,
                               details  = lDetail)
    lCategoryLog.save()
    # Complete the Stat object
    lCategoryStat = self.category.get_stat()
    lCategoryStat.validation_date = datetime.now()
    lCategoryStat.validation_user = admin.user
    lCategoryStat.save()
    # Display the category on website
    self.category.display = True
    self.category.save()
    # Delete the event
    self.delete()

  """ ---------------------------------------------------- """
  def refuse(self, admin: AccountAdmin):
    # Delete the category and the event (by cascade)
    self.category.delete()

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
class CategoryLog(models.Model):
  objects = None
  date      = models.DateTimeField(default=datetime.now())
  user      = models.ForeignKey(User, default=None, null=True, on_delete=models.SET_NULL)
  category  = models.ForeignKey(Category, on_delete=models.CASCADE)
  type      = models.CharField(max_length=2,
                               choices=[(tag, tag.value) for tag in LogType],
                               default=LogType.UN)
  details   = models.TextField(default="")


""" --------------------------------------------------------------------------------------------------------------------
------------------------------------------------------------------------------------------------------------------------
Class Stat
------------------------------------------------------------------------------------------------------------------------
-------------------------------------------------------------------------------------------------------------------- """
class CategoryStat(Stat):
  category = models.OneToOneField(Category, on_delete=models.CASCADE, primary_key=True)

