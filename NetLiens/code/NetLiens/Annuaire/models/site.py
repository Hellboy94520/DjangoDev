from django.db import models
from .account import User, AccountAdmin
from .category import Category
from .localisation import Localisation
from .stat import Stat
# from .keyword import Keyword, create_new_keyword, is_exist

from enum import Enum
from datetime import datetime


""" --------------------------------------------------------------------------------------------------------------------
------------------------------------------------------------------------------------------------------------------------
HOW TO USE

- Site creation from an Administrator: 
        lSite = Site(titleFr="toto", [...])
        lSite.create(lAdminAccount)

- Site request creation from a user: 
        lSite = Site(titleFr="toto", [...])
        lSite.request_creation(lUser)

- Site change display status from an Administrator:
        lSite.show(bool, lAccount)

- Site modification from an Administrator only:
        lSite.nameFr = "toto"
        lSite.modification(lAdminAccount)

- Site deletion from an Administrator only:
        lSite.erase(lAccountAdmin)


------------------------------------------------------------------------------------------------------------------------
-------------------------------------------------------------------------------------------------------------------- """


""" --------------------------------------------------------------------------------------------------------------------
------------------------------------------------------------------------------------------------------------------------
Data
------------------------------------------------------------------------------------------------------------------------
-------------------------------------------------------------------------------------------------------------------- """
titleMaxSize = 50
reasonMaxSize = 50


""" --------------------------------------------------------------------------------------------------------------------
------------------------------------------------------------------------------------------------------------------------
Class
------------------------------------------------------------------------------------------------------------------------
-------------------------------------------------------------------------------------------------------------------- """
class Site(models.Model):
  objects = None
  titleFr       = models.CharField(max_length=titleMaxSize, default="")
  titleEn       = models.CharField(max_length=titleMaxSize, default="")
  contentFr     = models.TextField(default="")
  contentEn     = models.TextField(default="")
  website       = models.URLField(default="")
  nllevel       = models.IntegerField(max_length=10, default=0)
  category      = models.ForeignKey(Category,     on_delete=models.CASCADE, null=True, default=None)
  localisation  = models.ForeignKey(Localisation, on_delete=models.CASCADE, null=True, default=None)
  display       = models.BooleanField(default=False)
  # keywords      = models.ManyToManyField(Keyword)

  """ ---------------------------------------------------- """
  def create(self, admin: AccountAdmin):
    # Creation in database
    self.display
    self.save()
    # Creation of the log
    lDetails = "Creation of " + str(self)
    lLog = SiteLog(user=admin.user,
                   site=self,
                   type=LogType.CR,
                   details=lDetails)
    lLog.save()
    # Creation of the stat
    lStat = SiteStat(localisation=self,
                     creation_user=admin.user,
                     validation_date=datetime.now(),
                     validation_user=admin.user)
    lStat.create()

  """ ---------------------------------------------------- """
  def request_creation(self, user:User):
    # Creation in database
    self.display = False
    self.save()
    # Creation of the log
    lDetails = "Request Creation"
    lSiteLog = SiteLog(user=user,
                       site=self,
                       type=LogType.RC,
                       details=lDetails)
    lSiteLog.save()
    # Creation of the stat
    lSiteStat = SiteStat(category=self, creation_user=user)
    lSiteStat.create()
    # Creation of the event
    lSiteEvent = SiteEventCreationRequest(user 		= user,
                                          site    = None)
    lSiteEvent.save()

  """ ---------------------------------------------------- """
  def modification(self, user: User):
    # Save the data
    self.save()
    # Creation of the log
    lDetails = "Modification of '" + str(self) + "'"
    lLog = SiteLog(user     = user,
                   site     = self,
                   type     = LogType.MO,
                   details  = lDetails)
    lLog.save()

  """ ---------------------------------------------------- """
  def get_logs(self):
    return SiteLog.objects.filter(site=self)

  """ ---------------------------------------------------- """
  def get_stat(self):
    return SiteStat.objects.get(site=self)

  """ ---------------------------------------------------- """
  def __repr__(self):
    return "Site : titleFr={}, titleEn={}, contentFr={}, contentEn={}, website={}, nllevel={}"\
      .format(self.titleFr, self.titleEn, self.contentFr, self.contentEn,
              self.website, self.NLlevel)


""" --------------------------------------------------------------------------------------------------------------------
------------------------------------------------------------------------------------------------------------------------
Class Event
------------------------------------------------------------------------------------------------------------------------
-------------------------------------------------------------------------------------------------------------------- """
class SiteEventCreationRequest(models.Model):
  objects = None
  date     = models.DateTimeField(default=datetime.now())
  saw      = models.BooleanField(default=False)
  user     = models.ForeignKey(User, on_delete=models.CASCADE)
  site     = models.ForeignKey(Site, on_delete=models.CASCADE)

  """ ---------------------------------------------------- """
  def accept(self, admin: AccountAdmin):
    # Creation of the log
    lDetail = "Request Accept from '" + admin.user.username + "'"
    lSiteLog = SiteLog(user     = admin.user   ,
                       site     = self.site,
                       type     = LogType.CR   ,
                       details  = lDetail)
    lSiteLog.save()
    # Complete the Stat object
    lSiteStat = self.site.get_stat()
    lSiteStat.validation_date = datetime.now()
    lSiteStat.validation_user = admin.user
    lSiteStat.save()
    # Display the category on website
    self.site.display = True
    self.site.save()
    # Delete the event
    self.delete()

  """ ---------------------------------------------------- """
  def refuse(self, admin: AccountAdmin):
    # Delete the category and the event (by cascade)
    self.site.delete()

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
  # TODO
  UN = "unknown"
  RC = "creation_request"
  RM = "modification_request"
  CR = "creation"
  MO = "modification"


""" ---------------------------------------------------------------------------------------------------------------- """
class SiteLog(models.Model):
  objects = None
  date      = models.DateTimeField(default=datetime.now())
  user      = models.ForeignKey(User, default=None, null=True, on_delete=models.SET_NULL)
  site      = models.ForeignKey(Site, on_delete=models.CASCADE)
  type      = models.CharField(max_length=2,
                               choices=[(tag, tag.value) for tag in LogType],
                               default=LogType.UN)
  details   = models.TextField(default="")


""" --------------------------------------------------------------------------------------------------------------------
------------------------------------------------------------------------------------------------------------------------
Class Stat
------------------------------------------------------------------------------------------------------------------------
-------------------------------------------------------------------------------------------------------------------- """
class SiteStat(Stat):
  site = models.OneToOneField(Site, on_delete=models.CASCADE, primary_key=True)
