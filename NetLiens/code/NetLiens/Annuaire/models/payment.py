from django.db import models
from datetime import datetime
from enum import Enum


""" --------------------------------------------------------------------------------------------------------------------
------------------------------------------------------------------------------------------------------------------------
Data
------------------------------------------------------------------------------------------------------------------------
-------------------------------------------------------------------------------------------------------------------- """
PaypalRefSize   = 20


class Type(Enum):
  UN = "Unknown"
  GI = "Gift"
  RE = "Reference"
  PA = "Paypal"


class NLPurchase(models.Model):
  level01 = models.PositiveSmallIntegerField()
  level02 = models.PositiveSmallIntegerField()
  level03 = models.PositiveSmallIntegerField()
  level04 = models.PositiveSmallIntegerField()
  level05 = models.PositiveSmallIntegerField()
  level06 = models.PositiveSmallIntegerField()
  level07 = models.PositiveSmallIntegerField()
  level08 = models.PositiveSmallIntegerField()
  level09 = models.PositiveSmallIntegerField()
  level10 = models.PositiveSmallIntegerField()


class PaypalPayment(models.Model):
  reference     = models.CharField(max_length=PaypalRefSize)

  def __repr__(self):
      return "PaypalPayment : {}".format(self.reference)


class Payment(models.Model):
  reference     = models.CharField(max_length=20)
  sum           = models.DecimalField(max_digits=7, decimal_places=2)
  date          = models.DateTimeField()
  purchase      = models.OneToOneField(NLPurchase, on_delete=models.CASCADE, primary_key=True)
  details       = models.TextField()

  type          = models.CharField(max_length=2,
                                   choices=[(tag, tag.value) for tag in Type],
                                   default=Type.UN)
  paypal        = models.ForeignKey(PaypalPayment, null=True, on_delete=models.CASCADE)

  def __repr__(self):
      return "Payment : type={} - reference={} - sum={}".format(self.type, self.reference, self.sum)


""" --------------------------------------------------------------------------------------------------------------------
------------------------------------------------------------------------------------------------------------------------
Functions
------------------------------------------------------------------------------------------------------------------------
-------------------------------------------------------------------------------------------------------------------- """
" --- Creation of payment --- "
def create(pType: Type, pReference: str, pDetails: str, pDate: datetime, pPurchase: int, pNLDict: dict, pPaypalRef: str):

  lPayment = Payment()
  lPayment.type      = pType
  lPayment.reference = pReference
  lPayment.details   = pDetails
  lPayment.date      = pDate
  lPayment.purchase  = pPurchase

  lNLPurchase = NLPurchase()

  for nlevel, quantity in pNLDict.items():
    add_levelToPurchase(lNLPurchase, nlevel, quantity)

  lNLPurchase.save()
  lPayment.purchase = lNLPurchase

  # In case of a paypal payment
  if pType == Type.PA:
    # Creation of PaypalPayment
    lPaypalPayment = PaypalPayment()
    lPaypalPayment.reference = pPaypalRef
    lPaypalPayment.save()
    # Save PaypalPayment in Payment
    lPayment.paypal = lPaypalPayment

  lPayment.save()


def add_levelToPurchase(pNLPurchase: NLPurchase, pLevel: int, pQuantity: int):
	if pLevel == 1:   pNLPurchase.level01 = pQuantity
	if pLevel == 2:   pNLPurchase.level02 = pQuantity
	if pLevel == 3:   pNLPurchase.level03 = pQuantity
	if pLevel == 4:   pNLPurchase.level04 = pQuantity
	if pLevel == 5:   pNLPurchase.level05 = pQuantity
	if pLevel == 6:   pNLPurchase.level06 = pQuantity
	if pLevel == 7:   pNLPurchase.level07 = pQuantity
	if pLevel == 8:   pNLPurchase.level08 = pQuantity
	if pLevel == 9:   pNLPurchase.level09 = pQuantity
	if pLevel == 10:  pNLPurchase.level10 = pQuantity
