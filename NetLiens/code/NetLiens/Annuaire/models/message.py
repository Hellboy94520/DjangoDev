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

  def __repr__(self):
    return "Message : is_read={}, date={}, content={}"\
      .format(str(self.is_read), str(self.date), self.content)


" -------------------------------------------------------------------------------------------------------------------- "
def create_message(pContent: str):
  lMesg = Message()
  lMesg.content = pContent
  lMesg.save()
