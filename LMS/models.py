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
    branch = models.CharField(max_length=20)

    from django.contrib.auth.models import User

    account = models.OneToOneField(User,on_delete=models.DO_NOTHING,null=True,blank=True)

    def __str__(self):
        return self.name+"  "+str(self.id)


class Faculty(models.Model):
    name = models.CharField(max_length=20,blank=True)
    isHOD = models.BooleanField(default=False)
    branch = models.CharField(max_length=20)
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
    quantity = models.PositiveIntegerField(default=0)
    count_issued = models.PositiveIntegerField(default=0)

    def __str__(self):
        return str(self.isbn)


class Book(models.Model):
    details = models.ForeignKey(ISBN,on_delete=models.CASCADE)
    active = models.BooleanField(default=True)
    is_issued = models.BooleanField(default=False)

    def __str__(self):
        return self.details.title+"  "+str(self.id)

    def delete(self, using=None, keep_parents=False):
        isbn = self.details
        isbn.quantity -= 1
        if self.is_issued:
            isbn.count_issued -= 1
        isbn.save()
        super(Book, self).delete(using=None, keep_parents=False)
        

class Issue(models.Model):
    book = models.ForeignKey(Book,models.CASCADE)

    member_type = models.ForeignKey(ContentType,on_delete=models.CASCADE)
    member_id = models.PositiveIntegerField()
    member = GenericForeignKey('member_type', 'member_id')

    checkoutfrom = models.CharField(max_length=20)
    is_returned = models.BooleanField(default=False)
    countrenewal = models.PositiveIntegerField(default=0)
    checkedout = models.DateTimeField(auto_now=True)
    date = models.DateTimeField(auto_now=True)
    return_date = models.DateTimeField(default=None,null=True)
    duedate = models.DateTimeField()
    mail_send = models.BooleanField(default=False)
    autorenew = models.BooleanField(default=False)

    def isLate(self):
        return self.lateby() > 0

    def lateby(self):
        returnday = self.return_date if self.return_date else datetime.now()
        days = (self.duedate - returnday).days
        if days < 0:
            days = 0
        return days

    def fine(self):
        return self.lateby()*self.member.settings.finePerDay

    def send_mail(self):
        pass

