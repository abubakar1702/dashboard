from django.urls import path
from . import views

app_name = 'portal'

urlpatterns = [
    path('students/', views.student_list, name='student_list'),
    path('students/<int:student_id>/', views.student_info, name='student_info'),
]