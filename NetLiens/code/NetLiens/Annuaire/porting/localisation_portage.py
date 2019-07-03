import logging
from ..models.localisation import Localisation, LocalisationType
from ..models.account import AccountAdmin, User

# sudo pip3 install opencv
import csv

import re

logger = logging.getLogger(__name__)

""" --------------------------------------------------------------------------------------------------------------------
Data
-------------------------------------------------------------------------------------------------------------------- """
_equivLoc = {}


""" --------------------------------------------------------------------------------------------------------------------
Localisation
-------------------------------------------------------------------------------------------------------------------- """
def open_file(name: str):
	try:
		lFile = open(name)
	except FileNotFoundError:
		logger.fatal("Impossible to open file {}".format(name))
		return False
	return lFile


""" ---------------------------------------------------------------------------------------------------------------- """
def lower_libcog(name: str):
	# Delete useless space
	lName = re.sub(' +', ' ', name)
	# Lower all letter
	lName = lName.lower()
	# Upper first letter of each word
	lNameSplit = re.split(' ', lName)
	lName = ""
	for name in lNameSplit:
		lName += name[0].upper()
		lName += name[1:]
		lName += " "
	# Remove last useless space
	lName = lName[:-1]
	return lName


""" ---------------------------------------------------------------------------------------------------------------- """
def load_data(settings):
	dir      = settings.get('INSEE', 'dir')
	country  = settings.get('INSEE', 'country')  + settings.get('INSEE', 'ext')
	regionFr = settings.get('INSEE', 'regionFr') + settings.get('INSEE', 'ext')
	departFr = settings.get('INSEE', 'departFr') + settings.get('INSEE', 'ext')
	citiesFr = settings.get('INSEE', 'citiesFr') + settings.get('INSEE', 'ext')
	associat = settings.get('INSEE', 'associat') + settings.get('INSEE', 'ext')
	return dir, country, regionFr, departFr, citiesFr, associat


""" ---------------------------------------------------------------------------------------------------------------- """
def create_localisation_models(settings, admin: AccountAdmin, sqlcursor):
	""" Load data ----------------------------------------- """
	lDir, lCountryFileName, lRegionFrFileName, lDepartFrFileName, lCitiesFrFileName, lAssoc = load_data(settings)

	""" Open files ---------------------------------------- """
	lCountryFile = open_file(lDir+lCountryFileName)
	if lCountryFile is False:  return False
	lRegionFrFile = open_file(lDir+lRegionFrFileName)
	if lRegionFrFile is False: return False
	lDepartFrFile = open_file(lDir+lDepartFrFileName)
	if lDepartFrFile is False: return False
	lCitiesFrFile = open_file(lDir+lCitiesFrFileName)
	if lCitiesFrFile is False: return False
	lAssocFile = open_file(lDir+lAssoc)
	if lAssocFile is False: return False

	""" Unknown ------------------------------------------- """
	lUnknow   = Localisation(nameFr = "Inconnue",
		                       nameEn = "Unknown",
		                       type = LocalisationType.UN)
	lUnknow.create(admin)

	""" Continents ---------------------------------------- """
	lEurope   = Localisation(nameFr = "Europe",
		                       nameEn = "Europe",
		                       code = 991,
		                       type = LocalisationType.CO)
	lEurope.create(admin)
	lAsia     = Localisation(nameFr = "Asie",
		                       nameEn = "Asia",
		                       code = 992,
		                       type = LocalisationType.CO)
	lAsia.create(admin)
	lAfrica   = Localisation(nameFr = "Afrique",
		                       nameEn = "Africa" ,
		                       code = 993,
		                       type = LocalisationType.CO)
	lAfrica.create(admin)
	lAmerica  = Localisation(nameFr = "Amérique",
		                       nameEn = "America" ,
		                       code = 994,
		                       type = LocalisationType.CO)
	lAmerica.create(admin)
	lOceania  = Localisation(nameFr = "Océanie",
		                       nameEn = "Oceania" ,
		                       code = 995,
		                       type = LocalisationType.CO)
	lOceania.create(admin)

	""" Country ------------------------------------------- """
	# Open file with cvs
	# TODO: Voir pour l'option "actual" dans le fichier des pays
	lParthCountry = csv.DictReader(lCountryFile)
	# Get all country
	for lParam in lParthCountry:
		if    (lParam.get("cog") != "XXXXX" and lParam.get("actual") == "1") \
			or lParam.get("libcog")=="FRANCE":
			lCountry = Localisation(nameFr  = lower_libcog(lParam.get("libcog")),
			                        code    = lParam.get("codeiso3"),
			                        type    = LocalisationType.CU,
			                        display = True)
			lCountry.create(admin)
			# Search the parent
			if   lParam.get("cog")[:3] == "991": lCountry.set_parent(Localisation.objects.get(nameFr='Europe',
			                                                                                  type=LocalisationType.CO), admin)
			elif lParam.get("cog")[:3] == "992": lCountry.set_parent(Localisation.objects.get(nameFr='Asie',
			                                                                                  type=LocalisationType.CO), admin)
			elif lParam.get("cog")[:3] == "993": lCountry.set_parent(Localisation.objects.get(nameFr='Afrique',
			                                                                                  type=LocalisationType.CO), admin)
			elif lParam.get("cog")[:3] == "994": lCountry.set_parent(Localisation.objects.get(nameFr='Amérique',
			                                                                                  type=LocalisationType.CO), admin)
			elif lParam.get("cog")[:3] == "995": lCountry.set_parent(Localisation.objects.get(nameFr='Océanie',
			                                                                                  type=LocalisationType.CO), admin)

		elif lParam.get("cog") == "XXXXX" and (lParam.get("libcog") == "POLYNESIE FRANCAISE"          or
		                                       lParam.get("libcog") == "NOUVELLE-CALEDONIE"           or
																					 lParam.get("libcog") == "SAINT-PIERRE-ET-MIQUELON"     or
																					 lParam.get("libcog") == "TERRES AUSTRALES FRANCAISES"  or
																					 lParam.get("libcog") == "WALLIS-ET-FUTUNA"             or
																					 lParam.get("libcog") == "CLIPPERTON (ILE)"             or
																					 lParam.get("libcog") == "SAINT-BARTHELEMY"             or
																					 lParam.get("libcog") == "SAINT-MARTIN"
		):
			lTerritory = Localisation(nameFr  = lower_libcog(lParam.get("libcog")),
			                          code    = lParam.get("codeiso3"),
			                          type    = LocalisationType.TE,
			                          display = True)
			lTerritory.create(admin)
			lFrance = Localisation.objects.get(nameFr="France", type=LocalisationType.CU)
			lTerritory.set_parent(lFrance, admin)
	lCountryFile.close()

	""" RegionFR ------------------------------------------ """
	# Open file with cvs
	lPathRegionFr = csv.DictReader(lRegionFrFile)
	# Get all region
	for lParam in lPathRegionFr:
		lRegion = Localisation(nameFr = lParam.get("nccenr"),
		                       nameEn = lParam.get("nccenr"),
		                       code   = lParam.get("reg"),
		                       type   = LocalisationType.RE)
		lRegion.create(admin)
		lFrance = Localisation.objects.get(nameFr="France", type=LocalisationType.CU)
		lRegion.set_parent(lFrance, admin)
	lRegionFrFile.close()

	""" DepartmentFr -------------------------------------- """
	# Open file with cvs
	lPathDepartFr = csv.DictReader(lDepartFrFile)
	# Get all department
	for lParam in lPathDepartFr:
		lDepart = Localisation(nameFr = lParam.get("nccenr"),
		                       nameEn = lParam.get("nccenr"),
		                       code   = lParam.get("dep"),
		                       type   = LocalisationType.DE)
		lDepart.create(admin)
		# Get the parent
		lRegion = Localisation.objects.get(code=lParam.get("reg"),
		                                   type=LocalisationType.RE)
		lDepart.set_parent(lRegion, admin)
	lDepartFrFile.close()

	""" CitiesFr ------------------------------------------ """
	# # Open file with cvs
	# lPathCitiesFr = csv.DictReader(lCitiesFrFile)
	# # Get all city
	# for lParam in lPathCitiesFr:
	# 	if lParam.get("typecom") == "COM":
	# 		lCities = Localisation(nameFr = lParam.get("nccenr"),
	# 		                       nameEn = lParam.get("nccenr"),
	# 		                       code   = lParam.get("com"),
	# 		                       type   = LocalisationType.CI)
	# 		lCities.create(admin)
	# 		# Get the parent
	# 		lDepart = Localisation.objects.get(code=lParam.get("dep"),
	# 		                                   type=LocalisationType.DE)
	# 		lCities.set_parent(lDepart, admin)
	lCitiesFrFile.close()

	""" Association --------------------------------------- """

	# Get all annu_dept from old sql database
	sqlcursor.execute("SELECT * FROM annu_dept")
	lSqlDept = sqlcursor.fetchall()

	# Associated each annu_dept in a localisation
	# TODO: No case: 209, 210, 325, 503, 522, 566, 567, 573, 575, 598, 599
	for (sId, sNom, sRegion, sIdZone) in lSqlDept:
		# Departement
		if    1 < sId < 95 or sId == 973 or sId == 974:
			# Particular case for Corse
			if sId == 20:
				_equivLoc[sId] = Localisation.objects.get(type=LocalisationType.DE, code="2A")
			else:
				_equivLoc[sId] = Localisation.objects.get(type=LocalisationType.DE, code="{:02d}".format(sId))
		# Continent
		elif  202 < sId < 208 or sId == 211:
			lCode = ""
			if   sId == 202:                lCode = "991"  # Europe
			elif sId == 203 or sId == 204:  lCode = "994"  # America
			elif sId == 205 or sId == 206:  lCode = "993"  # Africa
			elif sId == 207 :               lCode = "992"  # Asie
			elif sId == 208 or sId == 211:  lCode = "995"  # Oceania
			_equivLoc[sId] = Localisation.objects.get(type=LocalisationType.CO, code=lCode)

		# Country
		elif sId == 201 or 401 < sId < 572 or sId == 576 or 600 < sId < 621:
			lCode = ""
			if   sId == 201 or 401: lCode = "FRA"
			elif sId == 402       : lCode = "DEU"
			elif sId == 403       : lCode = "AUT"
			elif sId == 404       : lCode = "BEL"
			elif sId == 405       : lCode = "CYP"
			elif sId == 406       : lCode = "DNK"
			elif sId == 407       : lCode = "ESP"
			elif sId == 408       : lCode = "FIN"
			elif sId == 410       : lCode = "GRC"
			elif sId == 411       : lCode = "HUN"
			elif sId == 412       : lCode = "IRL"
			elif sId == 413       : lCode = "ISL"
			elif sId == 414       : lCode = "ITA"
			elif sId == 415       : lCode = "LUX"
			elif sId == 416       : lCode = "MKD"
			elif sId == 417       : lCode = "MLT"
			elif sId == 418       : lCode = "MCO"
			elif sId == 419       : lCode = "NOR"
			elif sId == 420       : lCode = "NLD"
			elif sId == 421       : lCode = "POL"
			elif sId == 422       : lCode = "PRT"
			elif sId == 423       : lCode = "ROU"
			elif sId == 424       : lCode = "GBR"
			elif sId == 425       : lCode = "SWE"
			elif sId == 426       : lCode = "CHE"
			elif sId == 427       : lCode = "UKR"
			elif sId == 463       : lCode = "YEM"
			elif sId == 464       : lCode = "VNM"
			elif sId == 465       : lCode = "TUR"
			elif sId == 466       : lCode = ""    # Tibet
			elif sId == 467       : lCode = "THA"
			elif sId == 468       : lCode = "TWN"
			elif sId == 469       : lCode = ""    # Sirie
			elif sId == 470       : lCode = "LKA"
			elif sId == 471       : lCode = "SGP"
			elif sId == 472       : lCode = "PHL"
			elif sId == 473       : lCode = "PSE"
			elif sId == 474       : lCode = "PAK"
			elif sId == 475       : lCode = "NPL"
			elif sId == 476       : lCode = "MMR"
			elif sId == 477       : lCode = "MNG"
			elif sId == 478       : lCode = "MDV"
			elif sId == 479       : lCode = "MYS"
			elif sId == 480       : lCode = "LBN"
			elif sId == 481       : lCode = "LAO"
			elif sId == 482       : lCode = "KWT"
			elif sId == 483       : lCode = "JOR"
			elif sId == 484       : lCode = "JPN"
			elif sId == 485       : lCode = "ISR"
			elif sId == 486       : lCode = "IRN"
			elif sId == 487       : lCode = "IRQ"
			elif sId == 488       : lCode = "IDN"
			elif sId == 489       : lCode = "IND"
			elif sId == 490       : lCode = ""    # Hong Kong
			elif sId == 491       : lCode = "ARE"
			elif sId == 492       : lCode = "KOR"   # Corée
			elif sId == 493       : lCode = "CHN"
			elif sId == 494       : lCode = "KHM"
			elif sId == 495       : lCode = "BTN"
			elif sId == 496       : lCode = "BGD"
			elif sId == 497       : lCode = "ARM"
			elif sId == 498       : lCode = "SAU"
			elif sId == 499       : lCode = "AFG"
			elif sId == 500       : lCode = "USA"
			elif sId == 501       : lCode = "CAN"
			elif sId == 502       : lCode = "MEX"
			elif sId == 503       : lCode = ""    # UNKNOWN
			elif sId == 504       : lCode = "ARG"
			elif sId == 505       : lCode = "CRI"
			elif sId == 506       : lCode = "BOL"
			elif sId == 507       : lCode = "BLZ"
			elif sId == 508       : lCode = "BRA"
			elif sId == 509       : lCode = "CHL"
			elif sId == 510       : lCode = "COL"
			elif sId == 511       : lCode = "ECU"
			elif sId == 512       : lCode = "GTM"
			elif sId == 513       : lCode = "GUY"
			elif sId == 514       : lCode = "HND"
			elif sId == 515       : lCode = "NIC"
			elif sId == 516       : lCode = "PAN"
			elif sId == 517       : lCode = "PRY"
			elif sId == 518       : lCode = "PER"
			elif sId == 519       : lCode = "PRI"
			elif sId == 520       : lCode = "URY"
			elif sId == 521       : lCode = "VEN"
			elif sId == 522       : lCode = ""    # UNKNOWN
			elif sId == 523       : lCode = "ZAF"
			elif sId == 524       : lCode = "DZA"
			elif sId == 525       : lCode = "AGO"
			elif sId == 526       : lCode = "BEN"
			elif sId == 527       : lCode = "BFA"
			elif sId == 528       : lCode = "CMR"
			elif sId == 529       : lCode = "CPV"
			elif sId == 530       : lCode = "CAF"
			elif sId == 531       : lCode = "COM"
			elif sId == 532       : lCode = "COD"
			elif sId == 533       : lCode = "CIV"
			elif sId == 534       : lCode = "DJI"
			elif sId == 535       : lCode = "EGY"
			elif sId == 536       : lCode = "ETH"
			elif sId == 537       : lCode = "GAB"
			elif sId == 538       : lCode = "GMB"
			elif sId == 539       : lCode = "GHA"
			elif sId == 540       : lCode = "GIN"
			elif sId == 541       : lCode = "KEN"
			elif sId == 542       : lCode = "LBR"
			elif sId == 543       : lCode = "LBY"
			elif sId == 544       : lCode = "MDG"
			elif sId == 545       : lCode = "MLI"
			elif sId == 546       : lCode = "MAR"
			elif sId == 547       : lCode = "MRT"
			elif sId == 548       : lCode = "MOZ"
			elif sId == 549       : lCode = "NAM"
			elif sId == 550       : lCode = "NER"
			elif sId == 551       : lCode = "NGA"
			elif sId == 552       : lCode = "UGA"
			elif sId == 553       : lCode = "RWA"
			elif sId == 554       : lCode = "ESH"   # CODE = 4 !!!
			elif sId == 555       : lCode = "SEN"
			elif sId == 556       : lCode = "SYC"
			elif sId == 557       : lCode = "SLE"
			elif sId == 558       : lCode = "SOM"
			elif sId == 559       : lCode = "SDN"
			elif sId == 560       : lCode = "TZA"
			elif sId == 561       : lCode = "TCD"
			elif sId == 562       : lCode = "TGO"
			elif sId == 563       : lCode = "TUN"
			elif sId == 564       : lCode = "ZMB"
			elif sId == 565       : lCode = "ZWE"
			elif sId == 566       : lCode = ""  # UNKNOWN
			elif sId == 567       : lCode = ""  # UNKNOWN
			elif sId == 570       : lCode = "AUS"
			elif sId == 571       : lCode = "NZL"
			elif sId == 572       : lCode = "FJI"
			elif sId == 573       : lCode = ""  # UNKNOWN
			elif sId == 575       : lCode = ""  # UNKNOWN
			elif sId == 576       : lCode = "MUS"
			elif sId == 598       : lCode = ""  # UNKNOWN
			elif sId == 599       : lCode = ""  # UNKNOWN
			elif sId == 600       : lCode = "ALB"
			elif sId == 601       : lCode = "AND"
			elif sId == 603       : lCode = "BLR"
			elif sId == 604       : lCode = "BIH"
			elif sId == 605       : lCode = "BGR"
			elif sId == 606       : lCode = "HRV"
			elif sId == 607       : lCode = "EST"
			elif sId == 608       : lCode = "FRO"   # CODE + 3 !!!
			elif sId == 609       : lCode = "GIB"
			elif sId == 610       : lCode = "GGY"
			elif sId == 611       : lCode = "LVA"
			elif sId == 612       : lCode = "LIE"
			elif sId == 613       : lCode = "LTU"
			elif sId == 614       : lCode = "MDA"
			elif sId == 615       : lCode = "UKR"  # TCHECOSLOVAQUIE
			elif sId == 616       : lCode = "RUS"
			elif sId == 617       : lCode = "SXM"
			elif sId == 618       : lCode = "SVK"
			elif sId == 619       : lCode = "SVN"
			elif sId == 620       : lCode = "MKD"
			elif sId == 621       : lCode = ""    # ANTILLE-NEERLANDAISES

			if lCode:
				_equivLoc[sId] = Localisation.objects.get(type=LocalisationType.CU, code=lCode)

		# Territory
		elif sId == 998 or sId == 999:
			if sId == 998:
				_equivLoc[sId] = Localisation.objects.get(type=LocalisationType.TE, code="PYF")
			if sId == 999:
				_equivLoc[sId] = Localisation.objects.get(type=LocalisationType.TE, code="NCL")
		elif sId == 9999:
			_equivLoc[sId] = Localisation.objects.get(type=LocalisationType.UN)

		if _equivLoc.get(sId, None) is None:
			print("LOCALISATION ERROR: Impossible to find association with id={}".format(sId))

#
#
# def reset_localisation_useless_data():
# 	for lLoc in Localisation.objects.all():
# 		lLoc.sqlId = -1
# 		lLoc.save()
#
