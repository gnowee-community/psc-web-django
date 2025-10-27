from datetime import date
from django.test import TestCase
from django.contrib.auth import get_user_model

from course.models import Course
from students.models import Enrollment, Student

User = get_user_model()

# Create your tests here.


class StudentEnrollmentTest(TestCase):

    def setUp(self):
        admin = User.objects.create(username="admin")
        u1 = User.objects.create_user(username="aarav", password="pass123")
        s1 = Student.objects.create(
            user=u1, first_name="Aarav", last_name="Sharma",
            date_of_birth=date(2000, 1, 15), gender="m",
            phone_number="9876543210",
            emergency_contact_person_name="Rohit Sharma",
            emergency_contact_number="9123456780",
            status="a", date_joined=date(2025, 9, 10),
            created_by=admin, updated_by=admin
        )

        c1 = Course.objects.create(
            title="General Studies",
            description="Comprehensive coverage of general studies.",
            status="p", created_by=admin, updated_by=admin)

        Enrollment.objects.create(
            student_id=1, course_id=1, status="a", created_by=admin, updated_by=admin)

    def test_admin(self):
        self.assertEqual(User.objects.filter(username="admin").count(), 1)

    def test_enrollments(self):
        s_count = Enrollment.objects.filter(student__id=1).count()
        print("Count : ", s_count)
        self.assertAlmostEqual(s_count, 1)
