from django.conf.urls import url
from . import views
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^dashboard/', views.DashboardView.as_view()),
	url(r'^profile/', views.ProfileView.as_view()),
	url(r'^users/(?P<username>[A-Za-z0-9]+)/$', views.user),
	url(r'^users/(?P<username>[A-Za-z0-9]+)/(?P<request_type>.+)/$', views.user),
	url(r'^user/(?P<username>[A-Za-z0-9]+)/$', views.account),
	url(r'^delete/(?P<article_id>[0-9]+)/$', views.delete_article, name='delete'),
	url(r'^follow/(?P<username>.+)/$', views.follow, name='follow'),
	url(r'^create_article/', views.create_article),
	url(r'^account/', views.account),
	url(r'^discover/', views.DiscoverView.as_view()),
	url(r'^about/', views.about),
]
