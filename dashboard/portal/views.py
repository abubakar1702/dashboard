from django.shortcuts import render, get_object_or_404
from .models import Student


def student_list(request):
    students = Student.objects.all().order_by('last_name', 'first_name')

    context = {
        'students': students,
        'total_students': students.count()
    }

    return render(request, 'portal/index.html', context)

def student_info(request, student_id):
    student = get_object_or_404(Student, id=student_id)

    context = {
        'student': student
    }

    return render(request, 'portal/student_info.html', context)