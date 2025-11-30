from rest_framework import serializers
from utils.serializer import BaseSerializer
from assessment import models


class AssignmentSerializer(BaseSerializer):
    total_submissions = serializers.SerializerMethodField(read_only=True)
    graded_submissions = serializers.SerializerMethodField(read_only=True)
    pending_submissions = serializers.SerializerMethodField(read_only=True)
    is_overdue = serializers.SerializerMethodField(read_only=True)
    average_grade = serializers.SerializerMethodField(read_only=True)

    class Meta(BaseSerializer.META):
        model = models.Assignment
        fields = "__all__"

    def get_total_submissions(self, instance):
        return instance.submission_set.count()

    def get_graded_submissions(self, instance):
        return instance.submission_set.filter(status='g').count()

    def get_pending_submissions(self, instance):
        return instance.submission_set.exclude(status='g').count()

    def get_is_overdue(self, instance):
        if instance.due_date:
            from django.utils import timezone
            return timezone.now() > instance.due_date
        return False

    def get_average_grade(self, instance):
        from django.db.models import Avg
        submissions = instance.submission_set.all()
        avg = models.SubmissionGrade.objects.filter(
            submission__in=submissions
        ).aggregate(avg_grade=Avg('grade'))['avg_grade']
        return round(float(avg), 2) if avg else None


class SubmissionSerializer(BaseSerializer):
    is_graded = serializers.SerializerMethodField(read_only=True)
    days_until_due = serializers.SerializerMethodField(read_only=True)
    submission_status_display = serializers.SerializerMethodField(read_only=True)

    class Meta(BaseSerializer.META):
        model = models.Submission
        fields = "__all__"

    def get_is_graded(self, instance):
        return instance.status == 'g'

    def get_days_until_due(self, instance):
        if instance.assignment.due_date:
            from django.utils import timezone
            delta = instance.assignment.due_date - instance.submitted_date
            return delta.days
        return None

    def get_submission_status_display(self, instance):
        status_dict = dict(models.Submission.STATUS_CHOICES)
        return status_dict.get(instance.status, instance.status)


class SubmissionGradeSerializer(BaseSerializer):
    class Meta(BaseSerializer.META):
        model = models.SubmissionGrade
        fields = "__all__"


class QuestionCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.QuestionCategory
        fields = "__all__"


class ExamSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Exam
        fields = "__all__"


class ExamQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ExamQuestion
        fields = "__all__"


class QuestionOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.QuestionOption
        fields = "__all__"


class ExamQuestionMapSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ExamQuestionMap
        fields = "__all__"


class ExamSubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ExamSubmission
        fields = "__all__"


class ExamAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ExamAnswer
        fields = "__all__"


class ExamAnswerOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ExamAnswerOption
        fields = "__all__"


class ExamReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ExamReview
        fields = "__all__"
