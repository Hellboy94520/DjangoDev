from django.db import models
from datetime import datetime
from django.contrib.auth.models import User

""" --------------------------------------------------------------------------------------------------------------------
------------------------------------------------------------------------------------------------------------------------
Data
------------------------------------------------------------------------------------------------------------------------
-------------------------------------------------------------------------------------------------------------------- """
SubjectSize = 20


""" --------------------------------------------------------------------------------------------------------------------
------------------------------------------------------------------------------------------------------------------------
Class
------------------------------------------------------------------------------------------------------------------------
-------------------------------------------------------------------------------------------------------------------- """
# TODO: Voir comment lié le message à deux comptes et que si l'un des deux comptes est supprimées, le message l'est aussi !
class Message(models.Model):
  is_read   = models.BooleanField(default=False)  # Indicate if the message is read
  content   = models.TextField(max_length=SubjectSize)
  date      = models.DateTimeField(default=datetime.now())

  def __init__(self, pContent: str):
    models.Model.__init__(self)
    # Avoid to call my __setattr__ each time
    object.__setattr__(self, 'is_read'     , False)
    object.__setattr__(self, 'content'     , pContent)
    object.__setattr__(self, 'date'        , datetime.now())
    self.save()

  def __setattr__(self, key, value):
    object.__setattr__(self, key, value)
    self.save()

  def __repr__(self):
    return "Message : is_read={}, date={}, content={}"\
      .format(str(self.is_read), str(self.date), self.content)
