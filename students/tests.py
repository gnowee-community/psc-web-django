from datetime import date
from django.db import connection
from django.test import TestCase

from course.models import Course
from students.models import Enrollment, Student
from students.serializer import StudentAndModelNestedSerializer, StudentSerializer, StudentModelSerializer, StudentModelNestedSerializer
from utils.models import User
from django.test.utils import CaptureQueriesContext

# Create your tests here.


class SerializerTest(TestCase):

    def setUp(self):
        student_user = User.objects.create_user(
            username="aarav", password="pass123")
        self.student_1 = Student.objects.create(
            user=student_user, first_name="Aarav", last_name="Sharma",
            date_of_birth=date(2000, 1, 15), gender="m",
            phone_number="9876543210",
            emergency_contact_person_name="Rohit Sharma",
            emergency_contact_number="9123456780",
            status="a", date_joined=date(2025, 9, 10),
        )

    def test_serializer(self):
        se = StudentSerializer(self.student_1)
        print(se.data)
        expected_data = {
            'id': 1,
            'user': 1,
            'first_name': 'Aarav',
            'last_name': 'Sharma',
            'date_of_birth': '2000-01-15',
            'gender': 'm',
            'phone_number': '9876543210',
            'emergency_contact_person_name': 'Rohit Sharma',
            'emergency_contact_number': '9123456780',
            'status': 'a',
            'profile_picture': None,
            'date_joined': '2025-09-10'
        }
        self.assertEqual(se.data, expected_data)

    def test_serializer_create(self):

        student_user = User.objects.create_user(
            username="john", password="12345")

        data = {
            'user': student_user.id,
            'first_name': 'John',
            'last_name': 'Doe',
            'date_of_birth': '2000-01-15',
            'gender': 'm',
            'phone_number': '9876543211',
            'emergency_contact_person_name': 'Doe M',
            'emergency_contact_number': '9123456781',
            'status': 'a',
            'profile_picture': None,
            'date_joined': '2025-10-30'
        }

        se = StudentSerializer(data=data)

        print("Serializer valid :", se.is_valid())
        print("Serializer errors:", se.errors)

        self.assertTrue(se.is_valid())

        st2 = se.save()

        print(f"Student created: {st2}")
        print(f"Student count: {Student.objects.count()}")
        print(f"All students: {Student.objects.all()}")

        self.assertEqual(Student.objects.count(), 2)

    def test_update(self):
        st1 = Student.objects.first()
        change = {'last_name': 'alt'}
        se = StudentSerializer(st1, data=change, partial=True)
        self.assertTrue(se.is_valid())
        se.save()
        st1.refresh_from_db()
        self.assertEqual(st1.last_name, 'alt')

    def test_listing(self):
        u2 = User.objects.create_user(username="diya", password="pass123")
        u3 = User.objects.create_user(username="rohan", password="pass123")
        u4 = User.objects.create_user(username="sanya", password="pass123")
        u5 = User.objects.create_user(username="kabir", password="pass123")

        s2 = Student.objects.create(
            user=u2, first_name="Diya", last_name="Verma",
            date_of_birth=date(2001, 5, 22), gender="f",
            phone_number="8765432109",
            emergency_contact_person_name="Neha Verma",
            emergency_contact_number="9234567890",
            status="a", date_joined=date(2025, 9, 11),
        )

        s3 = Student.objects.create(
            user=u3, first_name="Rohan", last_name="Patel",
            date_of_birth=date(1999, 12, 5), gender="m",
            phone_number="7654321098",
            emergency_contact_person_name="Kiran Patel",
            emergency_contact_number="9345678901",
            status="a", date_joined=date(2025, 9, 12),
        )

        s4 = Student.objects.create(
            user=u4, first_name="Sanya", last_name="Kapoor",
            date_of_birth=date(2000, 8, 30), gender="f",
            phone_number="6543210987",
            emergency_contact_person_name="Anil Kapoor",
            emergency_contact_number="9456789012",
            status="a", date_joined=date(2025, 9, 13),
        )

        s5 = Student.objects.create(
            user=u5, first_name="Kabir", last_name="Singh",
            date_of_birth=date(2001, 3, 18), gender="m",
            phone_number="5432109876",
            emergency_contact_person_name="Vikram Singh",
            emergency_contact_number="9567890123",
            status="a", date_joined=date(2025, 9, 14),
        )

        qs = Student.objects.all()

        se = StudentSerializer(qs, many=True)

        self.assertEqual(len(se.data), 5)


class ModelSerializerTest(TestCase):

    def setUp(self):
        student_user = User.objects.create_user(
            username="aarav", password="pass123")
        self.student_1 = Student.objects.create(
            user=student_user, first_name="Aarav", last_name="Sharma",
            date_of_birth=date(2000, 1, 15), gender="m",
            phone_number="9876543210",
            emergency_contact_person_name="Rohit Sharma",
            emergency_contact_number="9123456780",
            status="a", date_joined=date(2025, 9, 10),
        )

    def test_serializer(self):
        se = StudentModelSerializer(self.student_1)
        print(se.data)
        self.assertEqual(se.data["first_name"], "Aarav")
        self.assertEqual(se.data["last_name"], "Sharma")

    def test_serializer_create(self):

        student_user = User.objects.create_user(
            username="john", password="12345")

        data = {
            'user': student_user.id,
            'first_name': 'John',
            'last_name': 'Doe',
            'date_of_birth': '2000-01-15',
            'gender': 'm',
            'phone_number': '9876543211',
            'emergency_contact_person_name': 'Doe M',
            'emergency_contact_number': '9123456781',
            'status': 'a',
            'profile_picture': None,
            'date_joined': '2025-10-30'
        }

        se = StudentModelSerializer(data=data)

        print("Serializer valid :", se.is_valid())
        print("Serializer errors:", se.errors)

        self.assertTrue(se.is_valid())

        st1 = se.save()

        self.assertEqual(Student.objects.count(), 2)

    def test_update(self):
        st1 = Student.objects.first()
        change = {'last_name': 'Doe-alt'}
        se = StudentModelSerializer(st1, data=change, partial=True)
        self.assertTrue(se.is_valid())
        se.save()
        st1.refresh_from_db()
        self.assertEqual(st1.last_name, 'Doe-alt')

    def test_listing(self):
        u2 = User.objects.create_user(username="diya", password="pass123")
        u3 = User.objects.create_user(username="rohan", password="pass123")
        u4 = User.objects.create_user(username="sanya", password="pass123")
        u5 = User.objects.create_user(username="kabir", password="pass123")

        s2 = Student.objects.create(
            user=u2, first_name="Diya", last_name="Verma",
            date_of_birth=date(2001, 5, 22), gender="f",
            phone_number="8765432109",
            emergency_contact_person_name="Neha Verma",
            emergency_contact_number="9234567890",
            status="a", date_joined=date(2025, 9, 11),
        )

        s3 = Student.objects.create(
            user=u3, first_name="Rohan", last_name="Patel",
            date_of_birth=date(1999, 12, 5), gender="m",
            phone_number="7654321098",
            emergency_contact_person_name="Kiran Patel",
            emergency_contact_number="9345678901",
            status="a", date_joined=date(2025, 9, 12),
        )

        s4 = Student.objects.create(
            user=u4, first_name="Sanya", last_name="Kapoor",
            date_of_birth=date(2000, 8, 30), gender="f",
            phone_number="6543210987",
            emergency_contact_person_name="Anil Kapoor",
            emergency_contact_number="9456789012",
            status="a", date_joined=date(2025, 9, 13),
        )

        s5 = Student.objects.create(
            user=u5, first_name="Kabir", last_name="Singh",
            date_of_birth=date(2001, 3, 18), gender="m",
            phone_number="5432109876",
            emergency_contact_person_name="Vikram Singh",
            emergency_contact_number="9567890123",
            status="a", date_joined=date(2025, 9, 14),
        )

        qs = Student.objects.all()

        se = StudentModelSerializer(qs, many=True)

        self.assertEqual(len(se.data), 5)


class NestedSerializerTest(TestCase):

    def setUp(self):
        student_user = User.objects.create_user(
            username="aarav", password="pass123")
        self.student_1 = Student.objects.create(
            user=student_user, first_name="Aarav", last_name="Sharma",
            date_of_birth=date(2000, 1, 15), gender="m",
            phone_number="9876543210",
            emergency_contact_person_name="Rohit Sharma",
            emergency_contact_number="9123456780",
            status="a", date_joined=date(2025, 9, 10),
        )

    def test_serializer(self):
        se = StudentModelNestedSerializer(self.student_1)
        # print(se.data)
        self.assertEqual(se.data["first_name"], "Aarav")
        self.assertEqual(se.data["last_name"], "Sharma")

    def test_serializer_create(self):

        student_user = User.objects.create_user(
            username="john", password="12345")

        data = {
            'user': {"username": "john_doe"},
            'first_name': 'John',
            'last_name': 'Doe',
            'date_of_birth': '2000-01-15',
            'gender': 'm',
            'phone_number': '9876543211',
            'emergency_contact_person_name': 'Doe M',
            'emergency_contact_number': '9123456781',
            'status': 'a',
            'profile_picture': None,
            'date_joined': '2025-10-30'
        }

        se = StudentModelNestedSerializer(data=data)

        print("Serializer valid :", se.is_valid())
        print("Serializer errors:", se.errors)

        self.assertTrue(se.is_valid())

        st1 = se.save()

        self.assertEqual(Student.objects.count(), 2)

    def test_listing(self):
        u2 = User.objects.create_user(username="diya", password="pass123")
        u3 = User.objects.create_user(username="rohan", password="pass123")
        u4 = User.objects.create_user(username="sanya", password="pass123")
        u5 = User.objects.create_user(username="kabir", password="pass123")

        s2 = Student.objects.create(
            user=u2, first_name="Diya", last_name="Verma",
            date_of_birth=date(2001, 5, 22), gender="f",
            phone_number="8765432109",
            emergency_contact_person_name="Neha Verma",
            emergency_contact_number="9234567890",
            status="a", date_joined=date(2025, 9, 11),
        )

        s3 = Student.objects.create(
            user=u3, first_name="Rohan", last_name="Patel",
            date_of_birth=date(1999, 12, 5), gender="m",
            phone_number="7654321098",
            emergency_contact_person_name="Kiran Patel",
            emergency_contact_number="9345678901",
            status="a", date_joined=date(2025, 9, 12),
        )

        s4 = Student.objects.create(
            user=u4, first_name="Sanya", last_name="Kapoor",
            date_of_birth=date(2000, 8, 30), gender="f",
            phone_number="6543210987",
            emergency_contact_person_name="Anil Kapoor",
            emergency_contact_number="9456789012",
            status="a", date_joined=date(2025, 9, 13),
        )

        s5 = Student.objects.create(
            user=u5, first_name="Kabir", last_name="Singh",
            date_of_birth=date(2001, 3, 18), gender="m",
            phone_number="5432109876",
            emergency_contact_person_name="Vikram Singh",
            emergency_contact_number="9567890123",
            status="a", date_joined=date(2025, 9, 14),
        )

        qs = Student.objects.all().select_related("user")
        with CaptureQueriesContext(connection) as ctx:
            se = StudentModelNestedSerializer(qs, many=True)
            se.data
        print(ctx.captured_queries)
        # print(se.data)

        self.assertEqual(len(se.data), 5)


class StudentAndModelNestedSerializerTest(TestCase):

    def setUp(self):
        student_user = User.objects.create_user(
            username="aarav", password="pass123")
        self.student_1 = Student.objects.create(
            user=student_user, first_name="Aarav", last_name="Sharma",
            date_of_birth=date(2000, 1, 15), gender="m",
            phone_number="9876543210",
            emergency_contact_person_name="Rohit Sharma",
            emergency_contact_number="9123456780",
            status="a", date_joined=date(2025, 9, 10),
        )
        Course.objects.create(
            title="General Studies", description="Comprehensive coverage of general studies.", status="p")
        Course.objects.create(
            title="Current Affairs", description="Daily and monthly updates on current events.", status="p")
        Course.objects.create(title="Quantitative Aptitude",
                              description="Practice and learn math and problem-solving skills.", status="p")
        Course.objects.create(title="English & Comprehension",
                              description="Improve English grammar, vocabulary, and comprehension.", status="p")
        Course.objects.create(
            title="History & Culture", description="Study history, heritage, and culture topics.", status="p")
        Course.objects.create(title="Geography & Environment",
                              description="Learn geography, environment, and ecology basics.", status="p")

        Enrollment.objects.create(student_id=1, course_id=1, status="a")
        Enrollment.objects.create(student_id=1, course_id=2, status="a")

    def test_serializer(self):
        se = StudentAndModelNestedSerializer(self.student_1)
        # print(se.data)
        self.assertEqual(se.data["first_name"], "Aarav")
        self.assertEqual(se.data["last_name"], "Sharma")

    def test_serializer_create(self):

        student_user = User.objects.create_user(
            username="john", password="12345")

        data = {
            'user': {"username": "john_doe"},
            'first_name': 'John',
            'last_name': 'Doe',
            'date_of_birth': '2000-01-15',
            'gender': 'm',
            'phone_number': '9876543211',
            'emergency_contact_person_name': 'Doe M',
            'emergency_contact_number': '9123456781',
            'status': 'a',
            'profile_picture': None,
            'date_joined': '2025-10-30'
        }

        se = StudentAndModelNestedSerializer(data=data)

        print("Serializer valid :", se.is_valid())
        print("Serializer errors:", se.errors)

        self.assertTrue(se.is_valid())

        st1 = se.save()

        self.assertEqual(Student.objects.count(), 2)

    def test_listing(self):
        u2 = User.objects.create_user(username="diya", password="pass123")
        u3 = User.objects.create_user(username="rohan", password="pass123")
        u4 = User.objects.create_user(username="sanya", password="pass123")
        u5 = User.objects.create_user(username="kabir", password="pass123")

        s2 = Student.objects.create(
            user=u2, first_name="Diya", last_name="Verma",
            date_of_birth=date(2001, 5, 22), gender="f",
            phone_number="8765432109",
            emergency_contact_person_name="Neha Verma",
            emergency_contact_number="9234567890",
            status="a", date_joined=date(2025, 9, 11),
        )

        s3 = Student.objects.create(
            user=u3, first_name="Rohan", last_name="Patel",
            date_of_birth=date(1999, 12, 5), gender="m",
            phone_number="7654321098",
            emergency_contact_person_name="Kiran Patel",
            emergency_contact_number="9345678901",
            status="a", date_joined=date(2025, 9, 12),
        )

        s4 = Student.objects.create(
            user=u4, first_name="Sanya", last_name="Kapoor",
            date_of_birth=date(2000, 8, 30), gender="f",
            phone_number="6543210987",
            emergency_contact_person_name="Anil Kapoor",
            emergency_contact_number="9456789012",
            status="a", date_joined=date(2025, 9, 13),
        )

        s5 = Student.objects.create(
            user=u5, first_name="Kabir", last_name="Singh",
            date_of_birth=date(2001, 3, 18), gender="m",
            phone_number="5432109876",
            emergency_contact_person_name="Vikram Singh",
            emergency_contact_number="9567890123",
            status="a", date_joined=date(2025, 9, 14),
        )

        qs = Student.objects.all().select_related("user").prefetch_related("courses",)
        with CaptureQueriesContext(connection) as ctx:
            se = StudentAndModelNestedSerializer(qs, many=True)
            se.data
        print(ctx.captured_queries)
        print(len(ctx.captured_queries))
        print(se.data)

        self.assertEqual(len(se.data), 5)
