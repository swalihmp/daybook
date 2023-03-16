"""daybook URL Configuration

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
from . import views
# from django.urls import handler404
# from django.conf.urls.defaults import handler404
from django.urls import path,include 
from django.conf.urls.static import static
from django.conf import settings
from django.shortcuts import render

# handler404 = views.custom_404

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.HomePage, name='HomePage'),
    path('users/',include('users.urls')),
    path('adminp/',include('adminp.urls')),
    path('bank_deposit',views.bank_deposit,name='bank_deposit')
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
