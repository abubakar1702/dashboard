import os
import django
from decimal import Decimal

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')
django.setup()

from portal.models import Grade, Student, Exam, Subject, Class, Teacher
from datetime import date

def verify_fix():
    print("Verifying fix for Grade properties with None marks_obtained...")

    # Create dummy objects if needed (we just need a Grade instance, but it needs FKs)
    # Actually, we can just instantiate Grade without saving to DB to test properties if they don't rely on DB state
    # But properties rely on self.exam.total_marks and self.exam.pass_marks
    
    # Let's try to mock or create minimal objects
    try:
        # Create a dummy teacher
        teacher = Teacher(first_name="Test", last_name="Teacher", teacher_id=9999, teacher_nid="123", email="test@test.com", hire_date=date.today())
        # We won't save them to avoid polluting DB if possible, but FKs need saved objects usually if we access them via ORM
        # However, we can assign instances directly to fields
        
        # Create dummy class
        cls = Class(class_name="TestClass", class_teacher=teacher)
        
        # Create dummy subject
        subj = Subject(subject_name="TestSubject", class_ref=cls)
        
        # Create dummy exam
        exam = Exam(exam_name="TestExam", subject=subj, class_ref=cls, academic_year="2024", exam_date=date.today(), total_marks=100, pass_marks=40)
        
        # Create dummy student
        student = Student(first_name="Test", last_name="Student", student_id=9999)
        
        # Create Grade with marks_obtained=None
        grade = Grade(student=student, exam=exam, marks_obtained=None)
        
        # Test properties
        print(f"Testing grade property: {grade.grade}")
        assert grade.grade is None
        
        print(f"Testing percentage property: {grade.percentage}")
        assert grade.percentage == 0
        
        print(f"Testing is_passed property: {grade.is_passed}")
        assert grade.is_passed == False
        
        print("Verification SUCCESS: All properties handled None correctly.")
        
    except Exception as e:
        print(f"Verification FAILED: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    verify_fix()
