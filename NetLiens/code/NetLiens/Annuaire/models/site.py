from django.db import models
# from .communs import Status, statusToValue, LogUser, LogAdmin, Stat, LogType, LogLevel
# from .account import User, AccountAdmin
# from .category import Category
# from .localisation import Localisation
# from .keyword import Keyword, create_new_keyword, is_exist
#
# """ --------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------
# Data
# ------------------------------------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------------------------- """
# titleMaxSize = 50
# reasonMaxSize = 50
#
#
""" --------------------------------------------------------------------------------------------------------------------
------------------------------------------------------------------------------------------------------------------------
Class
------------------------------------------------------------------------------------------------------------------------
-------------------------------------------------------------------------------------------------------------------- """
class Site(models.Model):
	objects = None
	# titleFr       = models.CharField(max_length=50, default="")
	# titleEn       = models.CharField(max_length=50, default="")
	# contentFr     = models.TextField(default="")
	# contentEn     = models.TextField(default="")
	# status        = models.CharField(max_length=2,
	#                                  choices=[(tag, tag.value) for tag in Status],
	#                                  default=Status.UN)
	# website       = models.URLField(default="")
	# NLlevel       = models.IntegerField(max_length=10, default=0)
	# category      = models.ForeignKey(Category,     on_delete=models.CASCADE, null=True, default=None)
	# localisation  = models.ForeignKey(Localisation, on_delete=models.CASCADE, null=True, default=None)
	# keywords      = models.ManyToManyField(Keyword)
	#
	# def get_logs(self):
	# 	return SiteLog.objects.filter(site=self)
	#
	# def get_stat(self):
	# 	return SiteStat.objects.get(site=self)
	#
	# def __repr__(self):
	# 	return "Site : titleFr={}, titleEn={}, contentFr={}, contentEn={}, status={}, website={}, nllevel={}"\
	# 		.format(self.titleFr, self.titleEn, self.contentFr, self.contentEn, statusToValue(self.status),
	# 	          self.website, self.NLlevel)
#
#
# " -------------------------------------------------------------------------------------------------------------------- "
# class SiteStat(Stat):
# 	objects = None
# 	site = models.OneToOneField(Site, on_delete=models.CASCADE, primary_key=True)
#
#
# """ ---------------------------------------------------------------------------------------------------------------- """
# class SiteLog(LogUser):
# 	objects = None
# 	site  = models.ForeignKey(Site, on_delete=models.CASCADE)
#
#
# """ ---------------------------------------------------------------------------------------------------------------- """
# class SiteLogAdmin(LogAdmin):
# 	objects = None
# 	site  = models.ForeignKey(Site, on_delete=models.CASCADE)


# """ --------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------
# Class Functions
# ------------------------------------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------------------------- """
# def create_site_stat(pSite: Site):
# 	lStat = SiteStat()
# 	lStat.site = pSite
# 	lStat.save()
#
# def create_site_log(pText: str, pLevel: LogLevel, pType: LogType, pSite: Site, pUser: User):
# 	lLog = SiteLog()
# 	lLog.user   = pUser
# 	lLog.site   = pSite
# 	lLog.level  = pLevel
# 	lLog.type   = pType
# 	lLog.text   = pText
# 	lLog.save()
#
# def create_site_log_admin(pText: str, pLevel: LogLevel, pType: LogType, pSite: Site, pAdmin: AccountAdmin):
# 	lLog = SiteLogAdmin()
# 	lLog.user   = pAdmin
# 	lLog.site   = pSite
# 	lLog.level  = pLevel
# 	lLog.type   = pType
# 	lLog.text   = pText
# 	lLog.save()
#
# def create_site(pTitleFr: str, pTitleEn: str, pContentFr: str, pContentEn: str, pWebsite: str, pNLLevel: int,
#                 pUser: User):
# 	lSite = Site()
# 	lSite.titleFr   = pTitleFr
# 	lSite.titleEn   = pTitleEn
# 	lSite.contentFr = pContentFr
# 	lSite.contentEn = pContentEn
# 	lSite.website   = pWebsite
# 	lSite.NLlevel   = pNLLevel
# 	lSite.status    = Status.UA
# 	lSite.save()
#
# 	# Creation of SiteStat link to Site
# 	create_site_stat(lSite)
#
# 	# Creation of SiteLog link to Site
# 	create_site_log(repr(lSite), LogLevel.DE, LogType.CR, lSite, pUser)
#
# 	# Return the new Category
# 	return lSite
#
#
# """ ---------------------------------------------------------------------------------------------------------------- """
# def modif_site(pSite: Site, pUser: User, pTitleFr="", pTitleEn="", pContentFr="", pContentEn="", pWebsite="",
#                pNLLevel=""):
# 	# Modification of the data
# 	if pTitleFr: pSite.titleFr      = pTitleFr
# 	if pTitleEn: pSite.titleEn      = pTitleEn
# 	if pContentFr: pSite.contentFr  = pContentFr
# 	if pContentEn: pSite.contentEn  = pContentEn
# 	if pWebsite: pSite.website      = pWebsite
# 	if pNLLevel: pSite.NLlevel      = pNLLevel
#
# 	# Save the data
# 	pSite.save()
#
# 	# Creation of the modification log
# 	create_site_log(repr(pSite), LogLevel.DE, LogType.MO, pSite, pUser)
#
# 	return True
#
#
# """ ---------------------------------------------------------------------------------------------------------------- """
# def modif_site_status(pStatus: Status, pReason: str, pSite: Site, pAdmin: AccountAdmin):
# 	# Creation of text log
# 	lLog = "Change status {} to {} for reason {}".format(statusToValue(pSite.status) ,
# 	                                                     statusToValue(pStatus)      ,
# 	                                                     pReason)
#
# 	# Save data
# 	pSite.status = pStatus
# 	pSite.save()
#
# 	# Creation of the log
# 	create_site_log_admin(lLog, LogLevel.WA, LogType.MO, pSite, pAdmin)
#
# 	return True
#
#
# """ ---------------------------------------------------------------------------------------------------------------- """
# def set_category(pSite: Site, pCategory: Category, pUser: User):
# 	# Preparation of the log
# 	lLog = "Set Category: {}".format(repr(pCategory))
#
# 	# Check Category Status
# 	if pCategory.status != Status.AC:
# 		create_site_log("Impossible to set a category with status \'{}\'".format(statusToValue(pCategory.status)),
# 		                LogLevel.WA, LogType.MO, pSite, pUser)
# 		return False
#
# 	# Save Data
# 	pSite.category = pCategory
# 	pSite.save()
#
# 	# Creation of the log
# 	create_site_log(lLog, LogLevel.DE, LogType.MO, pSite, pUser)
#
# 	return True
#
#
# """ ---------------------------------------------------------------------------------------------------------------- """
# def set_localisation(pSite: Site, pLocalisation: Localisation, pUser: User):
# 	# Preparation of the log
# 	lLog = "Set Localisation: {}".format(repr(pLocalisation))
#
# 	# Check Localisation Status
# 	if pLocalisation.status != Status.AC:
# 		create_site_log("Impossible to set a localisation with status \'{}\'".format(statusToValue(pLocalisation.status)),
# 		                LogLevel.WA, LogType.MO, pSite, pUser)
# 		return False
#
# 	# Save data
# 	pSite.localisation = pLocalisation
# 	pSite.save()
#
# 	# Creation of the log
# 	create_site_log(lLog, LogLevel.DE, LogType.MO, pSite, pUser)
#
# 	return True
#
#
# """ ---------------------------------------------------------------------------------------------------------------- """
# def add_keyword(pSite: Site, pKeywords: [], pUser: User):
# 	# Preparation of the log
# 	lLog = "Add Keywords: "
# 	for i, keyword in enumerate(pKeywords):
# 		# Lower the string
# 		lKeyword = keyword.lower()
#
# 		# Creation/Complete the log
# 		if i == 0: lLog += lKeyword
# 		else:      lLog += ", {}".format(lKeyword)
#
# 		# Creation/Get the keyword
# 		lKeyword = create_new_keyword(lKeyword)
#
# 		# Add Keyword to Site
# 		pSite.keywords.add(lKeyword)
#
# 	pSite.save()
# 	# Creation of the log
# 	create_site_log(lLog, LogLevel.DE, LogType.MO, pSite, pUser)
# 	return True
#
#
# """ ---------------------------------------------------------------------------------------------------------------- """
# def remove_keyword(pSite: Site, pKeywords: [], pUser: User):
# 	# Preparation of the log
# 	lLog = "Remove Keywords: "
#
# 	for i, keyword in enumerate(pKeywords):
# 		# Lower the string
# 		lKeyword = keyword.lower()
#
# 		# Creation/Complete the log
# 		if i == 0: lLog += lKeyword
# 		else:      lLog += ", {}".format(lKeyword)
#
# 		# Get keyword
# 		lKeyword = is_exist(keyword)
#
# 		# Remove Keyword to Site
# 		pSite.keywords.remove(lKeyword)
#
# 	pSite.save()
# 	# Creation of the log
# 	create_site_log(lLog, LogLevel.DE, LogType.MO, pSite, pUser)
#
# 	return True
