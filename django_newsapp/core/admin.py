from django.contrib import admin
from .models import Article, UserProfile, ArticleCount

# Register your models here.
admin.site.register(Article)
admin.site.register(UserProfile)
admin.site.register(ArticleCount)