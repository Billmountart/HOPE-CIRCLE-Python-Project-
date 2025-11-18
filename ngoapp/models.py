from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class Logintbl(AbstractUser):
    usertype=models.CharField(max_length=50)

class Ngo(models.Model):
    user=models.ForeignKey(Logintbl,on_delete=models.CASCADE)
    name=models.CharField(max_length=50)
    email=models.CharField(max_length=50)
    phone=models.BigIntegerField()
    lisence = models.FileField(null=True)
    logo = models.FileField(null=True)
    address =models.CharField(max_length=200)

class Volunteer(models.Model):
    user=models.ForeignKey(Logintbl,on_delete=models.CASCADE)
    name=models.CharField(max_length=50)
    email=models.CharField(max_length=50)
    phone=models.BigIntegerField()
    cv = models.FileField(null=True)
    photo = models.FileField(null=True)
    address =models.CharField(max_length=200)

class Donor(models.Model):
    user=models.ForeignKey(Logintbl,on_delete=models.CASCADE)
    name=models.CharField(max_length=50)
    email=models.CharField(max_length=50)
    phone=models.BigIntegerField()
    photo = models.FileField(null=True)
    address =models.CharField(max_length=200)

class Activity(models.Model):
    ngo=models.ForeignKey(Ngo,on_delete=models.CASCADE)
    name=models.CharField(max_length=50)
    category=models.CharField(max_length=50,null=True)
    description=models.TextField()
    loc=models.CharField(max_length=200)
    volunteers_needed=models.IntegerField()
    sDate=models.DateField()
    eDate=models.DateField()

class VolunteerActivity(models.Model):
    volunteer=models.ForeignKey(Volunteer,on_delete=models.CASCADE)
    activity=models.ForeignKey(Activity,on_delete=models.CASCADE)
    status=models.CharField(max_length=20,default="Requested")


class Subscribe(models.Model):
    vol=models.ForeignKey(Volunteer,on_delete=models.CASCADE, null=True)
    ngo=models.ForeignKey(Ngo,on_delete=models.CASCADE)
    don=models.ForeignKey(Donor,on_delete=models.CASCADE, null=True)
    status=models.CharField(max_length=20)
    date=models.DateField(auto_now_add=True)

class Donations(models.Model):
    donor=models.ForeignKey(Donor,on_delete=models.CASCADE)
    activity=models.ForeignKey(Activity,on_delete=models.CASCADE)
    amount=models.IntegerField()
    ngodon=models.IntegerField(default=0)
    fee=models.IntegerField(default=0)
    date=models.DateField(auto_now_add=True)
    time=models.TimeField(auto_now_add=True,null=True)

class ChatbotQA(models.Model):
    keyword = models.CharField(max_length=255, help_text="Use commas to separate multiple keywords, e.g. donate, donation")
    answer = models.TextField()

    def __str__(self):
        return self.keyword
    
class Blog(models.Model):
    title=models.CharField(max_length=100)
    description=models.CharField(max_length=255)
    ngo=models.ForeignKey(Ngo,on_delete=models.CASCADE)
    date=models.DateField(auto_now_add=True)

class Image(models.Model):
    blog=models.ForeignKey(Blog,on_delete=models.CASCADE)
    image=models.ImageField(null=True)
