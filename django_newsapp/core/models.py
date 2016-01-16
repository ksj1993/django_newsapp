from __future__ import unicode_literals
from django.db import models
from annoying.fields import AutoOneToOneField
from django.contrib.auth.models import User
from django.db.models.signals import post_save

class Article(models.Model):
	url = models.CharField(max_length=500)
	title = models.CharField(max_length= 300)
	image_url = models.CharField(max_length=500)
	image = models.ImageField(upload_to='images', blank=True)
	site_name = models.CharField(max_length=100)
	description = models.CharField(max_length=1000)
	real_pub_date = models.DateTimeField('real pub date')
	pub_date = models.DateField('date published')
	user = models.ForeignKey(User, on_delete=models.CASCADE)

class UserProfile(models.Model):
	user = AutoOneToOneField('auth.user')
	follows = models.ManyToManyField('UserProfile', related_name='followed_by')
	description = models.CharField(max_length=300)
	occupation = models.CharField(max_length= 100)

	def __unicode__(self):
		return self.user.username

class ArticleCount(models.Model):
	url = models.CharField(max_length=500)
	title = models.CharField(max_length= 300)
	image_url = models.CharField(max_length=500)
	image = models.ImageField(upload_to='images', blank=True)
	site_name = models.CharField(max_length=100)
	description = models.CharField(max_length=1000)

	count = models.IntegerField(default=0)


def create_user_profile(sender, instance, created, **kwargs):
	if created:
		UserProfile.objects.create(user=instance)

post_save.connect(create_user_profile, sender=User)
