from datetime import date
from rest_framework import serializers
from utils.serializer import BaseSerializer
from staff import models


class TeacherMinSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = models.Teacher
        fields = ['id', 'first_name', 'last_name', 'employee_code', 'full_name']

    def get_full_name(self, instance):
        return f"{instance.first_name} {instance.last_name}"


class TeacherSerializer(BaseSerializer):
    age = serializers.SerializerMethodField(read_only=True)
    total_courses = serializers.SerializerMethodField(read_only=True)
    total_students = serializers.SerializerMethodField(read_only=True)
    total_materials_uploaded = serializers.SerializerMethodField(read_only=True)
    years_of_service = serializers.SerializerMethodField(read_only=True)

    class Meta(BaseSerializer.META):
        model = models.Teacher

    def get_age(self, instance):
        if instance.dob:
            return date.today().year - instance.dob.year
        return None

    def get_total_courses(self, instance):
        from course.models import CourseTeacher
        return CourseTeacher.objects.filter(teacher=instance, status='a').count()

    def get_total_students(self, instance):
        from course.models import CourseTeacher
        from students.models import Enrollment
        # Get all active courses for this teacher
        course_ids = CourseTeacher.objects.filter(
            teacher=instance, status='a'
        ).values_list('course_id', flat=True)
        # Get unique students enrolled in those courses
        return Enrollment.objects.filter(
            course_id__in=course_ids, status='a'
        ).values('student').distinct().count()

    def get_total_materials_uploaded(self, instance):
        from course.models import Material
        return Material.objects.filter(teacher=instance, status='a').count()

    def get_years_of_service(self, instance):
        if instance.date_joined:
            from django.utils import timezone
            delta = timezone.now() - instance.date_joined
            return round(delta.days / 365.25, 1)
        return None


class QualificationSerializer(BaseSerializer):
    class Meta(BaseSerializer.META):
        model = models.Qualification


class UserQualificationSerializer(BaseSerializer):
    class Meta(BaseSerializer.META):
        model = models.UserQualification


class SpecializationSerializer(BaseSerializer):
    class Meta(BaseSerializer.META):
        model = models.Specialization


class UserSpecializationSerializer(BaseSerializer):
    class Meta(BaseSerializer.META):
        model = models.UserSpecialization


class DepartmentSerializer(BaseSerializer):
    class Meta(BaseSerializer.META):
        model = models.Department


class UserDepartmentSerializer(BaseSerializer):
    class Meta(BaseSerializer.META):
        model = models.UserDepartment


class DesignationSerializer(BaseSerializer):
    class Meta(BaseSerializer.META):
        model = models.Designation


class UserDesignationSerializer(BaseSerializer):
    class Meta(BaseSerializer.META):
        model = models.UserDesignation
