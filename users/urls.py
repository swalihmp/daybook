from django.contrib import admin
from . import views
from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('addexp',views.addexp,name='addexp'),
    path('add_exp',views.add_exp,name='add_exp'),
    path('addincome',views.addincome,name='addincome'),
    path('add_inc',views.add_inc,name='add_inc'),
    path('new_income',views.new_income,name='new_income'),
    path('new_exp',views.new_exp,name='new_exp'),
    path('new_doc',views.new_doc,name='new_doc'),
    path('doctors',views.doctors,name='doctors'),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)