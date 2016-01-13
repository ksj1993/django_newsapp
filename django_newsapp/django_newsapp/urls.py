from django.conf import settings
from django.conf.urls import url, include
from django.contrib import admin
from django.conf.urls.static import static

urlpatterns = [
	url(r'^admin/', admin.site.urls),
	url(r'^', include('core.urls')),
	url(r'^accounts/', include('allauth.urls')),
]  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
