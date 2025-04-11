from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),  # Add this new path
    path('log/', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('loggedin/', views.login_success, name='login_success'),
    path('logout/', views.logout_view, name='logout'),
    path('create-student/', views.create_student, name='create_student'),
    path('student-list/', views.student_list, name='student_list'),
    path('update-student/', views.update_student, name='update_student'),
]