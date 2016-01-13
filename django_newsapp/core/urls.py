from django.conf.urls import url
from . import views
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^dashboard/', views.DashboardView.as_view()),
	url(r'^profile/', views.ProfileView.as_view()),
	url(r'^users/(?P<user_id>[0-9]+)/$', views.user, name='user'),
	url(r'^delete/(?P<article_id>[0-9]+)/$', views.delete_article, name='delete'),
	url(r'^create_article/', views.create_article),
	url(r'^discover/', views.DiscoverView.as_view()),
]
