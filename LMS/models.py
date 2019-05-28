from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from datetime import datetime , timedelta
# Create your models here.


class UserBasicSetting(models.Model):
    type = models.CharField(max_length=20)
    maxBook = models.PositiveSmallIntegerField()
    maxDay = models.IntegerField()
    finePerDay = models.IntegerField()

    def __str__(self):
        return self.type


class Student(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    name = models.CharField(max_length=20,blank=True)
    count_books = models.PositiveIntegerField(default=0)
    settings = models.ForeignKey(UserBasicSetting,on_delete=models.ProtectedError)
    active = models.BooleanField(default=True)
    from django.contrib.auth.models import User

    account = models.OneToOneField(User,on_delete=models.DO_NOTHING,null=True,blank=True)

    def __str__(self):
        return self.name+"  "+str(self.id)


class Faculty(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    name = models.CharField(max_length=20,blank=True)
    isHOD = models.BooleanField(default=False)
    subject = models.CharField(max_length=20)
    count_books = models.PositiveIntegerField(default=0)
    settings = models.ForeignKey(UserBasicSetting,on_delete=models.ProtectedError)
    active = models.BooleanField(default=True)
    from django.contrib.auth.models import User

    account = models.OneToOneField(User,on_delete=models.DO_NOTHING,null=True,blank=True)

    def __str__(self):
        return self.name+"  "+str(self.id)


class ISBN(models.Model):
    isbn = models.PositiveIntegerField(primary_key=True)
    author = models.CharField(max_length=30)
    title = models.CharField(max_length=100)
    category = models.CharField(max_length=30)
    publisher = models.CharField(max_length=30)
    price = models.PositiveIntegerField()

    def __str__(self):
        return str(self.isbn)


class Book(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    details = models.ForeignKey(ISBN,on_delete=models.CASCADE)
    active = models.BooleanField(default=True)
    is_issued = models.BooleanField(default=False)

    def __str__(self):
        return self.details.title+"  "+str(self.id)


class Issue(models.Model):
    book = models.ForeignKey(Book,models.CASCADE)
    member_type = models.ForeignKey(ContentType,on_delete=models.CASCADE)
    member_id = models.PositiveIntegerField()
    member = GenericForeignKey('member_type', 'member_id')

    is_returned=models.BooleanField(default=False)
    issue_day = models.DateTimeField(auto_now=True)
    return_day = models.DateTimeField(auto_now=True)
    mail_send = models.BooleanField(default=False)

    def isLate(self):
        return self.return_day > datetime.now() + timedelta(days=self.member.settings.maxDay)

    def lateby(self):
        if self.isLate():
            return (datetime.now() - self.return_day).days
        return 0

    def fine(self):
        return self.lateby()*self.member.settings.finePerDay

    def send_mail(self):
        pass