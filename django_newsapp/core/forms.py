from django import forms
from django.forms import ModelForm
from .models import Article

class ArticleForm(ModelForm):
	class Meta:
		model = Article
		fields = ['url']
	
class FollowForm(forms.Form):
	followee = forms.CharField(label='Enter a user to follow', max_length=100)

class SignupForm(forms.Form):
	first_name = forms.CharField(max_length=30, label='First Name', widget=forms.TextInput(attrs={'placeholder': 'First Name'}))
	last_name = forms.CharField(max_length=30, label='Last Name', widget=forms.TextInput(attrs={'placeholder': 'Last Name'}))

	def signup(self, request, user):
		user.first_name = self.cleaned_data['first_name']
		user.last_name = self.cleaned_data['last_name']
		user.save()

class ProfileForm(forms.Form):
	profile = forms.CharField(label='Search for user', max_length=100)


