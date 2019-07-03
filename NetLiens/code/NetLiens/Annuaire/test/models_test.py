from ..models import Category, CategoryEventCreationRequest
from ..models import Localisation, LocalisationType, LocalisationEventCreationRequest
from ..models import AccountAdmin, User

def run():
	try_account("test_models")
	lUser = User.objects.get(username="test_models")
	lAccount = AccountAdmin.objects.get(user=lUser)
	try_category(lAccount)
	try_localisation(lAccount)

def try_account(username: str):
	lAccount = AccountAdmin()
	lAccount.create(username=username,
	                email="alexandre.delahaye@free.fr",
	                password="toto",
	                first_name="Alex",
	                last_name="Delahaye")

	return True


def try_category(account: AccountAdmin):
	lCarCat = Category(nameFr="Car", resumeFr="Brand Company")
	lCarCat.create(account)

	lAudiCat = Category(nameFr="Audi", nameEn="Audi", resumeFr="Marque allemande", resumeEn="Germany company")
	lAudiCat.create(account)
	lBMWCat = Category(nameFr="BMW", nameEn="BMW", resumeFr="Marque allemande", resumeEn="Germany company")
	lBMWCat.create(account)

	lAudiCat.set_parent(lCarCat, account)
	lBMWCat .set_parent(lCarCat, account)

	lRequestCat = Category(nameFr="Renault")
	lRequestCat.request_creation(account.user, "Not exist")
	lRequestCat.set_parent(lCarCat, account)
	lRequest = CategoryEventCreationRequest.objects.filter()[0]
	lRequest.accept(account)

	lRequestCat = Category(nameFr="Scooter")
	lRequestCat.request_creation(account.user, "Not exist")
	lRequest = CategoryEventCreationRequest.objects.filter()[0]
	lRequest.refuse(account)

	lA1 = Category(nameFr="A1")
	lA1.create(account)
	lA1.set_parent(lAudiCat, account)
	lA2 = Category(nameFr="A2")
	lA2.create(account)
	lA2.set_parent(lAudiCat, account)

	lA2 = Category.objects.get(nameFr="A2")
	lA2.erase(account)        # No Children
	lAudiCat = Category.objects.get(nameFr="Audi")
	lAudiCat.erase(account)   # Children and Parent
	lCarCat.erase(account)    # Children and no Parent

	return True


def try_localisation(account: AccountAdmin):
	lEurope = Localisation(nameFr = "Europe",
	                       nameEn = "Europe",
	                       code   = "EU",
	                       type   = LocalisationType.CO)
	lEurope.create(account)

	lAsie = Localisation(nameFr = "Asie",
	                     nameEn = "Asia",
	                     code   = "AD",
	                     type   = LocalisationType.CO)
	lAsie.create(account)

	lFrance = Localisation(nameFr = "France",
	                       nameEn = "France",
	                       code   = "FR",
	                       type   = LocalisationType.CU)
	lFrance.create(account)
	lFrance.set_parent(lEurope, account)

	lRequestLoc = Localisation(nameFr = "Allemagne",
	                           nameEn = "Germany",
	                           code   = "GE",
	                           type   = LocalisationType.CU)
	lRequestLoc.request_creation(account.user, "Not exist")
	lRequest = LocalisationEventCreationRequest.objects.filter()[0]
	lRequest.accept(account)

	lRequestLoc = Localisation(nameFr = "Chine",
	                           nameEn = "China",
	                           code   = "CH",
	                           type   = LocalisationType.CU)
	lRequestLoc.request_creation(account.user, "Not exist")
	lRequest = LocalisationEventCreationRequest.objects.filter()[0]
	lRequest.refuse(account)

	return True
