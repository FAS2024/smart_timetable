from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('',views.home, name="home"),
     
    
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),  # Add this line for logout
  
    # Registration path
    path('register/', views.register, name='register'),

    # Other URLs (login, etc.)
    path('login/', views.login_view, name='login'),

    # Other app URLs...
    # path('generate_timetable/', views.generate_timetable_view, name='generate_timetable'),
    path('view_timetable/', views.view_timetable, name='view_timetable'),  # Timetable page
    path('update_timetable/', views.update_timetable, name='update_timetable'),  # Add this line
]
