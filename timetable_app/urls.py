from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('student/',views.student_home, name="student_home"),
    path('teacher/',views.teacher_home, name="teacher_home"),
    path('admin_home/',views.admin_home, name="admin_home"),
    path('',views.home, name="home"),
     
    
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),  # Add this line for logout
  
    # Registration path
    path('sign-up/access/', views.access_page, name='access_page'),
    # path('register/<str:identification_number>/', views.register, name='register'),
    path('register/', views.register, name='register'),

    # Other URLs (login, etc.)
    path('login/', views.login_view, name='login'),

    # Other app URLs...
    # path('generate_timetable/', views.generate_timetable_view, name='generate_timetable'),
    path('view_timetable/', views.view_timetable, name='view_timetable'),  # Timetable page
    path('update_timetable/', views.update_timetable, name='update_timetable'),  # Add this line
    
    
    path('identification_number/add/', views.add_identification_numbers, name='add_identification_numbers'),
    path('identification_number/retrieve/', views.retrieve_identification_numbers, name='retrieve_identification_numbers'),
    path('identification_number/update/<int:pk>/', views.update_identification_number, name='update_identification_number'),
    path('identification_number/delete/<int:pk>/', views.delete_identification_number, name='delete_identification_number'),
    
    
    # teachers
    path('teachers/view/', views.view_teachers, name='view_teachers'),
    
    
    
    
      
    # students
    path('students/view/', views.view_students, name='view_students'),

]
