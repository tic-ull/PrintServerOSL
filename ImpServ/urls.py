"""ImpServ URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from rest_framework import routers
from APImpServ import views

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'userprofile', views.UserProfileViewSet)
router.register(r'printers', views.PrinterViewSet)
router.register(r'usertype', views.UserTypeViewSet)
router.register(r'printerquota', views.QuotaViewSet)
router.register(r'userquota', views.UserQuotaViewSet)
router.register(r'logs', views.LogsViewSet)
router.register(r'printsession', views.PrintSessionViewSet)
router.register(r'print', views.PrintViewSet, base_name='Print')
router.register(r'printon', views.PrintOnViewSet, base_name='PrintOn')

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]

