from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.http import HttpResponseRedirect
from django.urls import path, include

urlpatterns = [
    path('', lambda r: HttpResponseRedirect('winereviews/')),
    path('admin/', admin.site.urls),
    path('winereviews/', include('winereviews.urls')),
]