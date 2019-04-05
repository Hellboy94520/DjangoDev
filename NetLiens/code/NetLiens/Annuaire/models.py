from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
import datetime

UserMaxSize     = 100
CategorySize    = 30
PaypalRefSize   = 20
SiteTitleSize   = 50

# Create your models here.

""" --------------------------------------------------------------------------------------------------------------------
Category
-------------------------------------------------------------------------------------------------------------------- """


class CategoryStat(models.Model):
    creationDate  = models.DateTimeField(default=datetime.datetime.now())
    creationUser  = models.CharField(max_length=CategorySize, default="creation")
    lastModDate   = models.DateTimeField(default=datetime.datetime.now())
    lastModUser   = models.CharField(max_length=CategorySize, default="")
    last1yConsu   = models.IntegerField(default=0)
    last1mConsu   = models.IntegerField(default=0)
    last1wConsu   = models.IntegerField(default=0)
    last1dConsu   = models.IntegerField(default=0)


class CategoryData(models.Model):
    nameFr    = models.CharField(max_length=UserMaxSize, default="")
    nameEn    = models.CharField(max_length=UserMaxSize, default="")
    resumeFr  = models.TextField(max_length=50, default="")
    resumeEn  = models.TextField(max_length=50, default="")
    stat      = models.OneToOneField(CategoryStat, on_delete=models.CASCADE, primary_key=True)
    children  = models.ManyToManyField('self', related_name='ChildrenCategory')

    class Meta:
      abstract = True


class Category(CategoryData):

    def __repr__(self):
        return "Category: {} - {}".format(self.nameFr, self.nameEn)


class CategoryUnactive(CategoryData):

    def __repr__(self):
        return "CategoryUnactive: {} - {}".format(self.nameFr, self.nameEn)


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

    def __repr__(self):
        return "LocalisationCity : {}".format(self.name)


class LocalisationDepartment(models.Model):
    name          = models.CharField(max_length=UserMaxSize)
    code          = models.SmallIntegerField()
    children      = models.ManyToManyField(LocalisationCity)
    stat          = models.OneToOneField(LocalisationStat, on_delete=models.CASCADE, primary_key=True)

    def __repr__(self):
        return "LocalisationDepartment : {}".format(self.name)


class LocalisationRegion(models.Model):
    name          = models.CharField(max_length=UserMaxSize)
    code          = models.SmallIntegerField()
    children      = models.ManyToManyField(LocalisationDepartment)
    stat          = models.OneToOneField(LocalisationStat, on_delete=models.CASCADE, primary_key=True)

    def __repr__(self):
        return "LocalisationRegion : {}".format(self.name)


class LocalisationCountry(models.Model):
    nameFr        = models.CharField(max_length=UserMaxSize)
    nameEn        = models.CharField(max_length=UserMaxSize)
    code          = models.CharField(max_length=3, unique=True)
    children      = models.ManyToManyField(LocalisationRegion)
    stat          = models.OneToOneField(LocalisationStat, on_delete=models.CASCADE, primary_key=True)

    def __repr__(self):
        return "LocalisationCountry : {} - {}".format(self.nameFr, self.nameEn)


class LocalisationContinent(models.Model):
    nameFr        = models.CharField(max_length=UserMaxSize, unique=True)
    nameEn        = models.CharField(max_length=UserMaxSize, unique=True)
    code          = models.CharField(max_length=3, unique=True)
    children      = models.ManyToManyField(LocalisationCountry)
    stat          = models.OneToOneField(LocalisationStat, on_delete=models.CASCADE, primary_key=True)

    def __repr__(self):
        return "LocalisationContinent : {} - {}".format(self.nameFr, self.nameEn)


""" --------------------------------------------------------------------------------------------------------------------
Payment
-------------------------------------------------------------------------------------------------------------------- """


class NLPurchase(models.Model):
    # 01, 02, 03, etc...
    level         = models.PositiveSmallIntegerField()
    quantity      = models.PositiveSmallIntegerField()

    def __repr__(self):
        return "NLPurchase : {} - {}".format(self.level, self.quantity)


class PaypalPayment(models.Model):
    reference     = models.CharField(max_length=PaypalRefSize)
    details       = models.TextField()

    def __repr__(self):
        return "PaypalPayment : {}".format(self.reference)


class Payment(models.Model):
    reference     = models.CharField(max_length=20)
    sum           = models.DecimalField(max_digits=7, decimal_places=2)
    purchase      = models.ForeignKey(NLPurchase, on_delete=models.CASCADE)

    UNKNOWN   = 'UN'
    GIFT      = 'GI'
    REFERENCE = 'RE'
    PAYPAL    = 'PP'
    TYPE_PAYMENT = ( (UNKNOWN   , 'null'        ),
                     (GIFT      , 'Gift'        ),
                     (REFERENCE , 'Reference'   ),
                     (PAYPAL    , 'Paypal'      )
                    )
    type          = models.CharField(max_length=2, choices=TYPE_PAYMENT, default=UNKNOWN)
    paypal        = models.ForeignKey(PaypalPayment, null=True, on_delete=models.CASCADE)

    def __repr__(self):
        return "Payment : type={} - reference={} - sum={}".format(self.type, self.reference, self.sum)


""" --------------------------------------------------------------------------------------------------------------------
Message
-------------------------------------------------------------------------------------------------------------------- """


class MessageHeader(models.Model):
    subject       = models.CharField(max_length=100)

    def __repr__(self):
        return "MessageHeader : {}".format(self.subject)


class MessageData(models.Model):
    sender        = models.EmailField()
    recipient     = models.EmailField()
    datetime      = models.DateTimeField()
    content       = models.TextField()

    def __repr__(self):
        return "MessageData : sendBy={}, recipient={}, date={}".format(self.sender, self.recipient, self.datetime)


class Message(models.Model):
    header        = models.OneToOneField(MessageHeader, on_delete=models.CASCADE, primary_key=True)
    messages      = models.ForeignKey(MessageData, on_delete=models.CASCADE)

    def __repr__(self):
        return "Message : {}".format(self.header)


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
                          (OPINION    , 'New Opinion' )
                        )

    title         = models.CharField(max_length=2, choices=TITLE_POSSIBILITY, default=UNKNOWN)
    content       = models.TextField(max_length=50, default="")

    def __repr__(self):
        return "NotificationCustomer : {} - {}".format(self.title, self.content)


class NotificationAdmin(models.Model):
    UNKNOWN     = 'UN'
    MESSAGE     = 'NM'
    REPORT      = 'NR'
    VALIDATION  = 'NV'
    ERROR       = 'ER'
    TITLE_POSSIBILITY = ( (UNKNOWN    , 'null'            ),
                          (MESSAGE    , 'New Message'     ),
                          (REPORT     , 'New Report'      ),
                          (VALIDATION , 'New Validation'  ),
                          (ERROR      , 'New Error'       )
                        )

    title         = models.CharField(max_length=2, choices=TITLE_POSSIBILITY, default=UNKNOWN)
    content       = models.TextField(max_length=50, default="")

    def __repr__(self):
        return "NotificationAdmin : {} - {}".format(self.title, self.content)


""" --------------------------------------------------------------------------------------------------------------------
Site
-------------------------------------------------------------------------------------------------------------------- """


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
    rate          = models.DecimalField(max_digits=3, decimal_places=2)
    content       = models.TextField(default="")

    def __repr__(self):
        return "Opinion : sendBy={}, rate={}, text={}".format(self.sender, self.rate, self.content)


class Report(models.Model):
    # TODO: A compléter selon ce qu'il est possible de reporter
    UNKNOWN     = 'UN'
    COPYRIGHT   = 'CO'
    TITLE_POSSIBILITY = ( (UNKNOWN      , 'null'        ),
                          (COPYRIGHT    , 'Copyright'   )
                        )
    sender        = models.CharField(max_length=UserMaxSize, default="null")
    title         = models.CharField(max_length=2, choices=TITLE_POSSIBILITY, default=UNKNOWN)
    content       = models.TextField(max_length=50)
    date          = models.DateTimeField(default=datetime.datetime.now())

    def __repr__(self):
        return "Report : sendBy={}, date={}, title={}, content={}".format(self.sender, self.date, self.title,
                                                                          self.content)


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
    
    def __repr__(self):
        return "Site : "


""" --------------------------------------------------------------------------------------------------------------------
Account
-------------------------------------------------------------------------------------------------------------------- """


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
    username      = models.CharField(unique=True, max_length=30)
    # TODO: A changer pour le crypter
    password      = models.CharField(max_length=50)
    name          = models.CharField(max_length=50)
    familyname    = models.CharField(max_length=50)
    company       = models.CharField(max_length=50)
    sites         = models.ForeignKey(Site, null=True, on_delete=models.CASCADE)
    messages      = models.ManyToManyField(Message)
    notification  = models.ForeignKey(NotificationCustomer, null=True, on_delete=models.CASCADE)
    payment       = models.ForeignKey(Payment, null=True, on_delete=models.CASCADE)
    stat          = models.OneToOneField(AccountStat, on_delete=models.CASCADE, primary_key=True)

    class Meta:
      abstract = True


# Correct account
class Account(AccountData):

    def __repr__(self):
        return "Account : {} - {}".format(self.email, self.username)


# Account waiting to be validate with the link sent to the address
class AccountUnvalidate(AccountData):
    # Link to validate the account (www.netliens.com/validate/XXXXXXXXXX)
    link          = models.CharField(max_length=10)

    def __repr__(self):
        return "AccountUnvalidate : {} - {} - {}".format(self.email, self.username, self.link)


# Unactive Account
class AccountUnactive(AccountData):
    # Reason of unactive account (blocked, unactive, etc...)
    UNKNOWN     = 'UN'
    BLOCKED     = 'BL'
    UNACTIVE    = 'UA'
    UNACTIVE_REASON = ( (UNKNOWN    , 'null'        ),
                        (BLOCKED    , 'Blocked'     ),
                        (UNACTIVE   , 'Unactive'    )
                      )

    reason        = models.CharField(max_length=2, choices=UNACTIVE_REASON, default=UNKNOWN)
    details       = models.TextField(max_length=50, default="")

    def __repr__(self):
        return "AccountUnactive : {} - {} - reason={}".format(self.email, self.username, self.reason)


class AccountAdmin(models.Model):
    # Administrator rules
    UNKNOWN     = 'UN'
    CONSULT     = 'CO'
    VALIDATION  = 'VA'
    ALL         = 'AL'
    ADMIN_STATUS    = ( (UNKNOWN    , 'null'        ),
                        (CONSULT    , 'Consult'     ),
                        (VALIDATION , 'Validation'  ),
                        (ALL        , 'All'         )
                      )

    email         = models.EmailField(unique=True)
    username      = models.CharField(unique=True, max_length=UserMaxSize)
    # TODO: A changer pour le crypter
    password      = models.CharField(max_length=50)
    status        = models.CharField(max_length=2, choices=ADMIN_STATUS, default=UNKNOWN)

    def __repr__(self):
        return "AccountAdmin : {} - {}".format(self.email, self.username, self.status)
