""" ********************************************************************************************************************
   CategoryData
******************************************************************************************************************** """
class CategoryData:
  """ -- Constructor ----------------------------------------------------------------------------------------------- """
  def __init__(self):
    self.id            = None
    self.nameFr        = None
    self.nameEn        = None
    self.order         = None
    self.parent        = None
    self.resume        = None

  def fromAnnuCat(self, pTab):
    self.id            = 0              # mongodb_id
    self.nameFr        = pTab[1]        # cat_name
    self.order         = 0
    self.parent        = pTab[2]        # cat_parent
    self.resume        = pTab[0]        # cat_id

  def fromCategoryData(self, pCategory):
    self.id            = pCategory.id
    self.nameFr        = pCategory.nameFr
    self.nameEn        = pCategory.nameEn
    self.order         = pCategory.order
    self.parent        = pCategory.parent
    self.resume        = ""

  """ -- Affichage de l'object ------------------------------------------------------------------------------------- """
  def __repr__(self):
    return "id= {}, {} {} : {}\n".format(self.id, self.nameFr, self.parent, self.resume)

  def toTable(self):
    return {"nameFr" : self.nameFr,
            "nameEn" : self.nameEn,
            "order"  : self.order,
            "parent" : self.parent,
            "resume" : self.resume}


from datetime import datetime, timedelta


""" ********************************************************************************************************************
   CategoryStat
******************************************************************************************************************** """
class CategoryStat:
  """ -- Constructor ----------------------------------------------------------------------------------------------- """
  def __init__(self, pCategoryData):
    self.id           = pCategoryData.id
    self.creationDate = datetime.now() - timedelta(days=1)
    self.lastModDate  = datetime.now()
    self.lastModUser  = "portage"
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