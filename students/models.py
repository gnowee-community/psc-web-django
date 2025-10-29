from django.db import models
from django.contrib.auth import get_user_model
from django.dispatch import receiver

from utils.models import BaseModel, SoftDeleteModel
User = get_user_model()


class Student (SoftDeleteModel):
    GENDER_CHOICES = (
        ("m", "Male"),
        ("f", "Female"),
        ("o", "Others"),
    )
    STATUS_CHOICES = (
        ("a", "Active"),
        ("i", "Inactive"),
        ("s", "Suspended"),
        ("g", "Graduated"),
        ("w", "Withdrawn"),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    phone_number = models.CharField(max_length=10, unique=True)
    emergency_contact_person_name = models.CharField(max_length=100)
    emergency_contact_number = models.CharField(max_length=10)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES)
    profile_picture = models.CharField(max_length=10, null=True, blank=True)
    date_joined = models.DateField()
    courses = models.ManyToManyField("course.Course", through="Enrollment")

    def __str__(self):
        return f"{self.pk} : {self.first_name} {self.last_name}"


# Student enrollment for courses
class Enrollment(SoftDeleteModel):
    STATUS_CHOICES = (
        ("a", "Active"),
        ("i", "Inactive"),
        ("c", "Completed"),
        ("d", "Dropped"),
    )
    student = models.ForeignKey('Student', on_delete=models.CASCADE)
    course = models.ForeignKey('course.Course', on_delete=models.CASCADE)
    enrollment_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=1, choices=STATUS_CHOICES, default="a")

    def __str__(self):
        return f"Enrollment {self.id}: Student {self.student_id} in Course {self.course_id}"
