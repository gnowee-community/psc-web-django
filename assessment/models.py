from django.db import models
from django.contrib.auth import get_user_model
from utils.models import BaseModel

User = get_user_model()


class Assignment(BaseModel):
    course = models.ForeignKey('course.Course', on_delete=models.CASCADE)
    teacher = models.ForeignKey(
        'staff.Teacher', on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=150)
    description = models.TextField(blank=True, null=True)
    due_date = models.DateTimeField(null=True, blank=True)
    # created_date = models.DateTimeField(auto_now_add=True)
    # created_by = models.ForeignKey(User, on_delete=models.DO_NOTHING,
    #                                null=True, blank=True, related_name="assignment_created_by")

    def __str__(self):
        return f"{self.title} (Course: {self.course_id})"

# Submissions done by students
class Submission(BaseModel):
    STATUS_CHOICES = [
        ("submitted", "Submitted"),
        ("late", "Late"),
        ("graded", "Graded"),
    ]

    assignment = models.ForeignKey('Assignment', on_delete=models.CASCADE)
    student = models.ForeignKey('students.Student', on_delete=models.CASCADE)
    file_url = models.CharField(max_length=255)
    submitted_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default="submitted")
    # created_by = models.ForeignKey(User, on_delete=models.DO_NOTHING,
    #                                null=True, blank=True, related_name="submission_created_by")
    # updated_by = models.ForeignKey(User, on_delete=models.DO_NOTHING,
    #                                null=True, blank=True, related_name="submission_updated_by")
    # created_date = models.DateTimeField(auto_now_add=True)
    # updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Submission {self.id} for Assignment {self.assignment_id} by Student {self.student_id}"

# Grades of students submissions
class SubmissionGrade(BaseModel):
    submission = models.ForeignKey('Submission', on_delete=models.CASCADE)
    grade = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, blank=True)
    graded_by = models.ForeignKey(
        'staff.Teacher', on_delete=models.DO_NOTHING, null=True, blank=True)
    feedback = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Grade {self.grade} for Submission {self.submission_id}"
