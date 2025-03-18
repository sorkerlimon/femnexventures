from django.urls import path
from . import views

app_name = 'femnexventures_web'

urlpatterns = [
    path('', views.home_view, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    # Add your URL patterns here
    # Example: path('', views.home, name='home'),
] 