from django import forms

class PostForm(forms.Form):
	link_url = forms.CharField(label='Share a link', max_length=100)

	