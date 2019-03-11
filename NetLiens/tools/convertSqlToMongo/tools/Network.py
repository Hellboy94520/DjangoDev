import Log
from SqlConnection import SqlConnection
from MongoDBClient import MongoDBClient

className = "tools/Network"

""" Vérifie si l'object est un MongoDbClient """
def isMongoDBClient(MongoDbClient):
  try:
    type(MongoDBClient) == MongoDBClient
  except:
    return Log.fatal(className, "Object is not a MongoDBClient object")
  return True

""" Vérifie si l'object est un SQLClient """
def isSqlClient(SqlClient):
  try:
    type(SqlClient) == SqlConnection
  except:
    return Log.error(className, "Object is not a SqlNetwork object")
  return True
