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

    def __str__(self):
        return f"{self.title} (Course: {self.course_id})"

# Submissions done by students
class Submission(BaseModel):
    STATUS_CHOICES = (
        ("s", "Submitted"),
        ("l", "Late"),
        ("g", "Graded"),
    )

    assignment = models.ForeignKey('Assignment', on_delete=models.CASCADE)
    student = models.ForeignKey('students.Student', on_delete=models.CASCADE)
    file_url = models.CharField(max_length=255)
    submitted_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=1, choices=STATUS_CHOICES, default="s")

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


class QuestionCategory(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name if self.name else f"Category {self.id}"


class Exam(models.Model):
    course = models.ForeignKey('course.Course', on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    duration = models.DurationField(null=True, blank=True)
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)
    total_marks = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.title if self.title else f"Exam {self.id}"


class ExamQuestion(models.Model):
    QUESTION_TYPE_CHOICES = (
        ("s", "Single Choice"),
        ("m", "Multiple Choice"),
        ("t", "Text"),
    )

    category = models.ForeignKey('QuestionCategory', on_delete=models.SET_NULL, null=True, blank=True)
    question_text = models.TextField()
    question_type = models.CharField(max_length=20, choices=QUESTION_TYPE_CHOICES)
    marks = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f"Question {self.id} ({self.question_type})"


class QuestionOption(models.Model):
    question = models.ForeignKey('ExamQuestion', on_delete=models.CASCADE)
    option_code = models.CharField(max_length=4, blank=True, null=True)
    option_text = models.TextField()
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return f"Option {self.option_code}: {self.option_text[:50]}"


class ExamQuestionMap(models.Model):
    exam = models.ForeignKey('Exam', on_delete=models.CASCADE)
    question = models.ForeignKey('ExamQuestion', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('exam', 'question')

    def __str__(self):
        return f"Exam {self.exam_id} - Question {self.question_id}"


class ExamSubmission(models.Model):
    exam = models.ForeignKey('Exam', on_delete=models.CASCADE, null=True, blank=True)
    student = models.ForeignKey('students.Student', on_delete=models.CASCADE, null=True, blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('exam', 'student')

    def __str__(self):
        return f"Submission for Exam {self.exam_id} by Student {self.student_id}"


class ExamAnswer(models.Model):
    exam_submission = models.ForeignKey('ExamSubmission', on_delete=models.CASCADE, null=True, blank=True)
    question = models.ForeignKey('ExamQuestion', on_delete=models.CASCADE, null=True, blank=True)
    answer_text = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Answer for Question {self.question_id} in Submission {self.exam_submission_id}"


class ExamAnswerOption(models.Model):
    answer = models.ForeignKey('ExamAnswer', on_delete=models.CASCADE)
    option = models.ForeignKey('QuestionOption', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('answer', 'option')

    def __str__(self):
        return f"Answer {self.answer_id} - Option {self.option_id}"


class ExamReview(models.Model):
    exam_submission = models.ForeignKey('ExamSubmission', on_delete=models.CASCADE)
    score = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    graded_by = models.ForeignKey('staff.Teacher', on_delete=models.SET_NULL, null=True, blank=True)
    feedback = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Review for Submission {self.exam_submission_id} - Score: {self.score}"


