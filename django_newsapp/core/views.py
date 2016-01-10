from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import View
from .forms import ArticleForm, FollowForm
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Article, UserProfile
import sys
from scraper import Scraper

def index(request):
	return render(request, 'core/index.html')

def follow(request):
	pass



class DashboardView(View):
	template_name = 'core/dashboard.html'

	@method_decorator(login_required)
	def dispatch(self, *args, **kwargs):
		return super(DashboardView, self).dispatch(*args, **kwargs)

	def get(self, request, *args, **kwargs):
		articles = Article.objects.filter(user = request.user)
		followee_set = UserProfile.objects.get(user = request.user).follows.all()
		followee_set_users = [profile.user for profile in followee_set]
		articles = Article.objects.filter(user__in = followee_set_users)

		context = {
		'articleform': ArticleForm,
		'followform': FollowForm,
		'articles': articles,
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

		if 'FollowSubmit' in request.POST:
			form = FollowForm(request.POST)
			if form.is_valid():
				new_followee = form.cleaned_data['followee']
				new_followee = User.objects.get(username = new_followee)
				if new_followee is not None:
					UserProfile.objects.get(user = request.user).follows.add(new_followee.userprofile)
					return HttpResponseRedirect('/dashboard/')

				return HttpResponse("error")
			else:
				#TODO errors
				pass

		return HttpResponse('error')

