from django.db import models
from datetime import datetime
from enum import Enum


""" --------------------------------------------------------------------------------------------------------------------
------------------------------------------------------------------------------------------------------------------------
Data
------------------------------------------------------------------------------------------------------------------------
-------------------------------------------------------------------------------------------------------------------- """
RefSize         = 20 # TODO: a modifier et définir un format
PaypalRefSize   = 20
NLSize          = 10


""" --------------------------------------------------------------------------------------------------------------------
------------------------------------------------------------------------------------------------------------------------
Enum
------------------------------------------------------------------------------------------------------------------------
-------------------------------------------------------------------------------------------------------------------- """
class Type(Enum):
  UN = "Unknown"
  GI = "Gift"
  RE = "Reference"
  PA = "Paypal"


""" --------------------------------------------------------------------------------------------------------------------
------------------------------------------------------------------------------------------------------------------------
Class
------------------------------------------------------------------------------------------------------------------------
-------------------------------------------------------------------------------------------------------------------- """
class Payment(models.Model):
  reference     = models.CharField(max_length=20)                         # Intern reference
  sum           = models.DecimalField(max_digits=7, decimal_places=2)     # Sum of the purchase
  type          = models.CharField(max_length=2,
                                   choices=[(tag, tag.value) for tag in Type],
                                   default=Type.UN)                       # Type of payment
  date          = models.DateTimeField()
  details       = models.TextField()

  # Quantity of NL buy in the purchase
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

  " --- Shower --- "
  def __repr__(self):
    lRepr = "Payment : reference={}, sum={}, date={}, detail={}"\
      .format(self.reference, self.sum, self.date, self.details)
    if self.level01 != 0: lRepr += ", level01={}".format(self.level01)
    if self.level02 != 0: lRepr += ", level02={}".format(self.level02)
    if self.level03 != 0: lRepr += ", level03={}".format(self.level03)
    if self.level04 != 0: lRepr += ", level04={}".format(self.level04)
    if self.level05 != 0: lRepr += ", level05={}".format(self.level05)
    if self.level06 != 0: lRepr += ", level06={}".format(self.level06)
    if self.level07 != 0: lRepr += ", level07={}".format(self.level07)
    if self.level08 != 0: lRepr += ", level08={}".format(self.level08)
    if self.level09 != 0: lRepr += ", level09={}".format(self.level09)
    if self.level10 != 0: lRepr += ", level10={}".format(self.level10)
    return lRepr


""" ---------------------------------------------------------------------------------------------------------------- """
class PaypalPayment(models.Model):
  reference     = models.CharField(max_length=PaypalRefSize)      # Paypal reference
  # TODO: Ajouter d'autres informations si Paypal en fournit plus
  payment       = models.OneToOneField(Payment, on_delete=models.CASCADE, primary_key=True)

  " --- Shower --- "
  def __repr__(self):
    return "PaypalPayment : reference={}"\
      .format(self.reference)


""" --------------------------------------------------------------------------------------------------------------------
------------------------------------------------------------------------------------------------------------------------
Class Functions
------------------------------------------------------------------------------------------------------------------------
-------------------------------------------------------------------------------------------------------------------- """
def get_nl(pPayment: Payment, pNLDict: dict):
  for nlevel, quantity in pNLDict.items():
    if nlevel == 1:     pPayment.level01 = quantity
    elif nlevel == 2:   pPayment.level02 = quantity
    elif nlevel == 3:   pPayment.level03 = quantity
    elif nlevel == 4:   pPayment.level04 = quantity
    elif nlevel == 5:   pPayment.level05 = quantity
    elif nlevel == 6:   pPayment.level06 = quantity
    elif nlevel == 7:   pPayment.level07 = quantity
    elif nlevel == 8:   pPayment.level08 = quantity
    elif nlevel == 9:   pPayment.level09 = quantity
    elif nlevel == 10:  pPayment.level10 = quantity


" --- Creation of a gift payment --- "
def create_payment_gift(pReference: str, pDetails: str, pNLDict: dict):
  lPayment = Payment()
  lPayment.reference = pReference
  lPayment.details   = pDetails
  lPayment.type      = Type.GI
  lPayment.sum       = 0
  get_nl(lPayment, pNLDict)
  lPayment.save()
  return lPayment


" --- Creation of a referencement payment --- "
def create_payment_reference(pReference: str, pDetails: str, pNLDict: dict):
  lPayment = Payment()
  lPayment.reference = pReference
  lPayment.details   = pDetails
  lPayment.type      = Type.RE
  lPayment.sum       = 0
  get_nl(lPayment, pNLDict)
  lPayment.save()
  return lPayment


" --- Creation of a referencement payment --- "
def create_payment_paypal(pReference: str, pSum: int, pDetails: str, pNLDict: dict, pPaypalRef: str):
  lPayment = Payment()
  lPayment.reference = pReference
  lPayment.details   = pDetails
  lPayment.type      = Type.PA
  lPayment.sum       = pSum
  get_nl(lPayment, pNLDict)
  lPayment.save()

  # Creation of Paypal payment
  lPaypal = PaypalPayment()
  lPaypal.reference = pPaypalRef
  lPaypal.payment   = lPayment
  lPaypal.save()

  return lPayment
