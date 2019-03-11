# Toutes les informations de ce document sur la norme ISO 3166-1
from tools.String import adjustLowerAndUpperText

""" ********************************************************************************************************************
   ContinentDataModel
******************************************************************************************************************** """
ContinentFrCodeData = {"Afrique"        : "AF",
                       "Amérique du Nord"  : "NA",
                       "Océanie"        : "OC",
                       "Antarctique"    : "AN",
                       "Asie"           : "AS",
                       "Europe"         : "EU",
                       "Amérique du Sud": "SA"}
ContinentNameFrToUs = {"Afrique"        : "Africa"        ,
                       "Amérique du Nord"  : "North America" ,
                       "Océanie"        : "Oceania"       ,
                       "Antarctique"    : "Antarctuca"    ,
                       "Asie"           : "Asia"          ,
                       "Europe"         : "Europe"        ,
                       "Amérique du Sud": "South America" }


class ContinentData:
  """ -- Constructor ----------------------------------------------------------------------------------------------- """
  def __init__(self):
    self.id         = None    # Code du continent en deux lettres (ISO 3166-1)
    self.nameFr     = None    # Nom du continent en Français
    self.nameEn     = None    # Nom du continent en Anglais US

  def __repr__(self):
    return "id={}, {}".format(self.id, self.nameFr)

  def toTable(self):
    return {"_id"     : self.id,
            "nameFr"  : self.nameFr,
            "nameEn"  : self.nameEn}



""" ********************************************************************************************************************
   CountryDataModel
******************************************************************************************************************** """
class CountryData:
  """ -- Constructor ----------------------------------------------------------------------------------------------- """
  def __init__(self):
    self.id         = None    # Code du pays en trois lettres (ISO 3166-1 alpha 3)
    self.nameFr     = None    # Nom Français du pays
    self.nameEn     = None    # Nom Anglais US du pays
    self.parent     = None    # Id du continent parent
    self.children   = None    # Nom du dictionnaire contenant les régions du pays

  def __repr__(self):
    return "id={}, {}".format(self.id, self.nameFr)

  def toTable(self):
    return {"_id"     : self.id,
            "nameFr"  : self.nameFr,
            "nameEn"  : self.nameEn,
            "parent"  : self.parent,
            "children": self.children}

  def fromInsee(self, pWords):
    self.nameFr     = adjustLowerAndUpperText(pWords[5])
    if not pWords[9] :
      return "Id incorrect for {}".format(pWords[5])
    self.id         = pWords[9]
    return True



""" ********************************************************************************************************************
   FrRegionDataModel
******************************************************************************************************************** """
class FrRegionData:
  """ -- Constructor ----------------------------------------------------------------------------------------------- """
  def __init__(self):
    self.id           = None    # Id de la région Française
    self.name         = None    # Nom de la région Française
    self.parentId     = None    # Id du pays (France)
    self.childrenName = None    # Nom du dictionnaire contenant les départements français

  def __repr__(self):
    return "id={}, {}".format(self.id, self.name)

  def toTable(self):
    return {"_id"         : self.id,
            "name"        : self.name,
            "parentId"    : self.parentId,
            "childrenName": self.childrenName}

  def fromInsee(self, pWords, pParentId, pChildrenName):
    if not pWords[0]:
      return "Region number incorrect for {}".format(pWords[4])
    self.id           = pWords[0]
    self.name         = pWords[4]
    self.parentId     = pParentId
    self.childrenName = pChildrenName
    return True


""" ********************************************************************************************************************
   FrDepartmentDataModel
******************************************************************************************************************** """
class FrDepartmentData:
  """ -- Constructor ----------------------------------------------------------------------------------------------- """
  def __init__(self):
    self.id           = None    # Numéro du département
    self.name         = None    # Nom du département
    self.parentId     = None    # Id de la région d'appartenance
    self.parentName   = None    # Nom du dictionnaire parent où est stocké l'information
    self.childrenName = None    # Nom du dictionnaire enfant où est stocké l'information

  def __repr__(self):
    return "id={}, {}".format(self.id, self.name)

  def toTable(self):
    return{"_id"          : self.id,
           "name"         : self.name,
           "parentId"     : self.parentId,
           "parentName"   : self.parentName,
           "childrenName" : self.childrenName}

  def fromInsee(self, pWords, pParentName, pChildreName):
    if not pWords[1]:
      return "Department number is incorrect for {}".format(pWords[1])
    self.id           = pWords[1]
    self.name         = pWords[5]
    self.parentId     = pWords[0]
    self.parentName   = pParentName
    self.childrenName = pChildreName
    return True



""" ********************************************************************************************************************
   FrCityDataModel
******************************************************************************************************************** """
class FrCityData:
  """ -- Constructor ----------------------------------------------------------------------------------------------- """
  def __init__(self):
    self.name       = None  # Nom du département
    self.parentId   = None  # Id du département parent
    self.parentName = None  # Nom du dictionnaire parent où est stocké l'information

  def __repr__(self):
    return "name={}".format(self.name)

  def toTable(self):
    return {"name": self.name,
            "parentId"  : self.parentId,
            "parentName": self.parentName}

  def fromInsee(self, pWords, pParentName):
    if not pWords[11]:
      return "City name is incorrect for {}".format(pWords[5])
    self.id         = pWords[4]
    # On récupère l'article du nom, s'il existe
    if not pWords[10]:
      self.name       = pWords[11]
    else:
      # On sauvegarde l'article en supprimant les parenthèses qui l'entoure
      lArt = pWords[10][1:-1]
      if lArt != "L'":
        self.name = lArt + " " + pWords[11]
      else:
        self.name = lArt + pWords[11]
    self.parentId   = pWords[3]
    self.parentName = pParentName
    return True
