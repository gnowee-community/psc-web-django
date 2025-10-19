
from django.db import models
from django.contrib.auth import get_user_model

from utils.models import BaseModel

User = get_user_model()


class Teacher(BaseModel):
	GENDER_CHOICES = (
        ("male", "Male"),
		("female", "Female"),
		("other", "Other"),
    )
	STATUS_CHOICES = (
        ("active", "Active"),
		("on_leave", "On Leave"),
		("resigned", "Resigned"),
		("retired", "Retired"),
    )

	user = models.ForeignKey(User, on_delete=models.CASCADE)
	first_name = models.CharField(max_length=100)
	last_name = models.CharField(max_length=100)
	dob = models.DateField(null=True, blank=True)
	gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
	employee_code = models.CharField(max_length=50, unique=True)
	experience_years = models.PositiveIntegerField(default=0)
	phone_number = models.CharField(max_length=20, blank=True, null=True)
	emergency_contact_number = models.CharField(max_length=20, blank=True, null=True)
	email_institutional = models.CharField(max_length=150, unique=True)
	status = models.CharField(max_length=20, choices=STATUS_CHOICES)
	profile_picture = models.CharField(max_length=255, blank=True, null=True)
	date_joined = models.DateTimeField(null=True, blank=True)

	def __str__(self):
		return f"{self.first_name} {self.last_name} ({self.employee_code})"
