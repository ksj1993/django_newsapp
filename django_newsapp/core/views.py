from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import View
from .forms import PostForm
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required


def index(request):
	return render(request, 'core/index.html')

class DashboardView(View):
	form_class = PostForm
	template_name = 'core/dashboard.html'

	@method_decorator(login_required)
	def dispatch(self, *args, **kwargs):
		return super(DashboardView, self).dispatch(*args, **kwargs)

	def get(self, request, *args, **kwargs):
		return render(request, self.template_name, {'form': PostForm})

	def post(self, request, *args, **kwargs):
		form = self.form_class(request.POST)
		if form.is_valid():
			# <process form cleaned data>
			return HttpResponse("Success")


		return render(request, self.template_name, {'form': form})

