from django.urls import path
from . import views as v

urlpatterns = [
    path('isveren/', v.hr_dashboard, name='hr_dashboard'),
    path('isveren/ilan/yeni/', v.job_create, name='job_create'),
    path('isveren/ilan/<int:pk>/basvurular/', v.applicants, name='applicants'),
    path('isveren/basvuru/<int:pk>/<str:decision>/', v.decide, name='decide'),
    path('isveren/calisan/yeni/', v.worker_create, name='worker_create'),
    path('ilanlar/', v.job_list, name='job_list'),
    path('ilanlar/<int:pk>/', v.job_detail, name='job_detail'),
    path('basvurularim/', v.my_applications, name='my_applications'),
    path('profil/', v.profile, name='profile'),
]
