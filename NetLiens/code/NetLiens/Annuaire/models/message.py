from django.db import models
from datetime import datetime
from django.contrib.auth.models import User

""" --------------------------------------------------------------------------------------------------------------------
------------------------------------------------------------------------------------------------------------------------
Data
------------------------------------------------------------------------------------------------------------------------
-------------------------------------------------------------------------------------------------------------------- """
class Message(models.Model):
  sender        = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
  recipient     = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
  subject       = models.TextField()
  date          = models.DateTimeField(default=datetime.now())
  content       = models.TextField()

  def __repr__(self):
      return "Message : sender={}, recipient={}, subject={}, content={}".format(self.sender, self.recipient,
                                                                                self.subject, self.content)

  class Meta:
    abstract = True


class MessageUnread(Message):
  pass

class MessageRead(Message):
  pass


""" --------------------------------------------------------------------------------------------------------------------
------------------------------------------------------------------------------------------------------------------------
Functions
------------------------------------------------------------------------------------------------------------------------
-------------------------------------------------------------------------------------------------------------------- """
def create(pSender: User, pRecipient: User, pSubject, pContent: str):

  if pSender.username == pRecipient.username:
    return "sender: has the same username of recipient"

  lMessage = MessageUnread()
  lMessage.sender     = pSender
  lMessage.recipient  = pRecipient
  lMessage.subject    = pSubject
  lMessage.date       = datetime.now()
  lMessage.content    = pContent
  lMessage.save()

  return lMessage


def message_read(pMessage: MessageUnread):

  lMessage = MessageRead.copy(pMessage)
  lMessage.save()
  pMessage.delete()

  return lMessage
