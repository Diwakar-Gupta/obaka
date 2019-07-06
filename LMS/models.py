from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.urls import reverse

from datetime import datetime , timedelta ,timezone ,tzinfo
# Create your models here.


class UserBasicSetting(models.Model):
    type = models.CharField(max_length=20,default="Custom")
    maxBook = models.PositiveSmallIntegerField()
    maxDay = models.IntegerField()
    finePerDay = models.IntegerField()

    def __str__(self):
        return self.type


class Student(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    name = models.CharField(max_length=20)
    count_books = models.PositiveIntegerField(default=0)
    settings = models.ForeignKey(UserBasicSetting,on_delete=models.ProtectedError)
    active = models.BooleanField(default=True)
    branch = models.CharField(max_length=20)

    from django.contrib.auth.models import User

    account = models.OneToOneField(User,on_delete=models.DO_NOTHING,null=True,blank=True)

    def get_absolute_url(self):
        return reverse('member-profile', kwargs={'membertype':'Student','memberpk':self.pk})

    def __str__(self):
        return self.name+"  "+str(self.id)


class Faculty(models.Model):
    name = models.CharField(max_length=20,)
    isHOD = models.BooleanField(default=False)
    branch = models.CharField(max_length=20)
    count_books = models.PositiveIntegerField(default=0)
    settings = models.ForeignKey(UserBasicSetting,on_delete=models.ProtectedError)
    active = models.BooleanField(default=True)
    from django.contrib.auth.models import User

    account = models.OneToOneField(User,on_delete=models.DO_NOTHING,null=True,blank=True)

    def __str__(self):
        return self.name+"  "+str(self.id)

    def get_absolute_url(self):
        return reverse('member-profile', kwargs={'membertype':'Faculty','memberpk':self.pk})



class ISBN(models.Model):
    isbn = models.PositiveIntegerField(primary_key=True)
    author = models.CharField(max_length=30)
    title = models.CharField(max_length=100)
    category = models.CharField(max_length=30)
    publisher = models.CharField(max_length=30)
    price = models.PositiveIntegerField(default=0)
    quantity = models.PositiveIntegerField(default=0)
    issued = models.PositiveIntegerField(default=0)
    deactive = models.PositiveIntegerField(default=0)

    def __str__(self):
        return str(self.isbn)

    def get_absolute_url(self):
        return reverse('books')


class Issue(models.Model):
    book = models.ForeignKey(ISBN,models.CASCADE)

    member_type = models.ForeignKey(ContentType,on_delete=models.CASCADE)
    member_id = models.PositiveIntegerField()
    member = GenericForeignKey('member_type', 'member_id')

    issuefrom = models.CharField(max_length=20)
    is_returned = models.BooleanField(default=False)
    countrenewal = models.PositiveIntegerField(default=0)
    issued_time = models.DateTimeField(auto_now=True)
    date = models.DateField(auto_now=True)
    return_date = models.DateField(default=None,null=True)
    duedate = models.DateField()
    mail_send = models.BooleanField(default=False)
    autorenew = models.BooleanField(default=False)
    forgetoverdue = models.BooleanField(default=False)

    def isLate(self):
        returnday = self.return_date if self.return_date else datetime.now()
        return returnday > self.duedate

    def lateby(self):
        returnday = self.return_date if self.return_date else datetime.now()
        days = (self.duedate - returnday).days
        if days < 0:
            days = 0
        return days

    def fine(self):
        if self.forgetoverdue:
            return 0
        return self.lateby()*self.member.settings.finePerDay

    def send_mail(self):
        pass

