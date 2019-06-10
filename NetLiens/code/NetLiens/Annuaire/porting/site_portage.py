import logging
import re
from ..models.site import create_site, modif_site_status, set_category, set_localisation, add_keyword
from ..models.communs import Status
from ..models.account import AccountAdmin
from ..models.category import Category
from ..models.localisation import Localisation

"""
Site_status :
- 0 : Waiting sites
- 4 : Deleted
- 5 : Reported
- 9 : Validated
- 10: Special sites (OTS bug)
"""

""" --------------------------------------------------------------------------------------------------------------------
------------------------------------------------------------------------------------------------------------------------
Data
------------------------------------------------------------------------------------------------------------------------
-------------------------------------------------------------------------------------------------------------------- """
logger = logging.getLogger(__name__)
KeywordNotKeeping = ["", "de", "du", "le", "la", "les"]


""" --------------------------------------------------------------------------------------------------------------------
------------------------------------------------------------------------------------------------------------------------
Functions
------------------------------------------------------------------------------------------------------------------------
-------------------------------------------------------------------------------------------------------------------- """
def separate_keywords(pString: str):
	# Replace all non-alphanumerical caracters with a space
	lString = re.sub("[^a-zA-ZàâäôéèëêïîçùûüÿæœÀÂÄÔÉÈËÊÏÎŸÇÙÛÜÆŒ0-9]+", " ", pString)

	# Keep words in a list
	lWords = []
	for word in lString.split(" "):
		# Save the data only if it is a usefull word
		if word not in KeywordNotKeeping:
			lWords.append(word)

	return lWords


""" ---------------------------------------------------------------------------------------------------------------- """
def get_annu_site_text(pSqlCursor, pSId: int):
	pSqlCursor.execute("SELECT * FROM `annu_site_text` WHERE `site_id` = {}".format(str(pSId)))
	lAnnuSiteText = pSqlCursor.fetchall()
	if len(lAnnuSiteText) == 1:
		return lAnnuSiteText[0]


""" ---------------------------------------------------------------------------------------------------------------- """
def get_category(pSqlCursor, pSId: int):
	pSqlCursor.execute("SELECT * FROM `annu_site_appartient` WHERE `app_site_id` = {}".format(pSId))
	lAnnuSiteAppartient = pSqlCursor.fetchall()
	if len(lAnnuSiteAppartient) == 1:
		(sAppId, sAppCatId, sAppPriority) = lAnnuSiteAppartient[0]
		# MySql ID is saved in resumeFr
		lCategory = Category.objects.filter(resumeFr=str(sAppCatId))
		if lCategory.count() == 1:
			return lCategory[0]
	return None


""" ---------------------------------------------------------------------------------------------------------------- """
def get_localisation(pDept: int):
	# MySql ID is saved in nameEn
	# TODO: Search with a contain because some localisation have many id
	lLocalisation = Localisation.objects.filter(nameEn=str(pDept))
	if len(lLocalisation) == 1:
		return lLocalisation[0]
	return None


""" ---------------------------------------------------------------------------------------------------------------- """
def create_site_models(pSqlCursor, pAdmin: AccountAdmin):

	logger.debug("[Site] Conversion starting...")

	# Creation of new Site
	pSqlCursor.execute("SELECT * FROM annu_site")
	lSqlSites = pSqlCursor.fetchall()
	for(sId, sName, sUrl, sMail, sPr, sPrLast, sStatus, sDisp, sRegDate, sValDate, sMailDate, sDept, sPriority, sIp,
	    sOrig, sClic, sRss, sLienRetour, sVisRetour, sVisRetour06, sIsOffice, sIsCriteria, sIs1stPage, sSiteResidence,
	    sValidator, sPageRank, sLienRetourUrl, sPaypalTxn, sSiteInscr) in lSqlSites:

		# Get more annu_site data in annu_site_text table
		sTextId, sTextDesc, sTextInfo, sSiteDesc, sTextKeywords = "", "", "", "", ""
		lAnnuSiteText = get_annu_site_text(pSqlCursor, sId)
		if lAnnuSiteText is not None: (sTextId, sTextDesc, sTextInfo, sSiteDesc, sTextKeywords)  = lAnnuSiteText

		# Get the category of website
		lCategory = get_category(pSqlCursor, sId)

		# Get the localisation of the website
		lLocalisation = get_localisation(sDept)
		
		# Creation of the site and keyword associated
		lSite = create_site(sName, "", sTextDesc, "", sUrl, sPr, pAdmin.user)
		if sTextKeywords: add_keyword(lSite, separate_keywords(sTextKeywords), pAdmin.user)

		# If the data from annu_site_text is not found, register in log
		if not sTextId:
			modif_site_status(Status.UA, "Impossible to find annu_site_text associated to {}".format(sId), lSite, pAdmin)

		# If the data from category is not found, register in log
		if lCategory      is not None: set_category(lSite, lCategory, pAdmin.user)
		else: modif_site_status(Status.UA, "Impossible to find the category to {}".format(sId), lSite, pAdmin)

		# If the data from localisation is not found, register in log
		if lLocalisation  is not None: set_localisation(lSite, lLocalisation, pAdmin.user)
		else: modif_site_status(Status.UA, "Impossible to find the localisation to {}".format(sId), lSite, pAdmin)

	logger.debug("[Site] Conversion done")
