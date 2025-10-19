from django.db import models
from django.contrib.auth import get_user_model

from utils.models import BaseModel
User = get_user_model()


class Student (BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100,validators=[])
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(
        choices=(("m", "Male"), ("f", "Female"), ("o", "Others")))
    phone_number = models.CharField(max_length=10, unique=True)
    emergency_contact_person_name = models.CharField(max_length=100)
    emergency_contact_number = models.CharField(max_length=10)
    status = models.CharField(choices=(
        ("a", "Active"), ("s", "Suspended"), ("g", "Graduated"), ("w", "Withdrawn")))
    profile_picture = models.CharField(max_length=10, null=True, blank=True)
    date_joined = models.DateField()
    created_by = models.ForeignKey(
        User, on_delete=models.DO_NOTHING, null=True, blank=True, related_name="student_created_by")
    updated_by = models.ForeignKey(
        User, on_delete=models.DO_NOTHING, null=True, blank=True, related_name="student_updated_by")
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.pk} : {self.first_name} {self.last_name}"


# Student enrollment for courses
class Enrollment(BaseModel):
    STATUS_CHOICES = (
        ("a", "Active"),
        ("c", "Completed"),
        ("d", "Dropped"),
    )
    student = models.ForeignKey('Student', on_delete=models.CASCADE)
    course = models.ForeignKey('course.Course', on_delete=models.CASCADE)
    enrollment_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=15, choices=STATUS_CHOICES, default="active")
    created_by = models.ForeignKey(User, on_delete=models.DO_NOTHING,
                                   null=True, blank=True, related_name="enrollment_created_by")
    updated_by = models.ForeignKey(User, on_delete=models.DO_NOTHING,
                                   null=True, blank=True, related_name="enrollment_updated_by")
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Enrollment {self.id}: Student {self.student_id} in Course {self.course_id}"
