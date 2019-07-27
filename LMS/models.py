from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.urls import reverse
from datetime import datetime , timedelta ,timezone ,tzinfo , date
from django.core.exceptions import ObjectDoesNotExist
# Create your models here.


class UserBasicSetting(models.Model):
    type = models.CharField(max_length=20,primary_key=True)
    maxBook = models.PositiveSmallIntegerField()
    maxDay = models.IntegerField()
    finePerDay = models.IntegerField()

    def save(self):
        self.type = self.type.upper()
        super().save()

    def __str__(self):
        return self.type


class Student(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    name = models.CharField(max_length=20)
    count_issues = models.PositiveIntegerField(default=0)
    settings = models.ForeignKey(UserBasicSetting,on_delete=models.ProtectedError)
    active = models.BooleanField(default=True)
    email = models.EmailField(null=True)
    issued = models.PositiveIntegerField(default=0)
    fine = models.PositiveIntegerField(default=0)
    #attentionMessage = models.CharField(max_length=100,default='',null=True,blank=True)
    from django.contrib.auth.models import User

    account = models.OneToOneField(User,on_delete=models.DO_NOTHING,null=True,blank=True)

    def save(self):
        print('here')
        try :
            self.settings
        except ObjectDoesNotExist:
            self.settings = UserBasicSetting.objects.get(type='STUDENT')
        super().save()

    def get_absolute_url(self):
        return reverse('member-profile', kwargs={'membertype': 'STUDENT', 'memberpk': self.pk})

    def __str__(self):
        return self.name+"  "+str(self.id)


class Faculty(models.Model):
    name = models.CharField(max_length=20,)
    isHOD = models.BooleanField(default=False)
    count_issues = models.PositiveIntegerField(default=0)
    settings = models.ForeignKey(UserBasicSetting,on_delete=models.ProtectedError)
    active = models.BooleanField(default=True)
    email = models.EmailField(null=True)
    issued = models.PositiveIntegerField(default=0)
    fine = models.PositiveIntegerField(default=0)
    from django.contrib.auth.models import User

    account = models.OneToOneField(User,on_delete=models.DO_NOTHING,null=True,blank=True)

    def save(self):
        self.settings = UserBasicSetting.objects.get(type='FACULTY')
        super().save()

    def __str__(self):
        return self.name+"  "+str(self.id)

    def get_absolute_url(self):
        return reverse('member-profile', kwargs={'membertype': 'FACULTY', 'memberpk': self.pk})


class Date(models.Model):
    date = models.DateField(primary_key=True)

    def __str__(self):
        return str(self.date)

    @staticmethod
    def today():
        dat = Date.objects.get_or_create(date=date.today())
        if dat[1]:
            dat[0].save()
        return dat[0]


class Newspaper(models.Model):
    name = models.CharField(max_length=20)
    costPerDay = models.DecimalField(decimal_places=2,max_digits=5)
    language = models.CharField(max_length=10)
    present = models.ManyToManyField(Date)

    def __str__(self):
        return self.name + '('+self.language+')'

    def present_today(self):
        self.present.add(Date.today)        
        self.save()


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
    count_issues = models.PositiveIntegerField(default=0)

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
    return_date = models.DateTimeField(default=None,null=True)
    duedate = models.DateField()
    autorenew = models.BooleanField(default=False)

    def isLate(self):
        if self.is_returned:
            rd = self.return_date.date()
            return rd > self.duedate
        rd =  date.today()
        return rd > self.duedate

    def lateby(self):
        days=0
        if self.is_returned:
            rd = self.return_date.date()
            days = (rd - self.duedate).days
        else :
            rd = date.today()
            days = (rd - self.duedate).days
        if days < 0:
            days = 0
        return days

    def fine(self):
        return self.lateby()*self.member.settings.finePerDay

    def send_mail(self):
        pass

