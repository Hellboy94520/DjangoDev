from django.db import models
from datetime import datetime, timedelta
from django.contrib.auth.models import User
from .message import Message
from uuid import uuid4


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

""" --------------------------------------------------------------------------------------------------------------------
------------------------------------------------------------------------------------------------------------------------
Data
------------------------------------------------------------------------------------------------------------------------
-------------------------------------------------------------------------------------------------------------------- 
activationDaysDelay = 7

class AccountActivation(models.Model):
  link          = models.SlugField(default=uuid4(), max_length=20, unique=True)
  expiration    = models.DateTimeField(default=datetime.now()+timedelta(days=activationDaysDelay))

  def __init__(self, pLink: str, pExpiration: datetime):
    models.Model.__init__(self)
    # Avoid to call deactivated __setattr__
    self.link = pLink
    self.expiration = pExpiration

  def __repr__(self):
    return "AccountActivation : link={}, expiration={}"\
      .format(self.link, self.expiration)

  # Deactivate the modification by this way to be sure to have a log
  def __setattr__(self, key, value):
    pass
"""

""" ---------------------------------------------------------------------------------------------------------------- 
class AccountCustomer(User):
  company = models.CharField(max_length=50)
  #activation = models.OneToOneField(AccountActivation, null=True, on_delete=models.SET_NULL)

  def __init__(self, pUsername: str, pLastname: str, pFirstName: str, pEmail: str, pPassword: str, pCompany: str):
    User.__init__(self)
    object.__setattr__(self, 'username'    , pUsername)
    object.__setattr__(self, 'last_name'   , pLastname)
    object.__setattr__(self, 'first_name'  , pFirstName)
    object.__setattr__(self, 'email'       , pEmail)
    object.__setattr__(self, 'password'    , pPassword)  # TODO: Crypter le mot de passe
    object.__setattr__(self, 'company'     , pCompany)
    object.__setattr__(self, 'is_active'   , False)
    object.__setattr__(self, 'is_staff'    , False)
    object.__setattr__(self, 'is_superuser', False)
    self.save()

  def __repr__(self):
    return "AccountCustomer : username={}, last_name={}, first_name={}, email={}, company={}"\
      .format(self.username, self.last_name, self.first_name, self.email, self.company)

  def __setattr__(self, key, value):
    object.__setattr__(self, key, value)
    self.save()
"""

""" ---------------------------------------------------------------------------------------------------------------- """
class AccountAdmin(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE)

  def __repr__(self):
    return "AccountCustomer : username={}, last_name={}, first_name={}, email={}"\
      .format(self.user.username, self.user.last_name, self.user.first_name, self.user.email)


""" --------------------------------------------------------------------------------------------------------------------
------------------------------------------------------------------------------------------------------------------------
Functions
------------------------------------------------------------------------------------------------------------------------
-------------------------------------------------------------------------------------------------------------------- """
def create_account_admin(pUsername: str, pLastname: str, pFirstName: str, pEmail: str, pPassword: str,
                         pSuperUser: bool):
  User.objects.create_superuser(pUsername, pEmail, pPassword, last_name=pLastname, first_name=pFirstName,
                                is_superuser=pSuperUser)
  lAccount = AccountAdmin()
  lAccount.user = User.objects.get(username=pUsername)
  lAccount.save()

  return lAccount