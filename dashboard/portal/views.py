from django.shortcuts import render, get_object_or_404
from .models import Student, Class


def student_list(request):
    students = Student.objects.filter(enrollments__status='ACTIVE').distinct().order_by('last_name', 'first_name')

    context = {
        'students': students,
        'total_students': students.count()
    }

    return render(request, 'portal/students.html', context)

def student_info(request, student_id):
    student = get_object_or_404(Student, id=student_id)

    context = {
        'student': student
    }

    return render(request, 'portal/student_info.html', context)


def class_list(request):
    classes = Class.objects.all().order_by('class_serial')
    context = {
        'classes': classes,
    }
    return render(request, 'portal/class.html', context)


def class_info(request, class_id):
    class_obj = get_object_or_404(Class, id=class_id)
    context = {
        'class_obj': class_obj,
    }
    return render(request, 'portal/class_info.html', context)