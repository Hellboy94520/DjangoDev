from SqlConnection import SqlConnection
from NetLiensData.Site import Site

class SiteManager:

  def __init__(self):
    self.sites = []


  def get_annu_site(self, NetLiensSqlNetwork):
    try:
      type(NetLiensSqlNetwork)==SqlConnection
    except:
      print("get_annu_cat : it is not a SqlNetwork")
      return False

    " Conversion des annu_site en Site "
    for annu_site in NetLiensSqlNetwork.set_command("SELECT * FROM `annu_site`"):
      self.sites[annu_site[0]] = Site(annu_site)

    print("{} sites are created".format(len(self.sites)))
    print("-----------------------------------------------------------------------------------------------------------")



  def site_category_association(self, NetLiensSqlNetwork, CategoryList):
    try:
      type(NetLiensSqlNetwork) == SqlConnection
    except:
      print("get_annu_parent: it is not a SqlNetwork")


    " On récupère les sites_apppartient "
    annu_site_appartientList = NetLiensSqlNetwork.set_command("SELECT * FROM `annu_site_appartient`")
    print("{} appartients are created".format(len(annu_site_appartientList)))

    for annu_site_appartient in annu_site_appartientList:
      # print("Search with appartient = {}".format(annu_site_appartient))

      " On récupère le site qui correspond "
      siteFound = self.sites.get(annu_site_appartient[0], None)
      if siteFound is None:
        print("Impossible to found Site with id={}".format(annu_site_appartient[0]))
        continue

      " On cherche la catégorie associée "
      categoryFound = None
      for category in CategoryList:
        " Si on le trouve, on l'enregistre "
        categoryFound = category.isContain(int(annu_site_appartient[1]))
        if categoryFound is not None:
          break

      if categoryFound is None:
        print("Impossible to found the category with id={}".format(annu_site_appartient[1]))
        continue
      # else:
      # print("Found category: {}".format(categoryFound))

      " Dans le cas ou la catégorie et le site ont été trouvées "
      categoryFound.addSite(siteFound)
      siteFound.category = categoryFound.name