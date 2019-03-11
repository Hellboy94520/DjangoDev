class Site:

  """ ******************************************************************************************************************
    Constructor
  ****************************************************************************************************************** """
  def __init__(self, pTab):
    self.id           = int(pTab[0])  #site_id
    self.name         = pTab[1]       #site_name

    self.category     = None

  def __repr__(self):
    return "{}, {}, {}\n".format(self.id, self.name, self.category)

