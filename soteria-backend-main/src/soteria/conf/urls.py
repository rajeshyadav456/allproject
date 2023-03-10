"""soteria URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include(("soteria.auth.urls", "soteria.auth"), namespace="soteria_auth")),
    path("", include(("soteria.orgs.urls", "soteria.orgs"), namespace="soteria_orgs")),
    path("", include(("soteria.users.urls", "soteria.users"), namespace="soteria_users")),
    path("", include(("soteria.atms.urls", "soteria.atms"), namespace="soteria_atms")),
    path("", include(("soteria.staff.urls", "soteria.staff"), namespace="soteria_staff")),
    path("", include(("soteria.reports.urls", "soteria.reports"), namespace="soteria_reports")),
    path("", include(("soteria.tms.urls", "soteria.tms"), namespace="soteria_tms")),
]
