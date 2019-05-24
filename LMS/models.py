from django.db import models
# Create your models here.


class UserBasicSetting(models.Model):
    type = models.CharField(max_length=20,primary_key=True)
    maxBook = models.IntegerField()
    maxDay = models.IntegerField()
    finePerDay = models.IntegerField()

    def __str__(self):
        return self.type


class Student(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=20,blank=True)

    settings = models.ForeignKey(UserBasicSetting,on_delete=models.ProtectedError)
    from django.contrib.auth.models import User

    account = models.OneToOneField(User,on_delete=models.DO_NOTHING,null=True,blank=True)

    def __str__(self):
        return self.name+"  "+str(self.id)


class Faculty(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=20,blank=True)
    isHOD = models.BooleanField(default=False)
    subject = models.CharField(max_length=20)
    settings = models.ForeignKey(UserBasicSetting,on_delete=models.ProtectedError)
    from django.contrib.auth.models import User

    account = models.OneToOneField(User,on_delete=models.DO_NOTHING,null=True,blank=True)

    def __str__(self):
        return self.name+"  "+str(self.id)


class ISBN(models.Model):
    isbn = models.IntegerField(primary_key=True)
    author = models.CharField(max_length=30)
    title = models.CharField(max_length=100)
    category = models.CharField(max_length=30)
    publisher = models.CharField(max_length=30)
    price = models.IntegerField()

    def __str__(self):
        return str(self.isbn)


class Book(models.Model):
    id = models.IntegerField(primary_key=True)
    details = models.ForeignKey(ISBN,on_delete=models.CASCADE)
    active = models.BooleanField(default=True)
    issued = models.BooleanField(default=False)

    def __str__(self):
        return self.details.title+"  "+str(self.id)


