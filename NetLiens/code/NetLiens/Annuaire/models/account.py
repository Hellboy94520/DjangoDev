from django.db import models
from datetime import datetime, timedelta
from django.contrib.auth.models import User
from uuid import uuid4

""" --------------------------------------------------------------------------------------------------------------------
------------------------------------------------------------------------------------------------------------------------
HOW TO USE



------------------------------------------------------------------------------------------------------------------------
-------------------------------------------------------------------------------------------------------------------- """


""" --------------------------------------------------------------------------------------------------------------------
------------------------------------------------------------------------------------------------------------------------
Data
------------------------------------------------------------------------------------------------------------------------
-------------------------------------------------------------------------------------------------------------------- """
activationDaysDelay = 7


""" --------------------------------------------------------------------------------------------------------------------
------------------------------------------------------------------------------------------------------------------------
Class
------------------------------------------------------------------------------------------------------------------------
-------------------------------------------------------------------------------------------------------------------- """
class Account(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
  """ User :
  - username,
  - first_name,
  - last_name,
  - email,
  - password,
  - is_staff,
  - is_active,
  - is_superuser,
  - last_login,
  - date_joined,
  - user_permissions,
  - groups
  """

  """ ---------------------------------------------------- """
  class Meta:
    abstract = True


""" ---------------------------------------------------------------------------------------------------------------- """
class AccountAdmin(Account):
  objects = None

  """ ---------------------------------------------------- """
  def create(self, username: str, first_name: str, last_name: str, email: str, password: str):
    self.user = User.objects.create_user(username     = username,
                                         email        = email,
                                         password     = password,
                                         last_name    = last_name,
                                         first_name   = first_name,
                                         is_staff     = True,
                                         is_active    = True,
                                         is_superuser = True)
    self.save()

  """ ---------------------------------------------------- """
  def __repr__(self):
    return "AccountAdmin : username={}, last_name={}, first_name={}, email={}"\
      .format(self.user.username, self.user.last_name, self.user.first_name, self.user.email)


""" ---------------------------------------------------------------------------------------------------------------- """
class AccountValid(Account):
  objects = None

  """ ---------------------------------------------------- """
  def create(self, username: str, first_name: str, last_name: str, email: str, password: str, account: AccountAdmin):
    self.user = User.objects.create_user(username     = username,
                                         email        = email,
                                         password     = password,
                                         last_name    = last_name,
                                         first_name   = first_name,
                                         is_staff     = True,
                                         is_active    = True,
                                         is_superuser = False)
    self.save()

  """ ---------------------------------------------------- """
  def __repr__(self):
    return "AccountValid : username={}, last_name={}, first_name={}, email={}"\
      .format(self.user.username, self.user.last_name, self.user.first_name, self.user.email)


""" ---------------------------------------------------------------------------------------------------------------- """
class AccountCustomer(Account):
  objects = None
  company = models.CharField(max_length=50)
  # Total quantity of NL link to account
  level01       = models.PositiveSmallIntegerField(default=0)
  level02       = models.PositiveSmallIntegerField(default=0)
  level03       = models.PositiveSmallIntegerField(default=0)
  level04       = models.PositiveSmallIntegerField(default=0)
  level05       = models.PositiveSmallIntegerField(default=0)
  level06       = models.PositiveSmallIntegerField(default=0)
  level07       = models.PositiveSmallIntegerField(default=0)
  level08       = models.PositiveSmallIntegerField(default=0)
  level09       = models.PositiveSmallIntegerField(default=0)
  level10       = models.PositiveSmallIntegerField(default=0)

  """ ---------------------------------------------------- """
  def create(self, username: str, first_name: str, last_name: str, email: str, password: str, company: str,
             account: AccountAdmin):
    self.user = User.objects.create_user(username     = username,
                                         email        = email,
                                         password     = password,
                                         last_name    = last_name,
                                         first_name   = first_name,
                                         is_staff     = False,
                                         is_active    = True,
                                         is_superuser = False)
    self.company = company
    self.save()

  """ ---------------------------------------------------- """
  def get_activation(self):
    return AccountActivation.objects.get(account=self)

  """ ---------------------------------------------------- """
  def __str__(self):
    return "AccountCustomer : username={}, last_name={}, first_name={}, email={}, company={}"\
      .format(self.user.username, self.user.last_name, self.user.first_name, self.user.email, self.company)


""" --------------------------------------------------------------------------------------------------------------------
------------------------------------------------------------------------------------------------------------------------
Class Activation
------------------------------------------------------------------------------------------------------------------------
-------------------------------------------------------------------------------------------------------------------- """
class AccountActivation(models.Model):
  objects = None
  link          = models.SlugField(default=uuid4(), max_length=20, unique=True)
  expiration    = models.DateTimeField(default=datetime.now()+timedelta(days=activationDaysDelay))
  account       = models.OneToOneField(AccountCustomer, on_delete=models.CASCADE, primary_key=True)

  """ ---------------------------------------------------- """
  def create(self):
    self.save()

  """ ---------------------------------------------------- """
  def __repr__(self):
    return "AccountActivation : link={}, expiration={}"\
      .format(self.link, self.expiration)
