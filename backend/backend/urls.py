"""backend URL Configuration

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
from django.contrib import admin
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view

openapi_info = openapi.Info(
    title="Toolshed API",
    default_version='v1',
    description="API for all things …",
)

schema_view = get_schema_view(
    openapi_info,
    public=True,
    permission_classes=[],
)

urlpatterns = [
    path('djangoadmin/', admin.site.urls),
    path('auth/', include('authentication.api')),
    path('admin/', include('hostadmin.api')),
    path('api/', include('toolshed.api.friend')),
    path('api/', include('toolshed.api.inventory')),
    path('api/', include('toolshed.api.info')),
    path('api/', include('toolshed.api.files')),
    path('media/', include('files.media_urls')),
    path('docs/', schema_view.with_ui('swagger', cache_timeout=0), name='api-docs'),
]
