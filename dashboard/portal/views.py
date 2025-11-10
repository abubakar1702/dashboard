from django.shortcuts import render
from django.core.paginator import Paginator
from .models import Student


def student_list(request):
    students = Student.objects.all().order_by('last_name', 'first_name')
    search_query = request.GET.get('search', '')
    if search_query:
        students = students.filter(
            first_name__icontains=search_query
        ) | students.filter(
            last_name__icontains=search_query
        ) | students.filter(
            student_id__icontains=search_query
        )

    # Optional: Add pagination (10 students per page)
    paginator = Paginator(students, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'students': page_obj,
        'search_query': search_query,
        'total_students': students.count()
    }

    return render(request, 'portal/index.html', context)


# Alternative: Simple view without pagination
def student_list_simple(request):
    """
    Simple view to display all students
    """
    students = Student.objects.all().order_by('last_name', 'first_name')

    context = {
        'students': students,
        'total_students': students.count()
    }

    return render(request, 'portal/index.html', context)