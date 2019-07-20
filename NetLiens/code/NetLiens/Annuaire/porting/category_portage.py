from ..models.account import AccountAdmin
from ..models.category import Category

""" --------------------------------------------------------------------------------------------------------------------
Data
-------------------------------------------------------------------------------------------------------------------- """
_equivLoc = {}

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
		                     resumeFr = str(sParent),
		                     display  = sShow)
		lCategory.create(account)
		_equivLoc[sId] = CategoryPorting(sqlId=sId, sqlIdParent=sParent, category=lCategory)

	""" Association parent-children """
	for sId, sCategoryPorting in _equivLoc.items():
		if sCategoryPorting.sqlIdParent != 0:
			lParent = _equivLoc.get(sCategoryPorting.sqlIdParent, None)
			if lParent is not None:
				sCategoryPorting.category.set_parent(lParent, account)
			else:
				sCategoryPorting.category.change_display(False, account, "No parent founded")

	return True


""" ---------------------------------------------------------------------------------------------------------------- """
def reset_category_model(account: AccountAdmin):
	for lCategory in Category.objects.all():
		lCategory.nameEn   = ""
		lCategory.resumeFr = ""
		lCategory.modification(account, "Remove useless data")


""" ------------------------------------------------------------------------------------------------------------------
CategoryPorting
------------------------------------------------------------------------------------------------------------------ """
class CategoryPorting:
	def __init__(self, sqlId: int, sqlIdParent: int, category: Category):
		self.sqlId        = sqlId
		self.sqlIdParent  = sqlIdParent
		self.category     = category