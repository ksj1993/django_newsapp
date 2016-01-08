from __future__ import unicode_literals
from django.db import models
from annoying.fields import AutoOneToOneField
from django.contrib.auth.models import User



class Article(models.Model):
	url_link = models.CharField(max_length=100, blank=False)
	user = models.ForeignKey(User, on_delete=models.CASCADE)

class UserProfile(models.Model):
	user = AutoOneToOneField('auth.user')
	follows = models.ManyToManyField('UserProfile', related_name='followed_by')

	def __unicode__(self):
		return self.user.username