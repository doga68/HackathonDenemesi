from django.contrib.auth import views as auth
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('giris/', auth.LoginView.as_view(template_name='form.html',
         extra_context={'title': 'Giriş Yap', 'button': 'Giriş'}), name='login'),
    path('cikis/', auth.LogoutView.as_view(), name='logout'),
    path('kayit/isveren/', views.register, {'role': 'hr'}, name='register_hr'),
    path('kayit/aday/', views.register, {'role': 'seeker'}, name='register_seeker'),
]
