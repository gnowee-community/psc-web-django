from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Teacher

User = get_user_model()


class TeacherSoftDeleteTestCase(TestCase):
    """Test case for Teacher model soft delete functionality"""

    def setUp(self):
        """Set up test data - create separate users for each teacher"""
        self.user1 = User.objects.create_user(
            username='teacher1',
            email='teacher1@example.com',
            password='testpass123'
        )
        self.user2 = User.objects.create_user(
            username='teacher2',
            email='teacher2@example.com',
            password='testpass123'
        )
        self.user3 = User.objects.create_user(
            username='teacher3',
            email='teacher3@example.com',
            password='testpass123'
        )

    def test_soft_delete_functionality(self):
        """
        Test soft delete workflow:
        1. Create 3 teachers (each with unique user)
        2. Count and assert 3 teachers exist
        3. Delete 1 teacher
        4. objects should return 2 (active only)
        5. all_objects should return 3 (including deleted)
        6. Reactivate the deleted teacher
        7. Verify counts again
        """
        # Step 1: Create 3 teachers with unique users
        teacher1 = Teacher.objects.create(
            user=self.user1,
            first_name="John",
            last_name="Doe",
            gender="m",
            employee_code="EMP001",
            email_institutional="john.doe@institution.edu",
            status="a"
        )
        teacher2 = Teacher.objects.create(
            user=self.user2,
            first_name="Jane",
            last_name="Smith",
            gender="f",
            employee_code="EMP002",
            email_institutional="jane.smith@institution.edu",
            status="a"
        )
        teacher3 = Teacher.objects.create(
            user=self.user3,
            first_name="Bob",
            last_name="Johnson",
            gender="m",
            employee_code="EMP003",
            email_institutional="bob.johnson@institution.edu",
            status="a"
        )

        # Step 2: Count and assert 3 teachers exist
        self.assertEqual(Teacher.objects.count(), 3, "Should have 3 active teachers")
        self.assertEqual(Teacher.all_objects.count(), 3, "Should have 3 total teachers")

        # Step 3: Delete 1 teacher (soft delete)
        teacher1.delete()

        # Step 4: objects should return 2 (active only)
        self.assertEqual(Teacher.objects.count(), 2, "Should have 2 active teachers after soft delete")
        
        # Step 5: all_objects should return 3 (including deleted)
        self.assertEqual(Teacher.all_objects.count(), 3, "Should still have 3 total teachers (including soft deleted)")

        # Verify the deleted teacher has status 'i'
        teacher1.refresh_from_db()
        self.assertEqual(teacher1.status, "i", "Deleted teacher should have status 'i' (inactive)")

        # Verify the remaining active teachers
        active_teachers = Teacher.objects.all()
        self.assertIn(teacher2, active_teachers, "Teacher 2 should be in active list")
        self.assertIn(teacher3, active_teachers, "Teacher 3 should be in active list")
        self.assertNotIn(teacher1, active_teachers, "Teacher 1 should NOT be in active list")

        # Step 6: Reactivate the deleted teacher
        teacher1.activate()

        # Step 7: Verify counts again - all 3 should be active now
        self.assertEqual(Teacher.objects.count(), 3, "Should have 3 active teachers after reactivation")
        self.assertEqual(Teacher.all_objects.count(), 3, "Should have 3 total teachers after reactivation")

        # Verify the reactivated teacher has status 'a'
        teacher1.refresh_from_db()
        self.assertEqual(teacher1.status, "a", "Reactivated teacher should have status 'a' (active)")

        # Verify all teachers are now in the active list
        active_teachers = Teacher.objects.all()
        self.assertIn(teacher1, active_teachers, "Teacher 1 should be back in active list")
        self.assertIn(teacher2, active_teachers, "Teacher 2 should be in active list")
        self.assertIn(teacher3, active_teachers, "Teacher 3 should be in active list")
