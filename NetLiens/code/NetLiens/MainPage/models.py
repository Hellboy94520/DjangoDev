from django.db import models

# Create your models here.

""" --------------------------------------------------------------------------------------------------------------------
User (NetLiens SQL)
-------------------------------------------------------------------------------------------------------------------- """
class Users(models.Model):
  name = models.CharField(max_length=20)
  family_name = models.CharField(max_length=20)
  user_name = models.CharField(max_length=20)
  email = models.CharField(max_length=50)
  password = models.CharField(max_length=20)
  company_name = models.CharField(max_length=50)

  def __str__(self):
    return print("{}_{} : {}".format(self.family_name, self.name, self.user_name))

""" --------------------------------------------------------------------------------------------------------------------
AnnuCats (NetLiens SQL)
-------------------------------------------------------------------------------------------------------------------- """
class AnnuCats(models.Model):
  cat_id = models.AutoField(primary_key=True)
  cat_name = models.CharField(max_length=255)
  cat_parent = models.PositiveIntegerField()
  cat_priority = models.PositiveSmallIntegerField()
  cat_show = models.IntegerField()
  cat_locked = models.IntegerField()
  cat_subd_geo = models.IntegerField()
  cat_subd_type = models.IntegerField()
  cat_color = models.CharField(max_length=7)

  class Meta:
    managed = False
    db_table = 'annu_cats'

  def __str__(self):
    return print("Id={}, name={}".format(self.id, self.name))


""" --------------------------------------------------------------------------------------------------------------------
AnnuSite (NetLiens SQL)
-------------------------------------------------------------------------------------------------------------------- """
class AnnuSite(models.Model):
  site_id = models.AutoField(primary_key=True)
  site_name = models.CharField(max_length=255)
  site_url = models.CharField(max_length=255)
  site_mail = models.CharField(max_length=100)
  site_pr = models.PositiveIntegerField()
  site_pr_lastchecked = models.PositiveIntegerField()
  site_status = models.IntegerField()
  site_dispmode = models.IntegerField()
  site_reg_date = models.PositiveIntegerField()
  site_valid_date = models.PositiveIntegerField()
  site_mail_date = models.PositiveIntegerField()
  site_dept = models.PositiveSmallIntegerField()
  site_priority = models.IntegerField()
  site_ip = models.CharField(max_length=15)
  site_origine = models.PositiveIntegerField()
  site_clics = models.BigIntegerField()
  site_rss = models.CharField(max_length=255)
  site_lien_retour = models.IntegerField()
  site_vis_retours = models.BigIntegerField()
  site_vis_retours_06 = models.BigIntegerField()
  site_is_officetourisme = models.IntegerField()
  site_is_criteria = models.CharField(max_length=255)
  site_is_1stpage = models.IntegerField()
  site_residence = models.SmallIntegerField()
  site_validator = models.CharField(max_length=50)
  site_pagerank = models.IntegerField()
  site_lien_retour_url = models.TextField()
  site_paypal_txn = models.CharField(max_length=32)
  site_type_inscr = models.CharField(max_length=15)

  class Meta:
    managed = False
    db_table = 'annu_site'


""" --------------------------------------------------------------------------------------------------------------------
AnnuSiteAppartient (NetLiens SQL)
-------------------------------------------------------------------------------------------------------------------- """
class AnnuSiteAppartient(models.Model):
  app_site_id = models.IntegerField(primary_key=True)
  app_cat_id = models.IntegerField()
  app_priority = models.IntegerField()

  class Meta:
    managed = False
    db_table = 'annu_site_appartient'
    unique_together = (('app_site_id', 'app_cat_id'),)