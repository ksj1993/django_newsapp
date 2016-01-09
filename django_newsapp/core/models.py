from __future__ import unicode_literals
from django.db import models
from annoying.fields import AutoOneToOneField
from django.contrib.auth.models import User
from bs4 import BeautifulSoup
import requests
from django.core.files import File
import os, urllib
from django.core.files import File 

class Article(models.Model):
	url = models.CharField(max_length=100)
	image = models.ImageField(upload_to='images', blank=True)
	site_name = models.CharField(max_length=100)
	description = models.CharField(max_length=1000)
	user = models.ForeignKey(User, on_delete=models.CASCADE)

	

class UserProfile(models.Model):
	user = AutoOneToOneField('auth.user')
	follows = models.ManyToManyField('UserProfile', related_name='followed_by')

	def __unicode__(self):
		return self.user.username

