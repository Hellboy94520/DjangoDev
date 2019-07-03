from django.db import models
from ..models import User
from datetime import datetime


""" --------------------------------------------------------------------------------------------------------------------
------------------------------------------------------------------------------------------------------------------------
Data
------------------------------------------------------------------------------------------------------------------------
-------------------------------------------------------------------------------------------------------------------- """
PaypalRefSize   = 20
NLSize          = 10


""" --------------------------------------------------------------------------------------------------------------------
------------------------------------------------------------------------------------------------------------------------
Class
------------------------------------------------------------------------------------------------------------------------
-------------------------------------------------------------------------------------------------------------------- """
class Payment(models.Model):
  sum           = models.DecimalField(max_digits=7, decimal_places=2, default = 0)     # Sum of the purchase
  date          = models.DateTimeField(default=datetime.now())
  details       = models.TextField(default="")
  account       = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, default=None)
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

  """ ---------------------------------------------------- """
  def get_payment(self):
    # Search if it is a Paypal Payment
    lPaypal = PaypalPayment.objects.filter(payment=self)
    if   len(lPaypal) == 1:
      return lPaypal[0]

    return None


""" --------------------------------------------------------------------------------------------------------------------
------------------------------------------------------------------------------------------------------------------------
Class Paypal
------------------------------------------------------------------------------------------------------------------------
-------------------------------------------------------------------------------------------------------------------- """
class PaypalPayment(models.Model):
  objects = None
  reference = models.CharField(max_length=PaypalRefSize, default="")                     # Paypal reference
  date      = models.DateTimeField(default=datetime.now())
  payment   = models.OneToOneField(Payment, on_delete=models.CASCADE, primary_key=True)

