"""
URLs for videofront
"""
from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView

from api import urls as api_urls

urlpatterns = [
    path("", RedirectView.as_view(pattern_name="api:v1:api-root"), name="home"),
    path("api/", include((api_urls, "api"))),
    path("admin/", admin.site.urls),
]
