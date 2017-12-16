"""svexchange URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.urls import include, path, re_path
from sv import views, views_rest
from svexdb.settings import ADMIN_URL

urlpatterns = [
    path('', views.paste),
    path(ADMIN_URL, admin.site.urls),
    path('formatter', views.esv_tabler),
    re_path('tsv/(?P<gen>[6-7])/(?P<tsv>[0-3][0-9]{3}|[4][0][0-9][0-5])',
            views_rest.ShinyValueViewSet.as_view({'get': 'list'})),
    re_path('trainer/(?P<username>[-\w]{1,24})/', views_rest.TrainerViewSet.as_view({'get': 'list'})),
    #path('trainers/', views_rest.TrainersViewSet.as_view({'get': 'list'})),
]

