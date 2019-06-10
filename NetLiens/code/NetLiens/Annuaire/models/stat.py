from django.db import models
from datetime import datetime
from .account import User


""" --------------------------------------------------------------------------------------------------------------------
------------------------------------------------------------------------------------------------------------------------
Class
------------------------------------------------------------------------------------------------------------------------
-------------------------------------------------------------------------------------------------------------------- """
class Stat(models.Model):
  objects = None
  creation_date    = models.DateTimeField(default=datetime.now())
  creation_user    = models.ForeignKey(User                        ,
                                       related_name="creation_user",
                                       on_delete=models.SET_NULL   ,
                                       null=True)
  validation_date  = models.DateTimeField(default=None, null=True)
  validation_user  = models.ForeignKey(User                          ,
                                       related_name="validation_user",
                                       default=None                  ,
                                       on_delete=models.SET_NULL     ,
                                       null=True)

  """ ---------------------------------------------------- """
  def create(self):
    self.save()

  """ ---------------------------------------------------- """
  """ RETURN : - True if okay
           - '-1' if many StatDaily has found on same date"
           - '-2' if many StatMonthly has found on same date"  """
  def add_one_view(self):
    # Get the current object stat
    lCurrentDayList   = StatDaily.objects.filter(stat=self, date=datetime.now())
    lCurrentMonthList = StatMonthly.objects.filter(stat=self, date=datetime.now())
    # Check if the today object exist, if not create it
    if   len(lCurrentDayList) == 0:
      lCurrentDay = StatDaily()
      lCurrentDay.create()
    elif len(lCurrentDayList) == 1:
      lCurrentDay = lCurrentDayList[0]
    else:
      return -1
    # Check if the month object exist, if not create it
    if   len(lCurrentMonthList) == 0:
      lCurrentMonth = StatDaily()
      lCurrentMonth.create()
    elif len(lCurrentMonthList) == 1:
      lCurrentMonth = lCurrentMonthList[0]
    else:
      return -2

    # Add one view for each one
    lCurrentDay.add_one_view()
    lCurrentMonth.add_one_view()
    return True


""" ---------------------------------------------------------------------------------------------------------------- """
class StatDaily(models.Model):
  objects = None
  date  = models.DateField(default=datetime.now())
  count = models.IntegerField(default=0)
  stat  = models.ForeignKey(Stat, unique_for_date="date", on_delete=models.CASCADE)

  """ ---------------------------------------------------- """
  def create(self):
    self.save()

  """ ---------------------------------------------------- """
  def add_one_view(self):
    self.count += 1
    self.save()


""" ---------------------------------------------------------------------------------------------------------------- """
class StatMonthly(models.Model):
  objects = None
  month = models.DateField(default=datetime.now())
  count = models.IntegerField(default=0)
  stat  = models.ForeignKey(Stat, unique_for_month="date", on_delete=models.CASCADE)

  """ ---------------------------------------------------- """
  def create(self):
    self.save()

  """ ---------------------------------------------------- """
  def add_one_view(self):
    self.count += 1
    self.save()


""" ---------------------------------------------------------------------------------------------------------------- """


