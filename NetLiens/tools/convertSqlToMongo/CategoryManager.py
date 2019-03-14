from NetLiensData.Category import *
import Log
from tools.Network import isMongoDBClient, isSqlClient

className = "CategoryManager"

""" ********************************************************************************************************************
   Fonction de récupération et de triage des annu_cats
******************************************************************************************************************** """
def getannu_catsFromSql(SqlClient, AnnuCatList):

  Log.info("BEGIN : Get All annu_cat from SQL Database...")

  # Récupération de tous les annu_cats
  for annu_cat in SqlClient.set_command("SELECT * FROM `annu_cats`"):

    # On vérifie si il n'existe pas deux id d'annu_cat
    if AnnuCatList.get(annu_cat[0], None) is not None:
      return Log.fatal(className, "annu_cat with id={} already exist".format(annu_cat[0]))

    # Puis on l'enregistre
    AnnuCatList[annu_cat[0]] = annu_cat

  # Vérification après conversion
  if len(AnnuCatList)==0:
    Log.fatal(className, "No annu_cat get from SQL Database")

  Log.info("END : {} categories get from SQL Database".format(len(AnnuCatList)))
  return True


def sortannu_cats(AnnuCats, AnnuCatsShow, AnnuCatsUnshow):
  Log.info("BEGIN : Sort All annu_cat from SQL Database")

  for id in AnnuCats.keys():

    # On récupère le tableau contenant les données annu_cats
    annu_cat = list(AnnuCats.get(id))

    # Si la variable cat_show est false, on l'enregistre dans la table des erreurs
    if annu_cat[4] == 0:
      AnnuCatsUnshow[id] = annu_cat
    else:
      AnnuCatsShow[id] = annu_cat

  Log.info("END : {} annu_cat are showed".format(len(AnnuCatsShow)))
  Log.info("END : {} annu_cat are unshowed".format(len(AnnuCatsUnshow)))
  return True


""" ********************************************************************************************************************
   Fonctions de création et rangement des annu_cats
******************************************************************************************************************** """
def create_errorCategory(AnnuCatUnshow, ErrorCatTable, StatCatTable):

  Log.info("BEGIN : Creation of ErrorCategory...")

  # Création des CategoryData ne souhaitant pas être affiché
  for AnnuCat in AnnuCatUnshow.values():

    # Conversion et remplissage de l'objet CategoryData et ajout dans son dictionnaire de MongoDB
    lCategoryData = CategoryData()
    lCategoryData.fromAnnuCat(AnnuCat)
    lCategoryData.parent = 0
    lCategoryData.resume = "From annu_cat with parameter cat_show to false"
    idData = ErrorCatTable.insert(lCategoryData.toTable())
    lCategoryData.id = idData

    # Création de son équivalence en CategoryStat
    lCategoryStat = CategoryStat(lCategoryData)
    idStat = StatCatTable.insert(lCategoryStat.toTable())

    # Vérification que tout c'est bien passé
    if idData != idStat:
      Log.fatal(className, "Id is not the same for CategoryData {} and StatData {} in create_errorCategory function"
                .format(idData, idStat))
      return False

  Log.info("END : Creation of ErrorCategory done")
  return True


def create_correctCategory(AnnuCatShow, CorrectCatTable, ErrorCatTable, StatCatDict):

  Log.info("BEGIN : Creation of CorrectCategory...")

  # On effectue une première conversion de tous les AnnuCatShow :
  CategoryShowList = []
  for AnnuCat in AnnuCatShow.values():

    # On créé le format Data
    lCategoryData = CategoryData()
    lCategoryData.fromAnnuCat(AnnuCat)
    idData = CorrectCatTable.insert(lCategoryData.toTable())
    lCategoryData.id = idData
    CategoryShowList.append(lCategoryData)

    # Puis le format Stat
    lCategoryStat = CategoryStat(lCategoryData)
    idStat = StatCatDict.insert(lCategoryStat.toTable())

    # On vérifie que tout c'est bien passé
    if idData != idStat:
      Log.fatal(className, "Id is not the same for CategoryData {} and StatData {} in create_correctCategory function"
                .format(idData, idStat))
      return False

  # On trie les Category à problème
  for lCategory in CategoryShowList:

    # Si la Catégorie à un parent, je cherche l'Id de son parent dans la base MongoDB
    if lCategory.parent != 0:
      parentObject = CorrectCatTable.find_one({"resume": lCategory.parent})

      # Si un unique parent a été trouvée "
      if parentObject is not None :
        # On remplace l'ancien id de son parent par le nouveau
        query = {"parent": lCategory.parent}
        new = {"$set": {"parent": parentObject.get("_id")}}
        CorrectCatTable.update_many(query, new)
      # Si le parent n'existe pas
      else:
        # On le supprime puis on l'enregistre dans la table des erreurs
        CorrectCatTable.delete_one({"_id": lCategory.id})
        lErrorCategory = CategoryData()
        lErrorCategory.fromCategoryData(lCategory)
        lErrorCategory.resume = "No parent founded"
        Log.warning(className, "No parent has found for Category : {}".format(lCategory))
        ErrorCatTable.insert(lErrorCategory.toTable())

  Log.info("END : Creation of CorrectCategory done")
  return True


""" ********************************************************************************************************************
   Creation of Data
******************************************************************************************************************** """
def createCategoryData(SQLClient, MongoClient, settings):
  Log.info("--------------------------------------------------------------------------------------------------------")
  Log.info("BEGIN : annu_cat to Category conversion...")

  annucat       = {}
  annucatShow   = {}
  annucatUnshow = {}

  # Vérification de la connection SQL
  if not isSqlClient(SQLClient): return None

  # Vérification de la connection MongoDB
  if not isMongoDBClient(MongoClient): return None

  # Création des accès aux tables souhaitées
  ErrorCatTable     = MongoClient.db[settings.get('CategoryModel', 'dict1')]
  CorrectCatTable   = MongoClient.db[settings.get('CategoryModel', 'dict2')]
  StatCatTable      = MongoClient.db[settings.get('CategoryModel', 'dict3')]



  if not getannu_catsFromSql(SQLClient, annucat)                                          : return None
  if not sortannu_cats(annucat, annucatShow, annucatUnshow)                               : return None
  if not create_errorCategory(annucatUnshow, ErrorCatTable, StatCatTable)                 : return None
  if not create_correctCategory(annucatShow, CorrectCatTable, ErrorCatTable, StatCatTable): return None

  Log.info("END : annu_cat to Category conversion done")
  Log.info("--------------------------------------------------------------------------------------------------------")
