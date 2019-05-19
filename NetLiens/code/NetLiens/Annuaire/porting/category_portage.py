import logging
from ..models import AccountAdmin, Status, Category, create_category

logger = logging.getLogger(__name__)


""" ------------------------------------------------------------------------------------------------------------------
Category
------------------------------------------------------------------------------------------------------------------ """
def create_category_models(pSqlCursor, pAdmin: AccountAdmin):

	logger.debug("[Category] Conversion starting...")

	# key = Id (SQL), value = Category (MongoDb)
	lEquivalence = {}

	# Creation of new Category
	pSqlCursor.execute("SELECT * FROM annu_cats")
	lSqlCategory = pSqlCursor.fetchall()
	for (sId, sName, sParent, sPriority, sShow, sLocked, sGeo, sType, sColor) in lSqlCategory:

		if sShow:
			lStatus = Status.AC
		else:
			lStatus = Status.UN

		# Save temporarely the  parent in nameEn
		lCategory = create_category(sName, str(sParent), "", "", lStatus, pAdmin)
		lEquivalence[sId] = lCategory

	# Associated parent and children, only if status is available
	for lId, lCategory in lEquivalence.items():
		# Dans le cas ou il n'y a pas de parent
		if int(lCategory.nameEn) == 0:
			lCategory.save()
		else:
			lParent = lEquivalence.get(int(lCategory.nameEn), None)
			# If parent is founded
			if lParent is not None:
				lCategory.nameEn = ""
				lParent.children.add(lCategory)
				lParent.save()
			else:
				logger.error("[Category] Impossible to find the parent of {}-{}".format(lId, lCategory.nameFr))

	logger.debug("[Category] Conversion done")


def reset_category_useless_data():
	for lCategory in Category.objects.all():
		lCategory.nameEn = ""
		lCategory.save()
