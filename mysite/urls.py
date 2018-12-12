from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.http import HttpResponseRedirect
from django.urls import path, include

# Use static() to add url mapping to serve static files during development (only)

urlpatterns = [
    url(r'^$', lambda r: HttpResponseRedirect('winereviews/')),
    url(r'^admin/', admin.site.urls),
    url(r'^winereviews/', include('winereviews.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
