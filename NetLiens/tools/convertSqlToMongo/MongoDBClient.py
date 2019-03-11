from pymongo import MongoClient

class MongoDBClient:

  def __init__(self, hostname, port, database):
    self.hostname = hostname
    self.client = MongoClient(str(hostname), int(port))
    self.db = database

    self.db = self.client.NetLiens
    print("Connected to MongoDb database")

  def __del__(self):
    print("Delete MongoDBClient instance from database \'" + self.hostname + "\'")
    self.client.close()