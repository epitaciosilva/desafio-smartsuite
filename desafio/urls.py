"""desafio URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path

from api.utils import include_api_urls, include_docs_urls

v1_api_urlpatterns = [
    path('', include_api_urls('v1', namespace='api')),
]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/docs/', include_docs_urls(
        {'title': 'Desafio API v1.0.0 ', 'patterns': v1_api_urlpatterns}
    )),
] + v1_api_urlpatterns
