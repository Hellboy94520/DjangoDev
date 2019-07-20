from ..models.account import AccountAdmin
from ..models.category import Site
from ..porting.localisation_portage import _equivLoc
from ..porting.category_portage import _equivCat

from re import match

""" ------------------------------------------------------------------------------------------------------------------
Site
------------------------------------------------------------------------------------------------------------------ """
def create_site_models(pSqlCursor, account: AccountAdmin):

	""" Creation of the site """
	pSqlCursor.execute("SELECT * from annu_site")
	lSqlSite = pSqlCursor.fetchall()
	for (sId, sName, sUrl, sMail, sPr, sPrDate, sStatus, sDispMode, sRegdate, sValidDate, sDept, sPriority, sIp, sOrigine,
	     sClics, sRss, sLienRetour, sVisRetour, sIsOfficeTourisme, sIsCriteria, sIsFirstPage, sResidence, sValidator,
	     sPageRank, sRetourUrl, sPaypalTxn, sTypeinscr) in lSqlSite:
		# Construction of the site
		lSite = Site(nameFr   = sName,
		             website  = sUrl,
		             localisation = _equivLoc.get(sDept, None))
		lSite.create(account)

		# Search the category parent
		pSqlCursor.execute("SELECT * FROM `annu_site_appartient` WHERE `app_site_id` = {}".format(sId))
		lSqlAppartient = pSqlCursor.fetchall()
		if len(lSqlAppartient) == 1:
			sSiteId, sCatId, sPriority = lSqlAppartient[0]
			lCategoryPorting = _equivCat.get(sCatId, None)
			if lCategoryPorting is not None:
				lSite.category = lCategoryPorting

		# TODO: Set the NL

		# TODO: Search the content in annu_site_text

		# TODO: Set the display with sStatus

		# Creation of the site
		lSite.save()