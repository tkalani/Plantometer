from __future__ import unicode_literals
from django.db import models
from django import forms

#  REGISTERED  USERS  MODEL
class Users(models.Model):
	name = models.CharField(max_length=50)
	password = models.CharField(max_length=70)
	phone = models.CharField(max_length = 15, unique=True)
	address = models.CharField(max_length=150)
	currentplant = models.IntegerField(default = -1)

	def __str__(self):
		return self.name

#  DATABASES  OF  PLANTS  CONNECTED  WITH  IT'S  USERS 
class Plants(models.Model):
	userid = models.ForeignKey(Users, on_delete=models.CASCADE)
	plantname = models.CharField(max_length=50)
	latitude=models.CharField(default = '28.555576049185973',null=True, max_length=50)
	longitude = models.CharField(default = '77.16796875', null=True, max_length=50)
	actuatorstatus = models.IntegerField(default = 0)
	actuatorcontrol = models.IntegerField(default = 0)
	actuatorlink = models.CharField(max_length=200, default="-1")
	def __str__(self):
		return self.plantname
