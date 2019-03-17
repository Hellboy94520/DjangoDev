from SqlConnection import *
from MongoDBClient import *
from CategoryManager import createCategoryData
from LocalisationManager import createLocalisationData, getEquivalenceLocalisation
import Log
import os

print("Get value of *.ini files")
import configparser
settings = configparser.ConfigParser()
settings._interpolation = configparser.ExtendedInterpolation()
if not settings.read(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'private/auth_param.ini')):
  Log.fatal("main", "Impossible to open auth_param.ini !")
  exit(1)

mongodb_param = configparser.ConfigParser()
mongodb_param._interpolation = configparser.ExtendedInterpolation()
if not mongodb_param.read(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'private/mongodb_param.ini')):
  Log.fatal("main", "Impossible to open mongodb_param.ini !")
  exit(1)


Log.info("************************************************************************************************************")
Log.info("Starting Conversion\n")

# Open SQL Network
NetLiensSqlNetwork = SqlConnection(settings.get('sql_localhost', 'address'),
                                   settings.get('sql_localhost', 'user'),
                                   settings.get('sql_localhost', 'password'),
                                   settings.get('sql_localhost', 'databasename'))

NetLiensMongoDb = MongoDBClient(settings.get('mongodb_localhost', 'address'),
                                settings.get('mongodb_localhost', 'port'),
                                "NetLiens")

""" --------------------------------------------------------------------------------------------------------------------
CategoryManager
-------------------------------------------------------------------------------------------------------------------- """
#if not createCategoryData(NetLiensSqlNetwork, NetLiensMongoDb, mongodb_param) : exit(1)


""" --------------------------------------------------------------------------------------------------------------------
LocalisationManager
-------------------------------------------------------------------------------------------------------------------- """
#if not createLocalisationData(NetLiensMongoDb, mongodb_param, settings) : exit(1)

""" --------------------------------------------------------------------------------------------------------------------
ANNU_SITE & ANNU_SITE_APPARTIENT
-------------------------------------------------------------------------------------------------------------------- """
sites = NetLiensSqlNetwork.set_command("SELECT * FROM `annu_site`")
for site in sites:
  cat = NetLiensSqlNetwork.set_command("SELECT * from `annu_dept` WHERE `id_dept`={}".format(site[11]))
  if len(cat) != 0:
    if getEquivalenceLocalisation(cat[0][0], cat[0][1], NetLiensSqlNetwork, NetLiensMongoDb, mongodb_param) is False:
      print("No found : {}".format(cat))


""" Association des Sites avec les catégories ----------------------------------------------------------------------"""
# Site.site_category_association(NetLiensSqlNetwork, Category.categories)

Log.info("End Conversion")
Log.info("************************************************************************************************************")
exit(0)