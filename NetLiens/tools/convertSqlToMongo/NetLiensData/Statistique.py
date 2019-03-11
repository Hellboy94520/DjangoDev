from datetime import datetime, timedelta

""" ********************************************************************************************************************
   StatistiqueData
******************************************************************************************************************** """
class StatistiqueData:
  """ -- Constructor ----------------------------------------------------------------------------------------------- """
  def __init__(self, pId):
    self.id           = pId
    self.creationDate = datetime.now() - timedelta(days=1)
    self.lastModDate  = datetime.now()
    self.lastModUser  = "ConversionProgram"
    self.last1dConsu  = 0
    self.last1wConsu  = 0
    self.last1mConsu  = 0
    self.last1yConsu  = 0

  def toTable(self):
    return {"_id"           : self.id,
            "creationDate"  : self.creationDate,
            "lastModDate"   : self.lastModDate,
            "lastModUser"   : self.lastModUser,
            "last1dConsu"   : self.last1dConsu,
            "last1wConsu"   : self.last1wConsu,
            "last1mConsu"   : self.last1mConsu,
            "last1yConsu"   : self.last1yConsu}