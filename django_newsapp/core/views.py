from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import View
from .forms import ArticleForm, FollowForm, ProfileForm
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Article, UserProfile
from django.utils.html import escape
from django.utils.html import escape
import sys, json
from scraper import Scraper

def index(request):
	return render(request, 'core/index.html')

@login_required
def create_article(request):
	if request.method == 'POST':
		
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
	

			response_data = {
				'article_url': new_article.url,
				'article_image': new_article.image.url,
				'article_title': new_article.title,
				'article_site_name': new_article.site_name,
				'article_user': new_article.user,
				'article_user_id': new_article.user.id,
				'article_description': new_article.description,
			}

			return HttpResponse(
				json.dumps(response_data),
				content_type="application/json"
			)
		else:
			# TODO errors
			return HttpResponse(
			json.dumps({"Error": "error"}),
			content_type="application/json"
		)
	else:
		# TODO errors
		return HttpResponse(
			json.dumps({"Error": "error"}),
			content_type="application/json"
		)


@login_required
def delete_article(request, article_id):
	if request.method == 'POST':
		Article.objects.get(id = article_id).delete()
		return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

class ProfileView(View):
	template_name = 'core/profile.html'

	@method_decorator(login_required)
	def dispatch(self, *args, **kwargs):
		return super(ProfileView, self).dispatch(*args, **kwargs)

	def get(self, request, *args, **kwargs):
		my_profile = UserProfile.objects.get(user = request.user)
		my_articles = Article.objects.filter(user = request.user).all()[:20]

		if my_articles:	
			context = {
				'my_profile': my_profile,
				'my_articles': my_articles	
			}
			return render(request, self.template_name, context)
		else:
			# return discovery stuff
			context = {

			}
			# for now
			return render(request, self.template_name, context)

	def post(self, request, *args, **kwargs):
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

			return HttpResponseRedirect('/profile/')
		return HttpResponse("Error")



@login_required
def user(request, user_id):

	user_profile = User.objects.get(id = user_id)
	user_articles = Article.objects.filter(user = user_profile).all()[:20]

	context = {
		'user_profile': user_profile,
		'user_articles': user_articles
	}

	return render(request, 'core/user.html', context)
	

def discover(request):
	# TODO top articles
	# TODO top users
	pass

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
		followee_set = UserProfile.objects.get(user = request.user).follows.all()
		followee_set_users = [profile.user for profile in followee_set]

		# TODO change to distinct
		followee_articles = Article.objects.filter(user__in = followee_set_users).all()[:20]

		context = {
		'followee_articles': followee_articles,
		'followees': followee_set
		}

		return render(request, self.template_name, context)



	def post(self, request, *args, **kwargs):

		if 'ProfileSubmit' in request.POST:
			form = ProfileForm(request.POST)
			if form.is_valid():
				user_profile = form.cleaned_data['profile']
				user_profile = User.objects.get(username = user_profile)
				return HttpResponseRedirect("/user/" + str(user_profile.id))
			else:
				return HttpResponse('error')
		return HttpResponse("Something went wrong")


