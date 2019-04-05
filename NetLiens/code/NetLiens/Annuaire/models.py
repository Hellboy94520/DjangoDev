from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
import datetime

UserMaxSize = 100


# Create your models here.

""" --------------------------------------------------------------------------------------------------------------------
Category
-------------------------------------------------------------------------------------------------------------------- """


class CategoryStat(models.Model):
    creationDate  = models.DateTimeField(default=datetime.datetime.now())
    creationUser  = models.CharField(max_length=UserMaxSize, default="creation")
    lastModDate   = models.DateTimeField(default=datetime.datetime.now())
    lastModUser   = models.CharField(max_length=UserMaxSize, default="")
    last1yConsu   = models.IntegerField(default=0)
    last1mConsu   = models.IntegerField(default=0)
    last1wConsu   = models.IntegerField(default=0)
    last1dConsu   = models.IntegerField(default=0)


class CategoryData(models.Model):
    nameFr    = models.CharField(max_length=UserMaxSize, default="")
    nameEn    = models.CharField(max_length=UserMaxSize, default="")
    resumeFr  = models.TextField(default="")
    resumeEn  = models.TextField(default="")
    stat      = models.OneToOneField(CategoryStat, on_delete=models.CASCADE, primary_key=True)
    children  = models.ManyToManyField('self', related_name='ChildrenCategory')

    class Meta:
      abstract = True


class Category(CategoryData):
  pass


class CategoryUnactive(CategoryData):
  pass


""" --------------------------------------------------------------------------------------------------------------------
Localisation
-------------------------------------------------------------------------------------------------------------------- """


class LocalisationStat(models.Model):
    creationDate  = models.DateTimeField(default=datetime.datetime.now())
    creationUser  = models.CharField(max_length=UserMaxSize, default="creation")
    lastModDate   = models.DateTimeField(default=datetime.datetime.now())
    lastModUser   = models.CharField(max_length=UserMaxSize, default="")
    last1yConsu   = models.IntegerField(default=0)
    last1mConsu   = models.IntegerField(default=0)
    last1wConsu   = models.IntegerField(default=0)
    last1dConsu   = models.IntegerField(default=0)


class LocalisationCity(models.Model):
    name          = models.CharField(max_length=UserMaxSize)
    stat          = models.OneToOneField(LocalisationStat, on_delete=models.CASCADE, primary_key=True)


class LocalisationDepartment(models.Model):
    name          = models.CharField(max_length=UserMaxSize)
    code          = models.SmallIntegerField()
    children      = models.ManyToManyField(LocalisationCity)
    stat          = models.OneToOneField(LocalisationStat, on_delete=models.CASCADE, primary_key=True)


class LocalisationRegion(models.Model):
    name          = models.CharField(max_length=UserMaxSize)
    code          = models.SmallIntegerField()
    children      = models.ManyToManyField(LocalisationDepartment)
    stat          = models.OneToOneField(LocalisationStat, on_delete=models.CASCADE, primary_key=True)


class LocalisationCountry(models.Model):
    nameFr        = models.CharField(max_length=UserMaxSize)
    nameEn        = models.CharField(max_length=UserMaxSize)
    code          = models.CharField(max_length=3, unique=True)
    children      = models.ManyToManyField(LocalisationRegion)
    stat          = models.OneToOneField(LocalisationStat, on_delete=models.CASCADE, primary_key=True)


class LocalisationContinent(models.Model):
    nameFr        = models.CharField(max_length=UserMaxSize, unique=True)
    nameEn        = models.CharField(max_length=UserMaxSize, unique=True)
    code          = models.CharField(max_length=3, unique=True)
    children      = models.ManyToManyField(LocalisationCountry)
    stat          = models.OneToOneField(LocalisationStat, on_delete=models.CASCADE, primary_key=True)


""" --------------------------------------------------------------------------------------------------------------------
Payment
-------------------------------------------------------------------------------------------------------------------- """


class NLPurchase(models.Model):
    # 01, 02, 03, etc...
    level         = models.PositiveSmallIntegerField()
    quantity      = models.PositiveSmallIntegerField()


class PaypalPayment(models.Model):
    reference     = models.CharField(max_length=20)
    details       = models.TextField()


class Payment(models.Model):
    reference     = models.CharField(max_length=20)
    sum           = models.DecimalField(max_digits=7, decimal_places=2)
    purchase      = models.ForeignKey(NLPurchase, on_delete=models.CASCADE)

    UNKNOWN   = 'UN'
    GIFT      = 'GI'
    REFERENCE = 'RE'
    PAYPAL    = 'PP'
    TYPE_PAYMENT = ( (UNKNOWN   , 'null'     ),
                     (GIFT      , 'Gift'        ),
                     (REFERENCE , 'Reference'   ),
                     (PAYPAL    , 'Paypal'      )
                    )
    type          = models.CharField(max_length=2, choices=TYPE_PAYMENT, default=UNKNOWN)
    paypal        = models.ForeignKey(PaypalPayment, null=True, on_delete=models.CASCADE)


""" --------------------------------------------------------------------------------------------------------------------
Message
-------------------------------------------------------------------------------------------------------------------- """


class MessageHeader(models.Model):
    subject       = models.CharField(max_length=100)


class MessageData(models.Model):
    sender        = models.EmailField()
    recipient     = models.EmailField()
    datetime      = models.DateTimeField()
    content       = models.TextField()


class Message(models.Model):
    header        = models.OneToOneField(MessageHeader, on_delete=models.CASCADE, primary_key=True)
    messages      = models.ForeignKey(MessageData, on_delete=models.CASCADE)


""" --------------------------------------------------------------------------------------------------------------------
Notifications
-------------------------------------------------------------------------------------------------------------------- """


class NotificationCustomer(models.Model):
    UNKNOWN     = 'UN'
    MESSAGE     = 'NM'
    REPORT      = 'NR'
    OPINION     = 'NO'
    TITLE_POSSIBILITY = ( (UNKNOWN    , 'null'     ),
                          (MESSAGE    , 'New Message' ),
                          (REPORT     , 'New Report'  ),
                          (OPINION    , 'New Opinion' ),
                        )
    title         = models.CharField(max_length=2, choices=TITLE_POSSIBILITY, default=UNKNOWN)
    content       = models.TextField(max_length=50)


class NotificationAdmin(models.Model):
    UNKNOWN     = 'UN'
    MESSAGE     = 'NM'
    REPORT      = 'NR'
    VALIDATION  = 'NV'
    ERROR       = 'ER'
    TITLE_POSSIBILITY = ( (UNKNOWN    , 'null'         ),
                          (MESSAGE    , 'New Message'     ),
                          (REPORT     , 'New Report'      ),
                          (VALIDATION , 'New Validation'  ),
                          (ERROR      , 'New Error'       )
                        )
    title         = models.CharField(max_length=2, choices=TITLE_POSSIBILITY, default=UNKNOWN)
    content       = models.TextField(max_length=50)
    # TODO: Ajouter le lien à un compte ou une annonce


""" --------------------------------------------------------------------------------------------------------------------
Site
-------------------------------------------------------------------------------------------------------------------- """


# TODO: A compléter
class SiteStat(models.Model):
    creationDate  = models.DateTimeField(default=datetime.datetime.now())
    creationUser  = models.CharField(max_length=UserMaxSize, default="creation")
    lastModDate   = models.DateTimeField(default=datetime.datetime.now())
    lastModUser   = models.CharField(max_length=UserMaxSize, default="null")
    last1yConnect = models.IntegerField(default=0)
    last1mConnect = models.IntegerField(default=0)
    last1wConnect = models.IntegerField(default=0)
    last1dConnect = models.IntegerField(default=0)


class Opinion(models.Model):
    sender        = models.CharField(max_length=UserMaxSize, default="null")
    notes         = models.DecimalField(max_digits=3, decimal_places=2)
    text          = models.TextField()


class Report(models.Model):
  # TODO: A FAIRE
    # TODO: Lié user à un compte si possible
    # user          = models.ForeignKey(Account, null=True, on_delete=models.SET_NULL)
    pass


class Site(models.Model):
    title         = models.TextField(max_length=50)
    content       = models.TextField()
    link          = models.SlugField()
    nllevel       = models.PositiveSmallIntegerField(default=0)
    # pictures      = models.ForeignKey(models.ImageField(upload_to='site_pictures',
    #                                                         default='site_pictures/default/no_image.png'))
    category      = models.ForeignKey(Category, null=True, on_delete=models.SET_NULL)
    opinions      = models.ForeignKey(Opinion,  null=True, on_delete=models.CASCADE)
    report        = models.ForeignKey(Report,   null=True, on_delete=models.CASCADE)
    stat          = models.OneToOneField(SiteStat, on_delete=models.CASCADE, primary_key=True)


""" --------------------------------------------------------------------------------------------------------------------
Account
-------------------------------------------------------------------------------------------------------------------- """


# TODO: A compléter
class AccountStat(models.Model):
    creationDate  = models.DateTimeField(default=datetime.datetime.now())
    creationUser  = models.CharField(max_length=UserMaxSize, default="creation")
    lastModDate   = models.DateTimeField(default=datetime.datetime.now())
    lastModUser   = models.CharField(max_length=UserMaxSize, default="null")
    last1yConnect = models.IntegerField(default=0)
    last1mConnect = models.IntegerField(default=0)
    last1wConnect = models.IntegerField(default=0)
    last1dConnect = models.IntegerField(default=0)


class AccountData(models.Model):
    email         = models.EmailField(unique=True)
    id            = models.CharField(unique=True, max_length=30)
    #TODO: A changer pour le crypter
    password      = models.CharField(max_length=50)
    name          = models.CharField(max_length=50)
    familyname    = models.CharField(max_length=50)
    company       = models.CharField(max_length=50)
    #TODO: Créer les sites webs
    sites         = models.ForeignKey(Site, null=True, on_delete=models.CASCADE)
    messages      = models.ManyToManyField(Message)
    notification  = models.ForeignKey(NotificationCustomer, null=True, on_delete=models.CASCADE)
    stat          = models.OneToOneField(AccountStat, on_delete=models.CASCADE, primary_key=True)

    class Meta:
      abstract = True


# Correct account
class Account(AccountData):
  pass


# Account waiting to be validate with the email send to the address
class AccountUnvalidate(AccountData):
    # Link to validate the account (www.netliens.com/validate/XXXXXXXXXX)
    link          = models.CharField(max_length=10)


# Unactive Account
class AccountUnactive(AccountData):
    # Reason of unactive account (blocked, unactive, etc...)
    UNKNOWN   = 'UN'
    BLOCKED   = 'BL'
    UNACTIVE  = 'UA'
    UNACTIVE_REASON = ( (UNKNOWN,  'null'  ),
                        (BLOCKED,  'Blocked'  ),
                        (UNACTIVE, 'Unactive' )
                      )
    reason        = models.CharField(max_length=2, choices=UNACTIVE_REASON, default=UNKNOWN)
    details       = models.TextField()

