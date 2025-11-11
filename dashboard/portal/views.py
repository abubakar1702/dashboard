from django.shortcuts import render
from django.core.paginator import Paginator
from .models import Student


def student_list(request):
    students = Student.objects.all().order_by('last_name', 'first_name')

    context = {
        'students': students,
        'total_students': students.count()
    }

    return render(request, 'portal/index.html', context)

def student_info(request, student_id):
    student = Student.objects.filter(student_id = student_id)

    context = {
        'student' : student
    }

    return render(request, 'portal/student_info.html', context)