from django.db import models
from datetime import date
from django.core.validators import MinValueValidator, MaxValueValidator
from datetime import date


class BloodGroups(models.TextChoices):
    A_POSITIVE = "A_POS", "A+"
    A_NEGATIVE = "A_NEG", "A-"
    B_POSITIVE = "B_POS", "B+"
    B_NEGATIVE = "B_NEG", "B-"
    AB_POSITIVE = "AB_POS", "AB+"
    AB_NEGATIVE = "AB_NEG", "AB-"
    O_POSITIVE = "O_POS", "O+"
    O_NEGATIVE = "O_NEG", "O-"


class Student(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    nationality = models.CharField(max_length=100)
    student_id = models.IntegerField(unique=True)
    roll_number = models.SmallIntegerField()
    phone_number = models.CharField(max_length=15, blank=True)
    email = models.EmailField(max_length=100, null=True, blank=True)
    photo = models.ImageField(upload_to="photos/", null=True, blank=True)
    blood_group = models.CharField(
        max_length=10,
        choices=BloodGroups.choices,
        blank=True,
        null=True
    )
    birth_certificate_id = models.IntegerField(null=True, blank=True)
    fathers_name = models.CharField(max_length=100)
    fathers_nid = models.CharField(max_length=17)
    mothers_name = models.CharField(max_length=100)
    mothers_nid = models.CharField(max_length=17)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def age(self):
        today = date.today()
        base_age = today.year - self.date_of_birth.year
        is_birthday_passed = (today.month, today.day) >= (self.date_of_birth.month, self.date_of_birth.day)
        return base_age if is_birthday_passed else base_age - 1


class Teacher(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    teacher_id = models.IntegerField(unique=True)
    teachers_nid = models.CharField(max_length=17)
    phone_number = models.CharField(max_length=15, blank=True)
    email = models.EmailField(max_length=100, unique=True)
    photo = models.ImageField(upload_to="photos/", null=True, blank=True)
    blood_group = models.CharField(
        max_length=10,
        choices=BloodGroups.choices,
        blank=True,
        null=True
    )
    hire_date = models.DateField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return f"Prof. {self.last_name}"

    class Meta:
        verbose_name = "Teacher Record"
        ordering = ['last_name']


class Class(models.Model):
    class Section(models.TextChoices):
        SECTION_A = "SEC A", "Section A"
        SECTION_B = "SEC B", "Section B"
        SECTION_C = "SEC C", "Section C"

    class_name = models.CharField(max_length=10)
    section = models.CharField(
        max_length=15,
        choices=Section.choices,
    )
    teachers = models.ManyToManyField(Teacher, related_name='classes')
    class_teacher = models.ForeignKey(
        Teacher,
        on_delete=models.CASCADE,
        related_name='lead_classes'
    )

    def __str__(self):
        return f"{self.class_name} - {self.section}"

    class Meta:
        verbose_name_plural = "Classes"


class Subject(models.Model):
    subject_name = models.CharField(max_length=100)
    class_ref = models.ForeignKey(Class, on_delete=models.CASCADE, related_name='subjects')
    teachers = models.ManyToManyField(Teacher, related_name='subjects')

    def __str__(self):
        return self.subject_name


class Enrollment(models.Model):
    class Status(models.TextChoices):
        ACTIVE = "ACTIVE", "Active"
        INACTIVE = "INACTIVE", "Inactive"
        GRADUATED = "GRADUATED", "Graduated"
        TRANSFERRED = "TRANSFERRED", "Transferred"
        DROPPED = "DROPPED", "Dropped"

    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='enrollments')
    class_enrolled = models.ForeignKey(Class, on_delete=models.CASCADE, related_name='enrollments')
    academic_year = models.CharField(max_length=9, help_text="e.g., 2024-2025")
    enrollment_date = models.DateField()
    status = models.CharField(
        max_length=15,
        choices=Status.choices,
        default=Status.ACTIVE
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Enrollment"
        verbose_name_plural = "Enrollments"
        ordering = ['-enrollment_date']
        unique_together = ['student', 'class_enrolled', 'academic_year']

    def __str__(self):
        return f"{self.student.full_name} - {self.class_enrolled} ({self.academic_year})"


class Exam(models.Model):
    class ExamType(models.TextChoices):
        MIDTERM = "MIDTERM", "Mid-Term Exam"
        FINAL = "FINAL", "Final Exam"
        FIRST_CLASS_TEST = "FIRST_CLASS_TEST", "Class Test"
        SECOND_CLASS_TEST = "SECOND_CLASS_TEST", "Class Test"
        PRACTICAL = "PRACTICAL", "Practical Exam"

    exam_name = models.CharField(max_length=100)
    exam_type = models.CharField(max_length=20, choices=ExamType.choices)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='exams')
    class_ref = models.ForeignKey(Class, on_delete=models.CASCADE, related_name='exams')
    academic_year = models.CharField(max_length=9)
    exam_date = models.DateField()
    total_marks = models.PositiveIntegerField(default=100)
    pass_marks = models.PositiveIntegerField(default=40)
    duration_minutes = models.PositiveIntegerField(help_text="Exam duration in minutes")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-exam_date']
        unique_together = ['exam_name', 'subject', 'class_ref', 'academic_year']

    def __str__(self):
        return f"{self.exam_name} - {self.subject} ({self.class_ref})"


class Grade(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='grades')
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='grades')
    marks_obtained = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    remarks = models.TextField(blank=True, null=True)
    is_absent = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['student', 'exam']
        ordering = ['-exam__exam_date']

    def __str__(self):
        return f"{self.student.full_name} - {self.exam.exam_name}: {self.marks_obtained}/{self.exam.total_marks}"

    @property
    def percentage(self):
        if self.is_absent:
            return 0
        return (self.marks_obtained / self.exam.total_marks) * 100

    @property
    def is_passed(self):
        if self.is_absent:
            return False
        return self.marks_obtained >= self.exam.pass_marks

    @property
    def grade(self):
        if self.is_absent:
            return "AB"

        marks = self.marks_obtained
        if marks >= 80:
            return "A+"
        elif marks >= 70:
            return "A"
        elif marks >= 60:
            return "A-"
        elif marks >= 50:
            return "B"
        elif marks >= 40:
            return "C"
        elif marks >= 33:
            return "D"
        else:
            return "F"
