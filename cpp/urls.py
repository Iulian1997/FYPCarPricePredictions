from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', include('pages.urls')),
    path('accounts/', include('accounts.urls')),
    path('admin/', admin.site.urls),
] + static(settings.MEDIA_URL, documnet_root=settings.MEDIA_ROOT)
