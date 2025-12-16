from django.db.models import Count
from rest_framework import serializers
from utils.serializer import BaseSerializer
from course import models
from assessment.models import Assignment

from staff.serializer import TeacherMinSerializer



class CourseMinSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Course
        fields = ['id', 'title', 'status']


class CourseSerializer(BaseSerializer):
    total_enrolled_students = serializers.SerializerMethodField(read_only=True)
    total_teachers = serializers.SerializerMethodField(read_only=True)
    total_materials = serializers.SerializerMethodField(read_only=True)
    total_assignments = serializers.SerializerMethodField(read_only=True)
    materials_by_type = serializers.SerializerMethodField(read_only=True)

    class Meta(BaseSerializer.META):
        model = models.Course

    def get_total_enrolled_students(self, instance):
        return instance.enrollment_set.filter(status='a').count()

    def get_total_teachers(self, instance):
        return instance.courseteacher_set.filter(status='a').count()

    def get_total_materials(self, instance):
        return instance.material_set.filter(status='a').count()

    def get_total_assignments(self, instance):
        
        return Assignment.objects.filter(course=instance).count()

    def get_materials_by_type(self, instance):
        
        materials = instance.material_set.filter(
            status='a').values('type').annotate(count=Count('type'))
        return {item['type']: item['count'] for item in materials}


class CourseWithTeachersSerializer(BaseSerializer):
    teachers = serializers.SerializerMethodField(read_only=True)
    total_enrolled_students = serializers.SerializerMethodField(read_only=True)
    total_materials = serializers.SerializerMethodField(read_only=True)
    total_assignments = serializers.SerializerMethodField(read_only=True)
    materials_by_type = serializers.SerializerMethodField(read_only=True)

    class Meta(BaseSerializer.META):
        model = models.Course

    def get_teachers(self, instance):
        
        # Get active course-teacher relationships
        course_teachers = instance.courseteacher_set.filter(status='a')
        teachers = [ct.teacher for ct in course_teachers]
        return TeacherMinSerializer(teachers, many=True).data

    def get_total_enrolled_students(self, instance):
        return instance.enrollment_set.filter(status='a').count()

    def get_total_materials(self, instance):
        return instance.material_set.filter(status='a').count()

    def get_total_assignments(self, instance):
       
        return Assignment.objects.filter(course=instance).count()

    def get_materials_by_type(self, instance):
        materials = instance.material_set.filter(
            status='a').values('type').annotate(count=Count('type'))
        return {item['type']: item['count'] for item in materials}


class CourseTeacherSerializer(BaseSerializer):
    class Meta(BaseSerializer.META):
        model = models.CourseTeacher


class MaterialSerializer(BaseSerializer):
    uploaded_by_name = serializers.SerializerMethodField(read_only=True)

    class Meta(BaseSerializer.META):
        model = models.Material

    def get_uploaded_by_name(self, instance):
        if instance.teacher:
            return f"{instance.teacher.first_name} {instance.teacher.last_name}"
        return None
