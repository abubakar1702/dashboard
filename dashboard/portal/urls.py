from django.urls import path
from . import views

app_name = 'portal'

urlpatterns = [
    path('students/', views.student_list, name='student_list'),
    path('students/<int:student_id>/', views.student_info, name='student_info'),
    path('teachers/', views.teacher_list, name='teacher_list'),
    path('teachers/<int:teacher_id>/', views.teacher_info, name='teacher_info'),
    path('classes/', views.class_list, name='class_list'),
    path('classes/<int:class_id>/', views.class_info, name='class_info'),
]