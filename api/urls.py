"""
Url definitions for the Video Front API.
Just including routes for all versions of the API
"""
from django.urls import include, path

from api.v1 import urls as api_v1_urls

urlpatterns = [path("v1/", include((api_v1_urls, "v1")))]
