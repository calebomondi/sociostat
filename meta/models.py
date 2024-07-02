from django.db import models

# Create your models here.
class UsrCredentials(models.Model):
    email = models.EmailField()
    llat = models.CharField(max_length=500) #long lived access token
    pgat = models.CharField(max_length=500) #fb page access token
    iguserid = models.IntegerField()
    fbpageid = models.IntegerField()
    appid = models.IntegerField()
    appsecret = models.CharField(max_length=200)

class Followers(models.Model):
    email = models.EmailField()
    igfollowers = models.IntegerField()
    fbfollowers = models.IntegerField()