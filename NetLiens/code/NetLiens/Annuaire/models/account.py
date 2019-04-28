from django.db import models
from datetime import datetime, timedelta
from django.contrib.auth.models import User
from uuid import uuid4

from .payment import Payment


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
-------------------------------------------------------------------------------------------------------------------- """
activationDaysDelay = 7

class AccountActivation(models.Model):
  link          = models.SlugField(default=uuid4(), max_length=20, unique=True)
  expiration    = models.DateTimeField(default=datetime.now()+timedelta(days=activationDaysDelay))


class AccountCustomer(User):
  is_staff      = False
  is_superuser  = False

  company = models.CharField(max_length=50)

  activation = models.OneToOneField(AccountActivation, null=True, on_delete=models.SET_NULL)
  
  # sites = models.ForeignKey(Site, null=True, on_delete=models.CASCADE)
  # payment = models.ForeignKey(Payment, null=True, on_delete=models.CASCADE)


class AccountAdmin(User):
  is_staff      = True
  is_superuser  = False


""" --------------------------------------------------------------------------------------------------------------------
------------------------------------------------------------------------------------------------------------------------
Functions
------------------------------------------------------------------------------------------------------------------------
-------------------------------------------------------------------------------------------------------------------- """


" --- Creation of User --- "
def create_user(pAccount: (AccountAdmin, AccountCustomer), pUsername: str, pFirstName: str,
                pLastName: str, pEmail: str, pPassword: str, pIsActive: bool):

  if User.objects.filter(username=pUsername).count() != 0:
    return "Error : username already exist"
  if User.objects.filter(email=pEmail      ).count() != 0:
    return "Error : email already used"

  #TODO: vérifier que c'est bien une adresse mail

  pAccount.username   = pUsername
  pAccount.last_name  = pLastName
  pAccount.first_name = pFirstName
  pAccount.email      = pEmail
  pAccount.password   = pPassword
  pAccount.is_active  = pIsActive

  return True


" --- Creation of a customer account --- "
def create_customer(pUsername: str, pFirstName: str, pLastName: str, pEmail: str, pPassword: str, pIsActive: bool,
                 pCompany: str, pUser: AccountAdmin):

  # Create account from User
  lAccount = AccountCustomer()

  lResult = create_user(lAccount, pUsername, pFirstName, pLastName, pEmail, pPassword, pIsActive)
  if type(lResult) is str:
    return lResult
  lAccount.company = pCompany

  lActivation = AccountActivation()
  lAccount.activation = lActivation

  lAccount.save()

  return lAccount


" --- Creation of a validation account --- "
def create_valid(pUsername: str, pFirstName: str, pLastName: str, pEmail: str, pPassword: str, pIsActive: bool,
                 pUser: AccountAdmin):

  # Create account from Admin
  lAccount = AccountAdmin()

  lResult = create_user(lAccount, pUsername, pFirstName, pLastName, pEmail, pPassword, pIsActive)
  if type(lResult) is str:
    return lResult

  lAccount.save()

  return lAccount


" --- Creation of an admin account --- "
# TODO: Rajouter l'argument "pUser: AccountAdmin"
def create_admin(pUsername: str, pFirstName: str, pLastName: str, pEmail: str, pPassword: str, pIsActive: bool):

  # Create account from Admin
  lAccount = AccountAdmin()

  lResult = create_user(lAccount, pUsername, pFirstName, pLastName, pEmail, pPassword, pIsActive)
  if type(lResult) is str:
    return lResult
  lAccount.is_superuser = True

  lAccount.save()

  return lAccount
