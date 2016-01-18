from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.views.generic import View
from .forms import ArticleForm, FollowForm, ProfileForm
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Count
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Article, UserProfile, ArticleCount
from django.utils.html import escape
import sys, json, datetime
from scraper import Scraper
from django.utils import timezone
from datetime import date
import datetime
from urlparse import urlparse
import helper

def index(request):
	return render(request, 'core/index.html')

def about(request):
	return render(request, 'core/about.html')

@login_required
def create_article(request):
	
	if request.method == 'POST':
		
		form = ArticleForm(request.POST)

		if form.is_valid():
			
			try:
				# Check if user has already posted this article
				if not Article.objects.filter(user = request.user, url = form.cleaned_data['url']):
				
					print >> sys.stderr, "CREATING NEW ARTICLE"
					# Else create new article
					new_article = form.save(commit=False)

					cleaner = urlparse(new_article.url)
					cleaned_url = "http://" + cleaner.netloc + cleaner.path			
					new_article.url = cleaned_url

					# scape info from URL
					scraper = Scraper(new_article.url)
					new_article.user = request.user
					new_article.image, new_article.image_url = scraper.scrapeImage()
					new_article.title = scraper.scrapeTitle()
					new_article.site_name = scraper.scrapeSitename()
					new_article.description = scraper.scrapeDescr()
					new_article.pub_date = date.today()
					new_article.real_pub_date = timezone.now()
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

					# adjust date
					article_date = datetime.datetime.strptime(str(new_article.pub_date), '%Y-%m-%d').strftime('%b %d, %Y')

					response_data = {
						'article_id': new_article.id,
						'article_url': new_article.url,
						'article_image': new_article.image.url,
						'article_title': new_article.title,
						'article_site_name': new_article.site_name,
						'article_user': new_article.user.username,
						'article_user_id': new_article.user.id,
						'article_description': new_article.description,
						'article_pub_date': article_date,
					}

					# Success
					return HttpResponse(
						json.dumps(response_data),
						content_type="application/json"
					)

				response_data = {'Error': 'You have already posted this article'}
				return HttpResponse(
					json.dumps(response_data),
					content_type="application/json"
				)
			
			except:
				print >> sys.stderr, "ERROR IN SCRAPER"
				response_data = {'Error': 'Error posting link. Please try again'}
				return HttpResponse(
					json.dumps(response_data),
					content_type="application/json"
				)
		else:
			print >> sys.stderr, "FORM IS NOT VALID"
			response_data = {'Error': 'Error posting link. Please try again'}
			return HttpResponse(
				json.dumps(response_data),
				content_type="application/json"
			)
	else:
		print >> sys.stderr, "NOT POST REQUEST"
		response_data = {'Error': 'Error posting link. Please try again'}
		return HttpResponse(
			json.dumps(response_data),
			content_type="application/json"
		)


@login_required
def delete_article(request, article_id):
	article = Article.objects.filter(id=article_id).first()
	if not article or article.user != request.user:
		raise Http404("Cannot delete article")

	try:
		Article.objects.get(id = article_id, user=request.user).delete()
		response_data = {'Success': 'Article deleted'}
		return HttpResponse(
			json.dumps(response_data),
			content_type="application/json"
		)
	except:
		response_data = {'Error': 'Could not delete article. Please try again later'}
		return HttpResponse(
			json.dumps(response_data),
			content_type="application/json"
		)

@login_required
def follow(request, username):
	new_followee = User.objects.filter(username = username).first()
	if not new_followee:
		raise Http404("Cannot follow user")
	'''try:'''
	if not UserProfile.objects.get(user = request.user).follows.values().filter(id = new_followee.userprofile.id).first():
		UserProfile.objects.get(user = request.user).follows.add(new_followee.userprofile)
		return HttpResponse("Success")
	else:
		response_data = {'Error': 'You are already following that user.'}
		return HttpResponse(
			json.dumps(response_data),
			content_type="application/json"
		)
'''
	except:
		response_data = {'Error': 'Could not follow user. Please try again later'}
		return HttpResponse(
			json.dumps(response_data),
			content_type="application/json"
		)
	'''

class ProfileView(View):
	template_name = 'core/profile.html'

	@method_decorator(login_required)
	def dispatch(self, *args, **kwargs):
		return super(ProfileView, self).dispatch(*args, **kwargs)

	def get(self, request, *args, **kwargs):
		

		my_profile = UserProfile.objects.get(user = request.user)
		my_articles = Article.objects.filter(user = request.user).all().order_by('-real_pub_date')


		if my_articles:	

			paginator = Paginator(my_articles, 20)
			page = request.GET.get('page')

			try: 
				articles = paginator.page(page)
			except PageNotAnInteger:
				articles = paginator.page(1)
			except EmptyPage:
				articles = paginator.page(paginator.num_pages)
			context = {
				'form': ArticleForm,
				'my_profile': my_profile,
				'my_articles': articles	
			}
			return render(request, self.template_name, context)
		else:
			# return discovery stuff
			context = {

			}
			# for now
			return render(request, self.template_name, context)

	def post(self, request, *args, **kwargs):
		return HttpResponseRedirect('/profile/')
	

@login_required
def user(request, username, request_type="articles"):
	user_info = User.objects.filter(username = username).first()

	if user_info is not None:
		user_profile = UserProfile.objects.get(user = request.user)
		if request_type == "articles":
			user_articles = Article.objects.filter(user = user_info).all()
			if user_articles:
				paginator = Paginator(user_articles, 15)
				page = request.GET.get('page')

				try: 
					articles = paginator.page(page)
				except PageNotAnInteger:
					articles = paginator.page(1)
				except EmptyPage:
					articles = paginator.page(paginator.num_pages)


				context = {
					'user_info': user_info,
					'user_profile': user_profile,
					'user_articles': articles
				}
				return render(request, 'core/user.html', context)
			else:
				pass

		elif request_type == "followers":
			follower_set = UserProfile.objects.get(user__username = username).followed_by.all()
			context = {
				'user_info': user_info,
				'user_profile': user_profile,
				'user_followers': follower_set
			}
			return render(request, 'core/user.html', context)


		elif request_type == "following":
			followee_set = UserProfile.objects.get(user__username = username).follows.all()

			context = {
				'user_info': user_info,
				'user_profile': user_profile,
				'user_following': followee_set
			}
			return render(request, 'core/user.html', context)

		else:
			raise Http404("Invalid page")
	else:
		raise Http404("Cannot find user")



@login_required
def account(request):
	user = request.user
	return HttpResponse(user.username)


class DiscoverView(View):
	template_name = 'core/discover.html'

	@method_decorator(login_required)
	def dispatch(self, *args, **kwargs):
		return super(DiscoverView, self).dispatch(*args, **kwargs)

	def get(self, request, *args, **kwargs):

		date_from = datetime.datetime.now() - datetime.timedelta(days=1)
				
		#top_articles = Article.objects.filter(pub_date__gte=date_from).exclude(user = request.user).values('url').annotate(count=Count("url")).order_by('-count')[:20].values('url')
		#top_articles_inc = Article.objects.filter(url__in = top_articles).distinct('url')
		
		# For now, top users will be most followed
		# in the future, change this:

		#pub_date__gte=date_from << add in filter
		top_articles = Article.objects.filter().exclude(user = request.user).values().annotate(count=Count("url")).order_by('-count')
		top_users = UserProfile.objects.all().exclude(followed_by = request.user.userprofile).values("user__username", "id").annotate(followed_by_count = Count("followed_by")).order_by("-followed_by_count")[:20]
		
		#print >> sys.stderr, top_users

		if top_articles:	

			paginator = Paginator(top_articles, 8)
			page = request.GET.get('page')

			try: 
				articles = paginator.page(page)
			except PageNotAnInteger:
				articles = paginator.page(1)
			except EmptyPage:
				articles = paginator.page(paginator.num_pages)
			context = {
				'top_articles': articles,
				'top_users': top_users,	
			}
			return render(request, self.template_name, context)
		else:
			# return discovery stuff
			context = {

			}
			# for now
			return render(request, self.template_name, context)


		

		context = {
			'top_articles': top_articles,
			'top_users': top_users,
		}
		# TODO top users
		
		return render(request, self.template_name, context)



class DashboardView(View):
	template_name = 'core/dashboard.html'

	@method_decorator(login_required)
	def dispatch(self, *args, **kwargs):
		return super(DashboardView, self).dispatch(*args, **kwargs)

	def get(self, request, *args, **kwargs):
		followee_set = UserProfile.objects.get(user = request.user).follows.all()
		followee_set_users = [profile.user for profile in followee_set]

		# TODO change to distinct
		followee_articles = Article.objects.filter(user__in = followee_set_users).all()

		if followee_articles:
			paginator = Paginator(followee_articles, 20)
			page = request.GET.get('page')

			try: 
				articles = paginator.page(page)
			except PageNotAnInteger:
				articles = paginator.page(1)
			except EmptyPage:
				articles = paginator.page(paginator.num_pages)
			context = {
				'followee_articles': articles	
			}
			return render(request, self.template_name, context)
		else:
			# return discovery stuff
			context = {

			}
			# for now
			return render(request, self.template_name, context)


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


