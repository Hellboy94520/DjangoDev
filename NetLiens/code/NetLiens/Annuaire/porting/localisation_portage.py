import logging
from ..models.localisation import Type, create_localisation, add_children, Localisation
from ..models.communs import Status
from ..models.account import AccountAdmin
from django.db.models import Q


""" --------------------------------------------------------------------------------------------------------------------
------------------------------------------------------------------------------------------------------------------------
Data
------------------------------------------------------------------------------------------------------------------------
-------------------------------------------------------------------------------------------------------------------- """
logger = logging.getLogger(__name__)

lDir = '/Users/hellboy/Cozy Drive/dev/DjangoDev/NetLiens/doc/InseeSQL2017/'

Continent = ["Europe,Europe,991",
             "Asie,Asia,992",
             "Afrique,Africa,993",
             "Amérique,America,994",
             "Océanie,Oceania,995"]


""" --------------------------------------------------------------------------------------------------------------------
------------------------------------------------------------------------------------------------------------------------
Functions
------------------------------------------------------------------------------------------------------------------------
-------------------------------------------------------------------------------------------------------------------- """
# Low all caracters after a letter and delete the part with '('
def lower_libcog(pString: str):
	if   pString == "GRECE":      return "Grèce"
	elif pString == "MACEDOINE":  return "Macédoine"
	elif pString == "NORVEGE":    return "Norvège"
	elif pString == "SUEDE":      return "Suède"
	elif pString == "YEMEN (REPUBLIQUE ARABE DU)": return "Yémen"
	elif pString == "THAILANDE":  return "Thaïlande"
	elif pString == "NEPAL":      return "Népal"
	elif pString == "BIRMANIE":   return "Birmanie"
	elif pString == "KOWEIT":     return "Koweït"
	elif pString == "ISRAEL":     return "Israël"
	elif pString == "INDONESIE":  return "Indonésie"
	elif pString == "COREE":      return "Corée"
	elif pString == "ARMENIE":    return "Arménie"
	elif pString == "BRESIL":     return "Brésil"
	elif pString == "GUATEMALA":  return "Guatémala"
	elif pString == "PEROU":      return "Pérou"
	elif pString == "VENEZUELA":  return "Vénézuéla"
	elif pString == "ALGERIE":    return "Algérie"
	elif pString == "BENIN":      return "Bénin"
	elif pString == "GUINEE":     return "Guinée"
	elif pString == "SENEGAL":    return "Sénégal"
	elif pString == "NOUVELLE-ZELANDE":       return "Nouvelle-Zélande"
	elif pString == "BIELORUSSIE":  return "Biélorussie"
	elif pString == "BOSNIE-HERZEGOVINE":     return "Bosnie-Herzégovine"
	elif pString == "FEROE (ILES)": return "Féroé (Îles)"
	elif pString == "IRLANDE, ou EIRE":       return "Irlande"
	elif pString == "VIET NAM":   return "Viêt Nam"
	elif pString == "ETATS-UNIS": return "États-Unis"
	elif pString == "BURKINA":    return "Burkina Faso"
	elif pString == "POLYNESIE FRANCAISE":    return "Polynésie Française"
	elif pString == "NOUVELLE-CALEDONIE":     return "Nouvelle-Calédonie"

	lString = pString[0]
	for i in range(1, len(pString)):
		# If Previous caracter was a letter
		if 65 <= ord(pString[i-1]) <= 90 : lString += pString[i].lower()
		# If ( caracter, stop the conversion and delete all after (include space)
		elif pString[i] == "(":
			if   pString[i:] == "(ILE)":
				lString += "(Île)"
				return lString
			elif pString[i:] == "(ILES)":
				lString += "(Île)"
				return lString
			elif pString[i:] == "(REPUBLIQUE)":
				lString += "(République)"
				return lString
			elif pString[i:] == "(REPUBLIQUE DEMOCRATIQUE)":
				lString += "(République démocratique du)"
				return lString
			return lString[:-1]
		else: lString += pString[i]
	return lString


# Return Continent localisation associated to COG
def get_continent_parent(pCode: str):
	lResult = None
	# Only the three first numbers are usefull
	if   pCode[:3] == "991": lResult = Localisation.objects.filter(nameFr='Europe'  , type=Type.CO)
	elif pCode[:3] == "992": lResult = Localisation.objects.filter(nameFr='Asie'    , type=Type.CO)
	elif pCode[:3] == "993": lResult = Localisation.objects.filter(nameFr='Afrique' , type=Type.CO)
	elif pCode[:3] == "994": lResult = Localisation.objects.filter(nameFr='Amérique', type=Type.CO)
	elif pCode[:3] == "995": lResult = Localisation.objects.filter(nameFr='Océanie' , type=Type.CO)

	if lResult is not None and len(lResult) == 1:
		return lResult[0]
	return None


def create_localisation_models(pAdmin: AccountAdmin):

	logger.debug("[Localisation] Conversion starting...")

	" Continents ------------------------------------------------------------------------------------------------------- "
	lNum = 0
	for lvalue in Continent:
		lSplit = lvalue.split(",")
		create_localisation(lSplit[0], lSplit[1], lSplit[2], Type.CO, Status.AC, pAdmin)
		lNum += 1

	logger.debug("[Localisation] {} Continents has been created".format(lNum))

	" Countries -------------------------------------------------------------------------------------------------------- "
	try:
		lFile = open(lDir+'pays2017.txt')
	except FileNotFoundError:
		logger.error("Impossible to open {}".format(lFile.name))
	else:
		# Separate the file in line (without keeping the first one)
		Lines = lFile.read().split("\n")[1:]
		lNum = 0

		# Separate each line in words
		for i, line in enumerate(Lines):
			words = line.split("\t")
			# Checking the words quantity by line
			if len(words) != 11:
				logger.error("[Localisation] Incorrect word size in Insee file {}".format(lFile.name))
				return False
				# Checking
			elif words[0] != "XXXXX":
				lCountry = create_localisation(lower_libcog(words[5]), "", words[9], Type.CU,
				                               Status.AC, pAdmin)
				# Add country to a continent
				lParent = get_continent_parent(words[0])
				if lParent is not None: add_children(lParent, lCountry, pAdmin)
				else: logger.error("[Localisation] Impossible to find the parent country with code COG \'{}\'".format(words[0]))
				lNum += 1

		logger.debug("[Localisation] {} countries has been created".format(lNum))

	" RegionFR --------------------------------------------------------------------------------------------------------- "
	try:
		lFile = open(lDir+'reg2017.txt')
	except FileNotFoundError:
		logger.error("Impossible to open {}".format(lFile.name))
	else:
		# Separate the file in line (without keeping the first one)
		Lines = lFile.read().split("\n")[1:]
		lNum = 0

		# Separate each line in words
		for i, line in enumerate(Lines):
			words = line.split("\t")
			# Checking the words quantity by line
			if len(words) != 5:
				logger.error("[Localisation] Incorrect word size in Insee file {}".format(lFile.name))
				return False
			else:
				lRegion = create_localisation(words[4], "", words[0], Type.RE, Status.AC, pAdmin)
				lParent = Localisation.objects.filter(nameFr="France", type=Type.CU)
				if len(lParent) == 1: add_children(lParent[0], lRegion, pAdmin)
				else: logger.error("[Localisation] Impossible to find France country")
				lNum += 1

		logger.debug("[Localisation] {} regionfr has been created".format(lNum))

	" DepartementFR ---------------------------------------------------------------------------------------------------- "
	try:
		lFile = open(lDir+'depts2017.txt')
	except FileNotFoundError:
		logger.error("Impossible to open {}".format(lFile.name))
	else:
		# On sépares chaque ligne en supprimant la première :
		Lines = lFile.read().split("\n")[1:]
		lNum = 0

		# Pour chaque ligne séparée, on sépare les mots
		for i, line in enumerate(Lines):
			words = line.split("\t")
			# On vérifie qu'il en a bien 7
			if len(words) != 6:
				logger.error("[Localisation] Incorrect word size in Insee file {}".format(lFile.name))
				return False
			else:
				lDepartement = create_localisation(words[5], "", words[1], Type.DE, Status.AC, pAdmin)
				lParent = Localisation.objects.filter(code=words[0], type=Type.RE)
				if len(lParent) == 1: add_children(lParent[0], lDepartement, pAdmin)
				else: logger.error("[Localisation] Impossible to find the region with code {}".format(words[0]))
				lNum += 1

		logger.debug("[Localisation] {} regionfr has been created".format(lNum))

	"""
	" CityFR ----------------------------------------------------------------------------------------------------------- "
	try:
		lFile = open(lDir+'city2017.txt')
	except FileNotFoundError:
		logger.error("Impossible to open {}".format(lFile.name))
	else:
		# On sépares chaque ligne en supprimant la première :
		Lines = lFile.read().split("\n")[1:]
		lNum = 0

		# Pour chaque ligne séparée, on sépare les mots
		for i, line in enumerate(Lines):
			words = line.split("\t")
			# On vérifie qu'il en a bien 12
			if len(words) != 12:
				logger.error("[Localisation] Incorrect word size in Insee file {}".format(lFile.name))
				return False
			else:
				lCity = create_localisation(words[11], words[11], words[3]+words[4], Type.CI, Status.AC, pAdmin)
				lParent = Localisation.objects.filter(code=words[3], type=Type.DE)
				if len(lParent) == 1: add_children(lParent[0], lCity, pAdmin)
				else: logger.error("[Localisation] Impossible to find the department with code {}".format(words[3]))
				lNum += 1

		logger.debug("[Localisation] {} cityfr has been created".format(lNum))
	"""

	return True

def create_localisation_association(pSqlCursor, pAdmin: AccountAdmin):

	logger.debug("[Localisation] SQL Conversion starting...")
	pSqlCursor.execute("SELECT * FROM annu_dept")
	lSqlDept = pSqlCursor.fetchall()
	for (sId, sNom, sRegion, sIdZone) in lSqlDept:

		lLoc = None

		# Case for continent
		if    202 <= sId <= 208 or sId == 211 or sId == 523:
			lExpectedName = ""
			if   sId == 202: lExpectedName = "Europe"     # Europe
			elif sId == 203: lExpectedName = "Amérique"   # Amérique du Nord
			elif sId == 204: lExpectedName = "Amérique"   # Amérique centrale-Sud
			elif sId == 205: lExpectedName = "Afrique"    # Afrique du Nord
			elif sId == 206: lExpectedName = "Afrique"    # Afrique Centrale-Australe
			elif sId == 207: lExpectedName = "Asie"       # Moyen Orient-Asie
			elif sId == 208: lExpectedName = "Océanie"    # Océanie-Australie
			elif sId == 211: lExpectedName = "Océanie"    # Océan Indien
			elif sId == 523: lExpectedName = "Afrique"    # Afrique du Sud

			lLoc = Localisation.objects.filter(nameFr=lExpectedName, type=Type.CO)
			if len(lLoc) != 1:
				logger.error("[Localisation] Impossible to find \'{}\' continent".format(lExpectedName))
				return False

		# Other special case
		elif  sId == 209:
			# TODO:
			pass
		elif  sId == 210:
			# TODO:
		  pass
		# DOM TOM
		elif  sId == 325:
			# TODO:
		  pass
		# ???
		elif  sId == 503 or sId == 522 or sId == 566 or sId == 567 or sId == 573 or sId == 575 or sId == 598 or sId == 599:
			# TODO:
		  pass
		# Antille-Guyane, Réunion
		elif sId == 973 or sId == 974:
			if    sId == 973: lExpectedName = "Guyane"
			elif  sId == 974: lExpectedName = "La Réunion"
			lLoc = Localisation.objects.filter(nameFr=lExpectedName, type=Type.RE)
			if len(lLoc) != 1:
				logger.error("[Localisation] Impossible to find \'{}\' region".format(lExpectedName))
				return False
		# Polynésie Françaises
		elif sId == 998 or sId == 999:
			if   sId == 998:  lExpectedName = "Polynésie Française"
			elif sId == 999:  lExpectedName = "Nouvelle-Calédonie"
			lLoc = Localisation.objects.filter(nameFr=lExpectedName, type=Type.CU)
			if len(lLoc) != 1:
				logger.error("[Localisation] Impossible to find \'{}\' country".format(lExpectedName))
				return False
		# Unknown
		elif  sId == 9999:
			# TODO:
		 pass


		# Commun case
		else:
			# Searching the information type
			lType = Type.UN
			if   sIdZone == 0:  lType = Type.RE  # French Region
			elif sIdZone == 1:  lType = Type.DE  # Department
			elif sIdZone == 2:  lType = Type.CU  # Europe
			elif sIdZone == 3:  lType = Type.CU  # North America
			elif sIdZone == 4:  lType = Type.CU  # South America
			elif sIdZone == 5:  lType = Type.CU  # North Africa
			elif sIdZone == 6:  lType = Type.CU  # South Africa
			elif sIdZone == 7:  lType = Type.CU  # Asia
			elif sIdZone == 8:  lType = Type.CU  # Oceania
			elif sIdZone == 11: lType = Type.CU  # Oceania

			if lType == Type.UN:
				logger.error("[Localisation] Impossible to find the type of an annu_dept with id_zone=\'{}\'".format(sIdZone))
				return False

			# Specials cases:
			lExpectedName = sNom
			if   sNom == "Alpes de Hautes-Provence": lExpectedName = "Alpes-de-Haute-Provence"  # Spelling error
			elif sNom == "Corse" and sIdZone==1:                                                # Two Department in one
				lType = Type.DE
				lExpectedName = "Haute-Corse"
			elif sNom == "Côtes d'Armor": lExpectedName = "Côtes-d'Armor"                       # Spelling error
			elif sNom == "Territoire-de-Belfort": lExpectedName = "Territoire de Belfort"       # Spelling error
			elif sNom == "Nord Pas de Calais" or sNom == "Picardie":                            # Modification in 2017
				lExpectedName = "Hauts-de-France"
			elif sNom == "Basse Normandie" or sNom == "Haute Normandie":                        # Modification in 2017
				lExpectedName = "Normandie"
			elif sNom == "Ile De France": lExpectedName = "Île-de-France"                       # Spelling error
			elif sNom == "Centre": lExpectedName = "Centre-Val de Loire"                        # Modification in 2017
			elif sNom == "Alsace" or sNom == "Champagne Ardenne" or sNom == "Lorraine":         # Modification in 2017
				lExpectedName = "Grand Est"
			elif sNom == "Bourgogne" or sNom == "Franche Comté":                                # Modification in 2017
				lExpectedName = "Bourgogne-Franche-Comté"
			elif sNom == "Aquitaine" or sNom == "Poitou Charentes" or sNom == "Limousin":       # Modification in 2017
				lExpectedName = "Nouvelle-Aquitaine"
			elif sNom == "Auvergne" or sNom == "Rhônes Alpes":                                  # Modification in 2017
				lExpectedName = "Auvergne-Rhône-Alpes"
			elif sNom == "PACA": lExpectedName = "Provence-Alpes-Côte d'Azur"                   # Spelling error
			elif sNom == "Midi Pyrénées" or sNom == "Languedoc Rousillon":                      # Modification in 2017
				lExpectedName = "Occitanie"
			elif sNom == "Macédoine": lExpectedName = "Ex-Republique Yougoslave De Macedoine"   # Spelling error
			elif sNom == "Vietnam": lExpectedName = "Viêt Nam"                                  # Spelling error
			elif sNom == "Tibet"  : lExpectedName = "Chine"                                     # Tibet is not a country
			elif sNom == "Myanmar (Birmanie)": lExpectedName = "Birmanie"                       # Spelling error
			elif sNom == "Irak": lExpectedName = "Iraq"                                         # Spelling error
			elif sNom == "Hong Kong": lExpectedName = "Hong-Kong"                               # Spelling error
			elif sNom == "Etats unis": lExpectedName = "États-Unis"                             # Spelling error
			elif sNom == "Canada &amp; Quebec": lExpectedName = "Canada"                        # Spelling error
			elif sNom == "Cap Vert": lExpectedName = "Cap-Vert"                                 # Spelling error
			elif sNom == "Centrafrique": lExpectedName = "Centrafricaine (République)"          # Spelling error
			elif sNom == "Cote d'Ivoire": lExpectedName = "Cote D'Ivoire"                       # Spelling error
			elif sNom == "Sahara occidental": lExpectedName = "Sahara Occidental"               # Spelling error
			elif sNom == "Nouvelle Zelande": lExpectedName = "Nouvelle-Zélande"                 # Spelling error
			elif sNom == "Ile Maurice": lExpectedName = "Maurice"                               # Spelling error
			elif sNom == "Boznie Herzégovine": lExpectedName = "Bosnie-Herzégovine"             # Spelling error
			elif sNom == "Iles Féroé": lExpectedName = "Féroé (Îles)"                           # Spelling error
			elif sNom == "Letonie": lExpectedName = "Lettonie"                                  # Spelling error
			elif sNom == "Saint Marin": lExpectedName = "Saint-Marin"                           # Spelling error
			elif sNom == "Yougoslavie": lExpectedName = "Ex-Republique Yougoslave De Macedoine" # Spelling error
			elif sNom == "Antilles (hors DOM-TOM)": lExpectedName = "Territoires Du Royaume-Uni Aux Antilles" # Spelling error

			lLoc = Localisation.objects.filter(nameFr=lExpectedName, type=lType)
			if len(lLoc) != 1:
				logger.error("[Localisation] Impossible to find localisation with name \'{}\'".format(lExpectedName))
				return False

		# TODO: Modification d'un QuerySet impossible car copy de l'object
		if lLoc is not None:
			if lLoc[0].nameEn == "":
				lLoc[0].nameEn = str(sId)
				lLoc[0].save()
			else:
				lLoc[0].nameEn += ",{}".format(str(sId))
				lLoc[0].save()

	logger.debug("[Localisation] SQL Conversion done")


# TODO: Modification d'un QuerySet impossible car copy de l'object
def reset_localisation_useless_data():
	# Reset resumeEn and put correct data in Continent
	for i, lLoc in enumerate(Localisation.objects.filter(type=Type.CO)):
		lSplit = Continent[i].split(",")
		lLoc.nameEn = lSplit[1]
		lLoc.save()

	for lLoc in Localisation.objects.filter(Q(type=Type.RE) |  Q(type=Type.DE)):
		lLoc.nameEn = lLoc.nameFr
		lLoc.save()

	for lLoc in Localisation.objects.filter(type=Type.CU):
		lLoc.nameEn = ""
		lLoc.save()
