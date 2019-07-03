from ..models.account import AccountAdmin, User
from ..models.category import Category


""" ------------------------------------------------------------------------------------------------------------------
Category
------------------------------------------------------------------------------------------------------------------ """
def create_category_models(pSqlCursor, account: AccountAdmin):

	""" Creation of the category """
	pSqlCursor.execute("SELECT * FROM annu_cats")
	lSqlCategory = pSqlCursor.fetchall()
	for (sId, sName, sParent, sPriority, sShow, sLocked, sGeo, sType, sColor) in lSqlCategory:

		# Save temporarely oldId in nameEn and parentId in resumeFr
		lCategory = Category(nameFr   = sName,
		                     nameEn   = str(sId),
		                     resumeFr = str(sParent),
		                     display  = sShow)
		lCategory.create(account)

	""" Association parent-children """
	for lCategory in Category.objects.all():
		lOldId    = int(lCategory.nameEn)
		lParentId = int(lCategory.resumeFr)
		if lParentId != 0:
			lParent = Category.objects.filter(nameEn=lOldId)
			# If a parent is found
			if   len(lParent) == 1:
				lCategory.set_parent(lParent[0], account)
			# If no parent are founded, deactivated the category
			elif len(lParent) == 0:
				lCategory.change_display(False, account, "No parent founded")
			# If many parents are founded, deactivated the category
			else:
				lCategory.change_display(False, account, "Find {} parents".format(len(lParent)))

	return True


""" ---------------------------------------------------------------------------------------------------------------- """
def reset_category_model(account: AccountAdmin):
	for lCategory in Category.objects.all():
		lCategory.nameEn   = ""
		lCategory.resumeFr = ""
		lCategory.modification(account, "Remove useless data")
