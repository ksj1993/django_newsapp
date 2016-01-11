from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import View
from .forms import ArticleForm, FollowForm, ProfileForm
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Article, UserProfile

import sys
from scraper import Scraper

def index(request):
	return render(request, 'core/index.html')


@login_required
def profile(request, profile_id):

	user_profile = User.objects.get(id = profile_id)
	user_articles = Article.objects.filter(user = user_profile)

	context = {
		'user_profile': user_profile,
		'user_articles': user_articles
	}
	return render(request, 'core/profile.html', context)

@login_required
def follow(request):
	if 'FollowSubmit' in request.POST:
		form = FollowForm(request.POST)
		if form.is_valid():
			new_followee = form.cleaned_data['followee']
			new_followee = User.objects.get(username = new_followee)
			if new_followee is not None:
				UserProfile.objects.get(user = request.user).follows.add(new_followee.userprofile)
   				return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
			return HttpResponse("error")
		else:
			#TODO errors
			pass

class DashboardView(View):
	template_name = 'core/dashboard.html'

	@method_decorator(login_required)
	def dispatch(self, *args, **kwargs):
		return super(DashboardView, self).dispatch(*args, **kwargs)

	def get(self, request, *args, **kwargs):
		my_articles = Article.objects.filter(user = request.user)
		followee_set = UserProfile.objects.get(user = request.user).follows.all()
		followee_set_users = [profile.user for profile in followee_set]

		# TODO change to distinct
		followee_articles = Article.objects.filter(user__in = followee_set_users)

		context = {
		'articleform': ArticleForm,
		'followform': FollowForm,
		'profileform': ProfileForm,
		'my_articles': my_articles,
		'followee_articles': followee_articles,
		'followees': followee_set
		}

		return render(request, self.template_name, context)

	def post(self, request, *args, **kwargs):
		print >> sys.stderr, request.POST

		if 'ArticleSubmit' in request.POST:
			form = ArticleForm(request.POST)
			if form.is_valid():
				new_article = form.save(commit=False)
				scraper = Scraper(new_article.url)
				new_article.user = request.user
				new_article.image, new_article.image_url = scraper.scrapeImage()
				new_article.title = scraper.scrapeTitle()
				new_article.site_name = scraper.scrapeSitename()
				new_article.description = scraper.scrapeDescr()

				new_article.save()
				return HttpResponseRedirect('/dashboard/')

			else:
				# TODO errors
				pass

		if 'ProfileSubmit' in request.POST:
			form = ProfileForm(request.POST)
			if form.is_valid():
				user_profile = form.cleaned_data['profile']
				user_profile = User.objects.get(username = user_profile)
				return HttpResponseRedirect("/profile/" + str(user_profile.id))
			else:
				return HttpResponse('error')
		return HttpResponse("Something went wrong")

