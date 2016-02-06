from __future__ import unicode_literals
from django.db import models
from annoying.fields import AutoOneToOneField
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from pygments.lexers import get_all_lexers
from pygments.styles import get_all_styles

LEXERS = [item for item in get_all_lexers if item[1]]
LANGUAGE_CHOICES = sorted([(item[1][0], item[0]) for item in LEXERS])
STYLE_CHOICES = sorted((item, item) for item in get_all_styles())


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

	class Meta:
		ordering = ('real_pub_date',)

class UserProfile(models.Model):
	user = AutoOneToOneField('auth.user')
	profile_picture = models.ImageField(upload_to='images', default = 'default.png', blank=True)
	follows = models.ManyToManyField('UserProfile', related_name='followed_by')
	description = models.CharField(max_length=300, default='')
	occupation = models.CharField(max_length= 100, default='')

	def __unicode__(self):
		return self.user.username

def create_user_profile(sender, instance, created, **kwargs):
	if created:
		UserProfile.objects.create(user=instance)

post_save.connect(create_user_profile, sender=User)
