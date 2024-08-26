"""
URL configuration for imageTaskAPI project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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

from debug_toolbar.toolbar import debug_toolbar_urls
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from tasks.authentication import EnvironmentBasicAuthentication

schema_view = get_schema_view(
    openapi.Info(
        title="Task Service API",
        default_version="v1",
        description="API для управления задачами и изображениями",
        terms_of_service="https://www.google.com/policies/terms/",
        license=openapi.License(name="BSD License"),
    ),
    permission_classes=[
        permissions.AllowAny,
    ],
    public=True,
    authentication_classes=[
        EnvironmentBasicAuthentication,
    ],
)
urlpatterns = (
    [
        path("admin/", admin.site.urls),
        path("api/", include("tasks.urls")),
        path(
            "swagger/",
            schema_view.with_ui("swagger", cache_timeout=0),
            name="swagger-ui",
        ),
        path(
            "swagger.json", schema_view.without_ui(cache_timeout=0), name="schema-json"
        ),
    ]
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    + debug_toolbar_urls()
)
