
from django.db import models
from django.contrib.auth import get_user_model

from utils.models import BaseModel, SoftDeleteModel

User = get_user_model()


class Teacher(SoftDeleteModel):
    GENDER_CHOICES = (
        ("m", "Male"),
        ("f", "Female"),
        ("o", "Other"),
    )
    STATUS_CHOICES = (
        ("a", "Active"),
        ("i", "Inactive"),
        ("l", "On Leave"),
        ("r", "Resigned"),
        ("t", "Retired"),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    dob = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    employee_code = models.CharField(max_length=50, unique=True)
    experience_years = models.PositiveIntegerField(default=0)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    emergency_contact_number = models.CharField(
        max_length=20, blank=True, null=True)
    email_institutional = models.CharField(max_length=150, unique=True)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES)
    profile_picture = models.CharField(max_length=255, blank=True, null=True)
    date_joined = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.employee_code})"


class Qualification(BaseModel):
    STATUS_CHOICES = (
        ("a", "Active"),
        ("i", "Inactive"),
    )

    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    status = models.CharField(
        max_length=1, choices=STATUS_CHOICES, default="a")

    def __str__(self):
        return self.name


class UserQualification(BaseModel):
    STATUS_CHOICES = (
        ("a", "Active"),
        ("i", "Inactive"),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    qualification = models.ForeignKey(
        'Qualification', on_delete=models.CASCADE)
    status = models.CharField(
        max_length=1, choices=STATUS_CHOICES, default="a")

    def __str__(self):
        return f"{self.user} - {self.qualification}"


class Specialization(BaseModel):
    STATUS_CHOICES = (
        ("a", "Active"),
        ("i", "Inactive"),
    )

    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    status = models.CharField(
        max_length=1, choices=STATUS_CHOICES, default="a")

    def __str__(self):
        return self.name


class UserSpecialization(BaseModel):
    STATUS_CHOICES = (
        ("a", "Active"),
        ("i", "Inactive"),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    specialization = models.ForeignKey(
        'Specialization', on_delete=models.CASCADE)
    status = models.CharField(
        max_length=1, choices=STATUS_CHOICES, default="a")

    def __str__(self):
        return f"{self.user} - {self.specialization}"


class Department(BaseModel):
    STATUS_CHOICES = (
        ("a", "Active"),
        ("i", "Inactive"),
    )

    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    status = models.CharField(
        max_length=1, choices=STATUS_CHOICES, default="a")

    def __str__(self):
        return self.name


class UserDepartment(BaseModel):
    STATUS_CHOICES = (
        ("a", "Active"),
        ("i", "Inactive"),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    department = models.ForeignKey('Department', on_delete=models.CASCADE)
    status = models.CharField(
        max_length=1, choices=STATUS_CHOICES, default="a")

    def __str__(self):
        return f"{self.user} - {self.department}"


class Designation(BaseModel):
    STATUS_CHOICES = (
        ("a", "Active"),
        ("i", "Inactive"),
    )

    designation_name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    status = models.CharField(
        max_length=1, choices=STATUS_CHOICES, default="a")

    def __str__(self):
        return self.designation_name


class UserDesignation(BaseModel):
    STATUS_CHOICES = (
        ("a", "Active"),
        ("i", "Inactive"),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    designation = models.ForeignKey('Designation', on_delete=models.CASCADE)
    status = models.CharField(
        max_length=1, choices=STATUS_CHOICES, default="a")

    def __str__(self):
        return f"{self.user} - {self.designation}"
