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
class Conversation(models.Model):
  sender        = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
  recipient     = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
  subject       = models.CharField(max_length=SubjectSize)

  " --- Constructor --- "
  def __init__(self, pSender: User, pRecipient: User, pSubject: str, pContent):
    models.Model.__init__(self)
    # Avoid to call my __setattr__ each time
    object.__setattr__(self, 'sender'   , pSender)
    object.__setattr__(self, 'recipient', pRecipient)
    object.__setattr__(self, 'subject'  , pSubject)
    self.save()
    Message(True, pContent, self)

  " --- Setter --- "
  def __setattr__(self, key, value):
    object.__setattr__(self, key, value)
    self.save()

  " --- Shower --- "
  def __repr__(self):
    return "Conversation : sender={}, recipient={}, subject={}"\
      .format(self.sender, self.recipient, self.subject)

  " --- Return messages organized by date (most recent to old) --- "
  def get_messages(self):
    return Message.objects.filter(conv=self).order_by('-date')


""" ---------------------------------------------------------------------------------------------------------------- """
class Message(models.Model):
  is_sender = models.BooleanField()               # Indicate who send the message
  is_read   = models.BooleanField(default=False)  # Indicate if the message is read
  content   = models.TextField(max_length=SubjectSize)
  conv      = models.ForeignKey(Conversation, on_delete=models.CASCADE)
  date      = models.DateTimeField(default=datetime.now())

  def __init__(self, pIsSender: bool, pContent: str, pConv: Conversation):
    models.Model.__init__(self)
    # Avoid to call my __setattr__ each time
    object.__setattr__(self, 'is_sender'   , pIsSender)
    object.__setattr__(self, 'is_read'     , False)
    object.__setattr__(self, 'content'     , pContent)
    object.__setattr__(self, 'conv'        , pConv)
    object.__setattr__(self, 'date'        , datetime.now())
    self.save()

  def __setattr__(self, key, value):
    object.__setattr__(self, key, value)
    self.save()

  def __repr__(self):
    return "Message : is_sender={}, is_read={}, date={}, content={}"\
      .format(str(self.is_sender), str(self.is_read), str(self.date), self.conv)