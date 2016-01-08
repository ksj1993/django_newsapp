from django.conf.urls import url
from . import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^dashboard/', views.DashboardView.as_view()),
]