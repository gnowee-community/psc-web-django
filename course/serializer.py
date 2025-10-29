from rest_framework import serializers
from course import models

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Course
        fields = "__all__"
        read_only_fields = ["id", "created_by",
                            "updated_by", "created_date", "updated_date"]
    