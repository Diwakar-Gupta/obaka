from django.db import models
# Create your models here.


class UserBasicSetting(models.Model):
    type = models.CharField(max_length=20,primary_key=True)
    maxBook = models.IntegerField()
    maxDay = models.IntegerField()
    fineperDay = models.IntegerField()


class Student(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=20,blank=True)

    settings = models.ForeignKey(UserBasicSetting,on_delete=models.ProtectedError)
    from django.contrib.auth.models import User

    account = models.OneToOneField(User,on_delete=models.DO_NOTHING,null=True,blank=True)


class Faculty(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=20,blank=True)
    isHOD = models.BooleanField(default=False)
    subject = models.CharField(max_length=20)
    settings = models.ForeignKey(UserBasicSetting,on_delete=models.ProtectedError)
    from django.contrib.auth.models import User

    account = models.OneToOneField(User,on_delete=models.DO_NOTHING,null=True,blank=True)

