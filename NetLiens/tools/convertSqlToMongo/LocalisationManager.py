from NetLiensData.Category import *
from Log import *
from tools.Network import isMongoDBClient, isSqlClient
from tools.File import *
from NetLiensData.Localisation import *
from NetLiensData.Statistique import StatistiqueData

className = "LocalisationManager"

""" ********************************************************************************************************************
   Fonction de création des continents depuis les deux dictionnaires présent dans Localisation.py
******************************************************************************************************************** """
def createContinentFromDictionnary(MongoTable, MongoTableStat):

  Log.info("BEGIN : Creation of CountinentData...")

  for name, code in ContinentFrCodeData.items():
    # Enregistrement des données
    lContinent = ContinentData()
    lContinent.id     = code
    lContinent.nameFr = name
    lContinent.nameEn = ContinentNameFrToUs.get(name, None)
    # Vérification des concordances entre les deux dictionnaires
    if lContinent.nameEn is None:
      Log.fatal(className, "Dictionnairy with name and code are not the same")
      return False

    # Enregistrement dans la base de donnée de l'objet
    MongoTable.insert_one(lContinent.toTable())
    MongoTableStat.insert_one(StatistiqueData(lContinent.id).toTable())

  Log.info("END : {} continents has been created".format(MongoTable.find().count()))
  return True


""" ********************************************************************************************************************
   Fonction de création des pays 
******************************************************************************************************************** """
def createCountryFromInseeFile(MongoTable, MongoTableStat, pFile):

  Log.info("BEGIN : Creation of CountryData...")

  lFile = openFile(pFile)
  if lFile is False:
    return False

  Lines = lFile.read().split("\n")
  # On ne garde pas la première ligne
  Lines = Lines[1:]
  # On récupère chaque ligne du fichier
  for i, line in enumerate(Lines):
    # Que l'on sépare
    Words = line.split("\t")
    # On vérifie que l'on a bien le bon nombre de paramètres
    if len(Words) != 11:
      Log.error(className, "{} has incorrect syntax to be used at line {}".format(pFile, i))
    else:
      # Enregistrement de la donnée si le résultat de la conversion est correcte
      lCountryData = CountryData()
      result = lCountryData.fromInsee(Words)
      if result is not True:
        Log.warning(className, "Information is incorrect : {}".format(result))
      else:
        MongoTable.insert_one(lCountryData.toTable())
        MongoTableStat.insert_one(StatistiqueData(lCountryData.id).toTable())

  Log.info("END : {} countries has been created".format(MongoTable.find().count()))
  return True


""" ********************************************************************************************************************
   Fonction de création des régions françaises
******************************************************************************************************************** """
def createFrRegionFromInseeFile(MongoTable, MongoTableStat, pFile, pParent, pChildren):

  Log.info("BEGIN : Creation of FrRegion...")

  lFile = openFile(pFile)
  if lFile is False:
    return False

  Lines = lFile.read().split("\n")
  # On ne garde pas la première ligne
  Lines = Lines[1:]
  # On récupère chaque ligne du fichier
  for i, line in enumerate(Lines):
    # Que l'on sépare
    Words = line.split("\t")
    # On vérifie que l'on a bien le bon nombre de paramètres
    if len(Words) != 5:
      Log.error(className, "{} has incorrect syntax to be used at line {}".format(pFile, i))
    else:
      # Enregistrement de la donnée si le résultat de la conversion est correcte
      lFrRegion = FrRegionData()
      result = lFrRegion.fromInsee(Words, pParent, pChildren)
      if result is not True:
        Log.warning(className, "Information is incorrect : {}".format(result))
      else:
        MongoTable.insert_one(lFrRegion.toTable())
        MongoTableStat.insert_one(StatistiqueData(lFrRegion.id).toTable())

  Log.info("END : {} FrRegions has been created".format(MongoTable.find().count()))
  return True

""" ********************************************************************************************************************
   Fonction de création des départements français
******************************************************************************************************************** """
def createFrDepartmentFromInseeFile(MongoTable, MongoTableStat, pFile, pParentName, pChildrenName):

  Log.info("BEGIN : Creation of FrDepartement...")

  lFile = openFile(pFile)
  if lFile is False:
    return None

  Lines = lFile.read().split("\n")
  # On ne garde pas la première ligne
  Lines = Lines[1:]
  # On récupère chaque ligne du fichier
  for i, line in enumerate(Lines):
    # Que l'on sépare
    Words = line.split("\t")
    # On vérifie que l'on a bien le bon nombre de paramètres
    if len(Words) != 6:
      Log.error(className, "{} has incorrect syntax to be used at line {}".format(pFile, i))
    else:
      # Enregistrement de la donnée si le résultat de la conversion est correcte
      lFrDepartData = FrDepartmentData()
      result = lFrDepartData.fromInsee(Words, pParentName, pChildrenName)
      if result is not True:
        Log.warning(className, "Information is incorrect : {}".format(result))
      else:
        MongoTable.insert_one(lFrDepartData.toTable())
        MongoTableStat.insert_one(StatistiqueData(lFrDepartData.id).toTable())

  Log.info("END : {} FrDepartments has been created".format(MongoTable.find().count()))
  return True

""" ********************************************************************************************************************
   Fonction de création des villes françaises
******************************************************************************************************************** """
def createFrCityFromInseeFile(MongoTable, MongoTableStat, pFile, pParentName):

  Log.info("BEGIN : Creation of FrCity...")

  lFile = openFile(pFile)
  if lFile is False:
    return False

  Lines = lFile.read().split("\n")
  # On ne garde pas la première ligne
  Lines = Lines[1:]
  # On récupère chaque ligne du fichier
  for i, line in enumerate(Lines):
    # Que l'on sépare
    Words = line.split("\t")
    # On vérifie que l'on a bien le bon nombre de paramètres
    if len(Words) != 12:
      Log.error(className, "{} has incorrect syntax to be used at line {}".format(pFile, i))
    else:
      # Enregistrement de la donnée si le résultat de la conversion est correcte
      lFrCityData = FrCityData()
      result = lFrCityData.fromInsee(Words, pParentName)
      if result is not True:
        Log.warning(className, "Information is incorrect : {}".format(result))
      else:
        lId = MongoTable.insert_one(lFrCityData.toTable())
        MongoTableStat.insert_one(StatistiqueData(lId.inserted_id).toTable())

  Log.info("END : {} FrCities has been created".format(MongoTable.find().count()))
  return True


""" ********************************************************************************************************************
  Creation of Data
******************************************************************************************************************** """
def createLocalisationData(MongoClient, mongo_settings, settings):
  Log.info("--------------------------------------------------------------------------------------------------------")
  Log.info("BEGIN : Localisation data creation begin...")

  # Vérification de la connection MongoDB
  if not isMongoDBClient(MongoClient):
    return False

  # Création des accès aux tables souhaitées
  ContinentDataTable    = MongoClient.db[mongo_settings.get('LocalisationModel', 'continent')]
  CountryDataTable      = MongoClient.db[mongo_settings.get('LocalisationModel', 'country'  )]
  FrRegionDataTable     = MongoClient.db[mongo_settings.get('LocalisationModel', 'frregion' )]
  FrDepartmentDataTable = MongoClient.db[mongo_settings.get('LocalisationModel', 'frdepart' )]
  FrCityDataTable       = MongoClient.db[mongo_settings.get('LocalisationModel', 'frcity'   )]
  ContinentStatTable    = MongoClient.db[mongo_settings.get('LocalisationModel', 'continentStat')]
  CountryStatTable      = MongoClient.db[mongo_settings.get('LocalisationModel', 'countryStat'  )]
  FrRegionStatTable     = MongoClient.db[mongo_settings.get('LocalisationModel', 'fraRegionStat' )]
  FrDepartmentStatTable = MongoClient.db[mongo_settings.get('LocalisationModel', 'fraDepartStat' )]
  FrCityStatTable       = MongoClient.db[mongo_settings.get('LocalisationModel', 'fraCityStat'   )]

  # Récupération des noms de fichiers contenant les données
  mainDir               = settings.get('LocalisationDirFiles', 'mainDir')
  countryFileName       = mainDir + "/" + settings.get('LocalisationDirFiles', 'country')
  frRegionFileName      = mainDir + "/" + settings.get('LocalisationDirFiles', 'frRegion')
  frDepartmentFileName  = mainDir + "/" + settings.get('LocalisationDirFiles', 'frDepart')
  frCityFileName        = mainDir + "/" + settings.get('LocalisationDirFiles', 'frCity')

  # Vérification si les fichiers existent
  if not isExist(countryFileName)     : return False
  if not isExist(frRegionFileName)    : return False
  if not isExist(frDepartmentFileName): return False
  if not isExist(frCityFileName)      : return False

  # Créations des données
  if not createContinentFromDictionnary(ContinentDataTable, ContinentStatTable)         : return False
  if not createCountryFromInseeFile(CountryDataTable, CountryStatTable, countryFileName): return False
  if not createFrRegionFromInseeFile(FrRegionDataTable, FrRegionStatTable, frRegionFileName,
                                       "FRA", mongo_settings.get('LocalisationModel', 'frdepart' )):
    return False

  if not createFrDepartmentFromInseeFile(FrDepartmentDataTable, FrDepartmentStatTable, frDepartmentFileName,
                                           mongo_settings.get('LocalisationModel', 'frregion' ),
                                           mongo_settings.get('LocalisationModel', 'frcity' )):
    return False

  if not createFrCityFromInseeFile(FrCityDataTable, FrCityStatTable, frCityFileName,
                                     mongo_settings.get('LocalisationModel', 'frdepart' )):
    return False

  Log.info("END : Localisation data done")
  Log.info("--------------------------------------------------------------------------------------------------------")
  return True


""" ********************************************************************************************************************
  Return the equivalence betwwen old and new database
******************************************************************************************************************** """
def getEquivalenceLocalisation(pCatId, pName, SqlClient, MongoClient, mongo_settings):
  if type(pCatId) is not int:
    Log.error(className, "pCatId is not an int")
    return False
  if type(pName) is not str:
    Log.error(className, "pName is not a str")
    return False

  # Département
  if 0 <= pCatId < 100 or 971 <= pCatId < 999:
    FrDepartmentTable = MongoClient.db[mongo_settings.get('LocalisationModel', 'frdepart')]
    # On cherche le nouvel Id dans MongoDb
    result = FrDepartmentTable.find({"name": pName})
    if result.count() == 1:
      return {mongo_settings.get('LocalisationModel', 'frdepart'), result.next().get("_id")}
    # Si plusieurs résultats, on cherche des possibilitées
    if result.count() != 1:
      # Dans le cas de la Corse, on met la région car pas de distinction entre Nord et Sud avant
      if pName=="Corse":
        FrRegionDataTable = MongoClient.db[mongo_settings.get('LocalisationModel', 'frregion')]
        # On cherche le nouvel Id dans MongoDb
        result = FrRegionDataTable.find({"name": "Corse"})
        # Si un seul résultat
        if result.count() == 1:
          return {mongo_settings.get('LocalisationModel', 'frregion'), result.next().get("_id")}
      # Dans le cas des Alpes Hautes Provinces
      elif pName=="Alpes de Hautes-Provence":
        # On cherche le nouvel Id dans MongoDb
        result = FrDepartmentTable.find({"name": "Alpes-de-Haute-Provence"})
        if result.count() == 1:
          return {mongo_settings.get('LocalisationModel', 'frdepart'), result.next().get("_id")}
      # Dans le cas des Côtes-d'Armor
      elif pName=="Côtes d'Armor":
        # On cherche le nouvel Id dans MongoDb
        result = FrDepartmentTable.find({"name": "Côtes-d'Armor"})
        if result.count() == 1:
          return {mongo_settings.get('LocalisationModel', 'frdepart'), result.next().get("_id")}
      # Dans le cas de la Réunion
      elif pName=="Réunion":
        # On cherche le nouvel Id dans MongoDb
        result = FrDepartmentTable.find({"name": "La Réunion"})
        if result.count() == 1:
          return {mongo_settings.get('LocalisationModel', 'frdepart'), result.next().get("_id")}
      # Dans le cas de la Guyane
      elif pName == "Antilles-Guyanne":
        # On cherche le nouvel Id dans MongoDb
        result = FrDepartmentTable.find({"name": "Guyane"})
        if result.count() == 1:
          return {mongo_settings.get('LocalisationModel', 'frdepart'), result.next().get("_id")}

    # Si rien n'a été trouvé
    Log.error(className, "Impossible to found the Department named {}".format(pName))
    return False


  # France
  elif pCatId == 201:
    CountryTable = MongoClient.db[mongo_settings.get('LocalisationModel', 'country')]
    result = CountryTable.find({"nameFr":"France"})
    if result.count() != 1:
      Log.error(className, "Impossible to find France country !")
      return False
    return {mongo_settings.get('LocalisationModel', 'country'), result.next().get("_id")}

  # Continents (ici on fait à la main)
  elif 201 < pCatId <= 208:
    result = ""
    ContinentDataTable = MongoClient.db[mongo_settings.get('LocalisationModel', 'continent')]
    if pCatId == 202:
      result = ContinentDataTable.find({"nameFr": "Europe"}           ).next().get("_id", None)
    elif pCatId == 203:
      result = ContinentDataTable.find({"nameFr": "Amérique du Nord"} ).next().get("_id", None)
    elif pCatId == 204:
      result = ContinentDataTable.find({"nameFr": "Amérique du Sud"}  ).next().get("_id", None)
    elif pCatId == 205 and pCatId == 206:
      result = ContinentDataTable.find({"nameFr": "Afrique"}          ).next().get("_id", None)
    elif pCatId == 207:
      result = ContinentDataTable.find({"nameFr": "Asie"}             ).next().get("_id", None)
    elif pCatId == 208:
      result = ContinentDataTable.find({"nameFr": "Océanie"}          ).next().get("_id", None)
    # On vérifie le résultat
    if result is None:
      Log.error(className, "Impossible to found the continent named {}".format(pName))
      return False
    return {mongo_settings.get('LocalisationModel', 'continent'), result}

  # Région Françaises
  elif 300 < pCatId <= 399 :
    FrRegionDataTable = MongoClient.db[mongo_settings.get('LocalisationModel', 'frregion')]
    # On cherche le nouvel Id dans MongoDb
    result = FrRegionDataTable.find({"name": pName})
    # Si un seul résultat
    if result.count() == 1:
      return {mongo_settings.get('LocalisationModel', 'frregion'), result.next().get("_id")}

    Log.error(className, "Impossible to find this region named {}".format(pName))
    return False

  return False

