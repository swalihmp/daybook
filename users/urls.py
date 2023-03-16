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
    path('mark/<int:id>/',views.mark,name='mark'),
    path('cmark/<int:id>/',views.cmark,name='cmark'),
    path('credits',views.credits,name='credits'),
    path('search',views.search,name='search'),
    path('search_data',views.search_data,name='search_data'),
    path('dayclose',views.dayclose,name='dayclose'),
    path('daycloseamount',views.daycloseamount,name='daycloseamount')
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)