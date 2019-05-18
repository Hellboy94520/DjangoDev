from django.db import models
from datetime import datetime, timedelta
from .communs import Status, LogAdmin, Stat, CreationText, ModificationText, DeletionText
from .account import AccountAdmin
from .category import Category

""" --------------------------------------------------------------------------------------------------------------------
------------------------------------------------------------------------------------------------------------------------
Data
------------------------------------------------------------------------------------------------------------------------
-------------------------------------------------------------------------------------------------------------------- """
titleMaxSize = 50

""" --------------------------------------------------------------------------------------------------------------------
------------------------------------------------------------------------------------------------------------------------
Class
------------------------------------------------------------------------------------------------------------------------
-------------------------------------------------------------------------------------------------------------------- """
class Site(models.Model):
	titre   = models.CharField(max_length=50)
	content = models.TextField()
	status  = models.CharField(max_length=2,
	                           choices=[(tag, tag.value) for tag in Status],
	                           default=Status.UN)
	category = models.OneToOneField(Category, on_delete=models.CASCADE, primary_key=True)

	def modif(self, pTitre: str, pContent: str, pAdmin: AccountAdmin):
		# Prepare the log
		lLog = ModificationText
		# Modification only if it is
		if pTitre and pTitre != self.titre:
			lLog += " titre: {},".format(pTitre)
			object.__setattr__(self, 'titre', pTitre)
		if pContent and pContent != self.content:
			lLog += " content: {},".format(pContent)
			object.__setattr__(self, 'content', pContent)
		# Save the data
		if lLog == ModificationText: return False  # If any modification has been done
		self.save()
		SiteLog(lLog, self, pAdmin)

	def to_trash(self, pAdmin: AccountAdmin):
		# TODO: Faire le système qui va vérifier s'il faut supprimer un objet ou non dans la poubelle
		self.status = Status.TR
		self.date = datetime.now() + timedelta(days=7)  # Date of deletion
		SiteLog("{} {}".format(DeletionText, repr(self)), self, pAdmin)


" -------------------------------------------------------------------------------------------------------------------- "
class SiteStat(Stat):
	site = models.OneToOneField(Site, on_delete=models.CASCADE, primary_key=True)


""" ---------------------------------------------------------------------------------------------------------------- """
class SiteLog(LogAdmin):
	site  = models.ForeignKey(Site, on_delete=models.CASCADE)


""" --------------------------------------------------------------------------------------------------------------------
------------------------------------------------------------------------------------------------------------------------
Class Functions
------------------------------------------------------------------------------------------------------------------------
-------------------------------------------------------------------------------------------------------------------- """
def create_site_stat(pSite: Site):
	lStat = SiteStat()
	lStat.site = pSite
	lStat.save()

def create_site_log(pModif: str, pSite: Site, pAdmin: AccountAdmin):
	lLog = SiteLog()
	lLog.user   = pAdmin
	lLog.site   = pSite
	lLog.modif  = pModif
	lLog.save()

def create_site(pTitre: str, pContent: str, pAdmin: AccountAdmin):
	lSite = Site()
	lSite.titre = pTitre
	lSite.content = pContent
	lSite.status = Status.UA
	lSite.save()

	# Creation of SiteStat link to Site
	create_site_stat(lSite)

	# Creation of SiteLog link to Site
	create_site_log("{}{}".format(CreationText, repr(lSite)), lSite, pAdmin)

	# Return the new Category
	return lSite


""" ---------------------------------------------------------------------------------------------------------------- """
def modif_site(pSite: Site, pTitre: str, pContent: str, pAdmin: AccountAdmin):
	pSite.titre   = pTitre
	pSite.content = pContent
	pSite.save()

	create_site_log("{}{}".format(ModificationText, repr(pSite)))

	return True