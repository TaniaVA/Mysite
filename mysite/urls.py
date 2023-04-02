"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.views.i18n import JavaScriptCatalog
from django.conf.urls.static import serve

urlpatterns = [
    path('schedule/', include('schedule.urls')),
    path('admin/', admin.site.urls),
    path('accounts/', include("accounts.urls")),
    path('accounts/', include("django.contrib.auth.urls")),
    path('appointments/', include('appointments.urls')),
    path('blog/', include('blog.urls')),
    path('', include('frontend.urls')),
    path('jsi18n/', JavaScriptCatalog.as_view(), name='javascript-catalog'),
]

if settings.DEBUG:
    urlpatterns += [
        path('static/<path:path>', serve, {'document_root': settings.STATIC_ROOT}),
        path('media/<path:path>', serve, {'document_root': settings.MEDIA_ROOT}),
    ]
