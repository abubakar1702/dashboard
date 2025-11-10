from django.urls import path
from . import views

app_name = 'portal'

urlpatterns = [
    path('', views.student_list, name='student_list'),
    # Or use the simple version:
    # path('', views.student_list_simple, name='student_list'),
]