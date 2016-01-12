from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import View
from .forms import ArticleForm, FollowForm, ProfileForm
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Count
from .models import Article, UserProfile, ArticleCount
from django.utils.html import escape
import sys, json, datetime
from scraper import Scraper
from django.utils import timezone

def index(request):
	return render(request, 'core/index.html')

@login_required
def create_article(request):
	print >> sys.stderr, "CREATING ARTICLE"
	if request.method == 'POST':
		
		form = ArticleForm(request.POST)

		if form.is_valid():
			
			# Create new article
			new_article = form.save(commit=False)
			scraper = Scraper(new_article.url)
			new_article.user = request.user
			new_article.image, new_article.image_url = scraper.scrapeImage()
			new_article.title = scraper.scrapeTitle()
			new_article.site_name = scraper.scrapeSitename()
			new_article.description = scraper.scrapeDescr()
			new_article.pub_date = timezone.now()
			new_article.save()

			# Update article count

			article_count, created = ArticleCount.objects.get_or_create(url=new_article.url)
			if created:
				article_count.title = new_article.title
				article_count.image_url = new_article.image_url
				article_count.image = new_article.image
				article_count.site_name = new_article.site_name
				article_count.description = new_article.description
				article_count.count = 1
			else:
				article_count.count += 1

			article_count.save()


			response_data = {
				'article_url': new_article.url,
				'article_image': new_article.image.url,
				'article_title': new_article.title,
				'article_site_name': new_article.site_name,
				'article_user': new_article.user.username,
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
		my_articles = Article.objects.filter(user = request.user).all().order_by('-pub_date')

		if my_articles:	
			context = {
				'form': ArticleForm,
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
		print >> sys.stderr, "POSTING NEW ARTICLE"
		if form.is_valid():
			new_article = form.save(commit=False)
			scraper = Scraper(new_article.url)
			new_article.user = request.user
			new_article.image, new_article.image_url = scraper.scrapeImage()
			new_article.title = scraper.scrapeTitle()
			new_article.site_name = scraper.scrapeSitename()
			new_article.description = scraper.scrapeDescr()
			new_article.pub_date = timezone.now()
			new_article.save()

			return HttpResponseRedirect('/profile/')
		return HttpResponse("Error")



@login_required
def user(request, user_id):

	user_profile = User.objects.get(id = user_id)
	user_articles = Article.objects.filter(user = user_profile).all()

	context = {
		'user_profile': user_profile,
		'user_articles': user_articles
	}

	return render(request, 'core/user.html', context)


class DiscoverView(View):
	template_name = 'core/discover.html'

	@method_decorator(login_required)
	def dispatch(self, *args, **kwargs):
		return super(DiscoverView, self).dispatch(*args, **kwargs)

	def get(self, request, *args, **kwargs):

		#top_articles = ArticleCount.objects.all().order_by('-count')
		date_from = datetime.datetime.now() - datetime.timedelta(days=1)
		
		top_articles = Article.objects.filter(pub_date__gte=date_from).values('url').annotate(count=Count("url")).order_by('-count')[:20].values('url')
		top_articles_inc = Article.objects.filter(url__in = top_articles).distinct('url')
		print >> sys.stderr, top_articles
		print >> sys.stderr, top_articles_inc
		context = {
			'top_articles': top_articles_inc,
		}
		# TODO top users
		
		return render(request, self.template_name, context)


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


