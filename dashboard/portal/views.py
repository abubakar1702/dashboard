from django.shortcuts import render, get_object_or_404
from .models import Student, Class, Teacher, Enrollment, Section
from datetime import datetime


def teacher_list(request):
    teachers = Teacher.objects.all()
    context = {
        'teachers': teachers,
    }
    return render(request, 'portal/teachers.html', context)


def teacher_info(request, teacher_id):
    teacher = get_object_or_404(Teacher, id=teacher_id)
    context = {
        'teacher': teacher,
    }
    return render(request, 'portal/teacher_info.html', context)



from django.db.models import Exists, OuterRef

def student_list(request):
    selected_class = request.GET.get('class', 'all')
    selected_gender = request.GET.get('gender', 'all')
    selected_section = request.GET.get('section', 'all')
    selected_status = request.GET.get('status', 'ACTIVE')

    enrollment_filter = Enrollment.objects.filter(
        student=OuterRef('pk'),
        status=selected_status
    )

    if selected_class and selected_class != 'all':
        try:
            class_id = int(selected_class)
            enrollment_filter = enrollment_filter.filter(class_enrolled__id=class_id)
        except (ValueError, TypeError):
            pass

    if selected_class and selected_class != 'all' and selected_section and selected_section != 'all':
        try:
            section_id = int(selected_section)
            enrollment_filter = enrollment_filter.filter(section__id=section_id)
        except (ValueError, TypeError):
            pass

    students = Student.objects.filter(
        Exists(enrollment_filter)
    ).order_by('student_id')

    if selected_gender and selected_gender != 'all':
        students = students.filter(gender=selected_gender)

    classes = Class.objects.all().order_by('class_serial')
    
    if selected_class and selected_class != 'all':
        try:
            class_id = int(selected_class)
            sections = Section.objects.filter(class_ref__id=class_id).order_by('section')
        except (ValueError, TypeError):
            sections = Section.objects.none()
    else:
        sections = Section.objects.none()

    context = {
        'students': students,
        'total_students': students.count(),
        'classes': classes,
        'sections': sections,
        'selected_class': selected_class,
        'selected_gender': selected_gender,
        'selected_section': selected_section,
        'selected_status': selected_status,
    }
    return render(request, 'portal/students.html', context)

def student_info(request, student_id):
    student = get_object_or_404(Student, id=student_id)

    earliest_enrollment = student.enrollments.order_by('enrollment_date').first()
    
    if earliest_enrollment:
        start_year = earliest_enrollment.enrollment_date.year
    else:
        start_year = datetime.now().year
    
    current_year = datetime.now().year

    available_years = list(range(start_year, current_year + 1))
    
    selected_year = request.GET.get('year', current_year)
    try:
        selected_year = int(selected_year)
    except (ValueError, TypeError):
        selected_year = current_year
    
    grades = student.grades.filter(exam__academic_year=selected_year)
    
    roll = student.enrollments.last().roll_number

    section = student.enrollments.first().section
    
    context = {
        'student': student,
        'grades': grades,
        'roll_number': roll,
        'available_years': available_years,
        'selected_year': selected_year,
        'section': section,
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