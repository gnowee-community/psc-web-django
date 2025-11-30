from datetime import date
from rest_framework import serializers
from course.models import Course
from course.serializer import CourseMinSerializer
from utils.models import User
from utils.serializer import BaseSerializer
from students import models


class StudentMinSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = models.Student
        fields = ['id', 'first_name', 'last_name', 'full_name']

    def get_full_name(self, instance):
        return f"{instance.first_name} {instance.last_name}"


class StudentSerializer(BaseSerializer):
    age = serializers.SerializerMethodField(read_only=True)
    total_courses = serializers.SerializerMethodField(read_only=True)
    total_completed_courses = serializers.SerializerMethodField(read_only=True)
    enrollment_status_summary = serializers.SerializerMethodField(read_only=True)

    class Meta(BaseSerializer.META):
        model = models.Student
        fields = "__all__"

    def get_age(self, instance):
        return date.today().year - instance.date_of_birth.year

    def get_total_courses(self, instance):
        return instance.enrollment_set.filter(status='a').count()

    def get_total_completed_courses(self, instance):
        return instance.enrollment_set.filter(status='c').count()

    def get_enrollment_status_summary(self, instance):
        from django.db.models import Count
        summary = instance.enrollment_set.values('status').annotate(count=Count('status'))
        return {item['status']: item['count'] for item in summary}


class StudentWithCoursesSerializer(BaseSerializer):
    age = serializers.SerializerMethodField(read_only=True)
    courses = serializers.SerializerMethodField(read_only=True)
    total_courses = serializers.SerializerMethodField(read_only=True)
    total_completed_courses = serializers.SerializerMethodField(read_only=True)
    enrollment_status_summary = serializers.SerializerMethodField(read_only=True)

    class Meta(BaseSerializer.META):
        model = models.Student
        fields = "__all__"

    def get_age(self, instance):
        return date.today().year - instance.date_of_birth.year

    def get_courses(self, instance):
        # Get active enrollments
        enrollments = instance.enrollment_set.filter(status='a')
        courses = [enrollment.course for enrollment in enrollments]
        return CourseMinSerializer(courses, many=True).data

    def get_total_courses(self, instance):
        return instance.enrollment_set.filter(status='a').count()

    def get_total_completed_courses(self, instance):
        return instance.enrollment_set.filter(status='c').count()

    def get_enrollment_status_summary(self, instance):
        from django.db.models import Count
        summary = instance.enrollment_set.values('status').annotate(count=Count('status'))
        return {item['status']: item['count'] for item in summary}


class EnrollmentSerializer(BaseSerializer):
    student = StudentMinSerializer(read_only=True)
    course = CourseMinSerializer(read_only=True)
    enrollment_duration = serializers.SerializerMethodField(read_only=True)
    is_active = serializers.SerializerMethodField(read_only=True)

    class Meta(BaseSerializer.META):
        model = models.Enrollment
        fields = "__all__"

    def get_enrollment_duration(self, instance):
        from django.utils import timezone
        delta = timezone.now() - instance.enrollment_date
        return delta.days

    def get_is_active(self, instance):
        return instance.status == 'a'
