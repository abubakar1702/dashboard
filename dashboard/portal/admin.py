from django.contrib import admin
from .models import Student, Teacher, Class, Section, Subject, Enrollment, Exam, Grade


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('student_id', 'full_name', 'date_of_birth', 'nationality', 'roll_number', 'phone_number', 'photo')
    list_filter = ('blood_group', 'nationality', 'created_at')
    search_fields = ('first_name', 'last_name', 'student_id', 'email')
    readonly_fields = ('created_at', 'updated_at', 'age')

    fieldsets = (
        ('Personal Information', {
            'fields': (
                'first_name', 'last_name', 'date_of_birth', 'nationality',
                'blood_group', 'photo'
            )
        }),
        ('Academic Information', {
            'fields': ('student_id', 'roll_number', 'phone_number', 'email')
        }),
        ('Parent Information', {
            'fields': ('fathers_name', 'fathers_nid', 'mothers_name', 'mothers_nid', 'birth_certificate_id')
        }),
        ('System Information', {
            'fields': ('created_at', 'updated_at', 'age'),
            'classes': ('collapse',),
        }),
    )


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('teacher_id', 'full_name', 'teacher_nid', 'phone_number', 'email', 'hire_date')
    list_filter = ('blood_group', 'hire_date', 'created_at')
    search_fields = ('first_name', 'last_name', 'teacher_id', 'email')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Personal Information', {
            'fields': ('first_name', 'last_name', 'teacher_nid', 'blood_group')
        }),
        ('Contact Information', {
            'fields': ('phone_number', 'email')
        }),
        ('Employment Information', {
            'fields': ('teacher_id', 'hire_date')
        }),
        ('System Information', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


class SubjectInline(admin.TabularInline):
    model = Subject
    extra = 1


@admin.register(Class)
class ClassAdmin(admin.ModelAdmin):
    list_display = ('class_name', 'class_teacher')
    search_fields = ('class_name', 'class_teacher__first_name', 'class_teacher__last_name')
    filter_horizontal = ('teachers',)
    inlines = [SubjectInline]

@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ("section", "class_ref")

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('subject_name', 'class_ref')
    list_filter = ('class_ref',)
    search_fields = ('subject_name', 'class_ref__class_name')
    filter_horizontal = ('teachers',)


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('student', 'class_enrolled', 'academic_year', 'enrollment_date', 'status')
    list_filter = ('status', 'academic_year', 'class_enrolled', 'enrollment_date')
    search_fields = ('student__first_name', 'student__last_name', 'class_enrolled__class_name')
    readonly_fields = ('created_at', 'updated_at')


class GradeInline(admin.TabularInline):
    model = Grade
    extra = 1
    readonly_fields = ('percentage', 'grade', 'is_passed')


@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    list_display = ('exam_name', 'exam_type', 'subject', 'class_ref', 'academic_year', 'exam_date')
    list_filter = ('exam_type', 'academic_year', 'class_ref', 'subject')
    search_fields = ('exam_name', 'subject__subject_name', 'class_ref__class_name')
    readonly_fields = ('created_at', 'updated_at')
    inlines = [GradeInline]


@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = ('student', 'exam', 'marks_obtained', 'percentage', 'grade', 'is_passed', 'is_absent')
    list_filter = ('exam__exam_type', 'exam__academic_year', 'exam__class_ref', 'is_absent')
    search_fields = ('student__first_name', 'student__last_name', 'exam__exam_name')
    readonly_fields = ('created_at', 'updated_at', 'percentage', 'grade', 'is_passed')

    def get_readonly_fields(self, request, obj=None):
        if obj:  # editing an existing object
            return self.readonly_fields + ('student', 'exam')
        return self.readonly_fields