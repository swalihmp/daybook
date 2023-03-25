from django.urls import path
from . import views

urlpatterns = [
    path('users/',views.users,name='users'),
    path('blockuser/<int:id>/<str:action>/',views.blockuser,name='blockuser'),
    path('register/',views.register, name='register'),
    path('login/',views.login,name='login'),
    path('logout/',views.logout,name='logout'),
    path('activate/<uidb64>/<token>',views.activate,name='activate'),
    path('doctor_report',views.doctor_report,name='doctor_report'),
    path('admin_search',views.admin_search,name='admin_search'),
    path('admin_search_data',views.admin_search_data,name='admin_search_data'),
    path('admin_HomePage',views.admin_HomePage,name='admin_HomePage'),
    path('datewiseexp',views.datewiseexp,name='datewiseexp'),
    path('datewiseinc',views.datewiseinc,name='datewiseinc'),
    path('credits_p',views.credits_p,name='credits_p'),
    path('patient_p',views.patient_p,name='patient_p')

    
]