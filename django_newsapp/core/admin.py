from django.contrib import admin
from .models import Article, UserProfile, ArticleCounts

# Register your models here.
admin.site.register(Article)
admin.site.register(UserProfile)
admin.site.register(ArticleCounts)
