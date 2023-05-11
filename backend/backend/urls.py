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

schema_view = get_schema_view(
    openapi.Info(
        title="Toolshed API",
        default_version='v1',
        description="API for all things …",
    ),
    public=True,
    permission_classes=[]
)

urlpatterns = [
    path('djangoadmin/', admin.site.urls),
    #path('api-auth/', include('rest_framework.urls')),
    path('admin/', include('hostadmin.api')),
    path('auth/', include('authentication.api')),
    path('api/', include('toolshed.inventory_api')),
    path('api/', include('toolshed.friend_api')),
    path('api/', include('toolshed.info_api')),
    path('docs/', schema_view.with_ui('swagger', cache_timeout=0), name='api-docs'),
]
