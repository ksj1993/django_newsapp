from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import View
from .forms import ArticleForm
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from bs4 import BeautifulSoup
from .models import Article

def index(request):
	return render(request, 'core/index.html')

class DashboardView(View):
	form_class = ArticleForm
	template_name = 'core/dashboard.html'

	@method_decorator(login_required)
	def dispatch(self, *args, **kwargs):
		return super(DashboardView, self).dispatch(*args, **kwargs)

	def get(self, request, *args, **kwargs):
		articles = Article.objects.filter(user = request.user)
		context = {
		'form': ArticleForm,
		'articles': articles
		}
		return render(request, self.template_name, context)

	def post(self, request, *args, **kwargs):
		form = self.form_class(request.POST)
		if form.is_valid():
			new_article = form.save(commit=False)
			new_article.user = request.user
			new_article.save()

			return HttpResponse("Success")
		forms.errors.as_data()

		return render(request, self.template_name, {'form': form_class})

