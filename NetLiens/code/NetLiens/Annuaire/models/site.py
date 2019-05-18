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

	def __init__(self, pTitre: str, pContent: str, pAdmin: AccountAdmin):
		models.Model.__init__(self)
		object.__setattr__(self, 'titre'  , pTitre)
		object.__setattr__(self, 'content', pContent)
		object.__setattr__(self, 'status' , Status.UN)
		self.save()
		# Creation SiteStat and SiteLog associate
		SiteStat(self)
		SiteLog("{} {}".format(CreationText, repr(self)), self, pAdmin)

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

	# Deactivate the modification by this way to be sure to have a log
	def __setattr__(self, key, value):
		pass

	# Deactivate the deletion to have personnal system
	def __del__(self):
		pass


""" ---------------------------------------------------------------------------------------------------------------- """
class SiteStat(Stat):
	site = models.OneToOneField(Site, on_delete=models.CASCADE, primary_key=True)

	def __init__(self, pSite: Site):
		Stat.__init__(self)
		self.site = pSite
		self.save()


""" ---------------------------------------------------------------------------------------------------------------- """
class SiteLog(LogAdmin):
	site  = models.ForeignKey(Site, on_delete=models.CASCADE)

	def __init__(self, pModif: str, pSite: Site, pAdmin: AccountAdmin):
		LogAdmin.__init__(self)
		self.user     = pAdmin
		self.modif    = pModif
		self.site     = pSite
		self.save()
