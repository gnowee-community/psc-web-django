from datetime import date
from rest_framework import serializers
from course.models import Course
from course.serializer import CourseSerializer
from utils.models import User
from students import models


class StudentSerializer(serializers.Serializer):
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
    id = serializers.IntegerField(read_only=True)
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    first_name = serializers.CharField(max_length=100)
    last_name = serializers.CharField(max_length=100)
    date_of_birth = serializers.DateField(required=False, allow_null=True)
    gender = serializers.ChoiceField(choices=GENDER_CHOICES)
    phone_number = serializers.CharField(max_length=10)
    emergency_contact_person_name = serializers.CharField(max_length=100)
    emergency_contact_number = serializers.CharField(max_length=10)
    status = serializers.ChoiceField(choices=STATUS_CHOICES)
    profile_picture = serializers.CharField(
        max_length=10, required=False, allow_null=True)
    date_joined = serializers.DateField()

    def create(self, validated_data):
        return models.Student.objects.create(**validated_data)

    def update(self, instance, validated_data):
        # instance.user__id = validated_data.get("user",instance.user.id)

        for k, v in validated_data.items():
            setattr(instance, k, v)
        instance.save()
        return instance


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username"]


class StudentModelSerializer(serializers.ModelSerializer):
    age = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = models.Student
        fields = "__all__"
        read_only_fields = ["id", "created_by",
                            "updated_by", "created_date", "updated_date"]

    def get_age(self, instance):
        return date.today().year - instance.date_of_birth.year


class StudentModelNestedSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = models.Student
        fields = "__all__"
        read_only_fields = ["id", "created_by",
                            "updated_by", "created_date", "updated_date"]

    def create(self, validated_data):
        user_data = validated_data.pop("user")
        user = User.objects.create(**user_data)
        return models.Student.objects.create(user=user, **validated_data)


class StudentAndModelNestedSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    courses = CourseSerializer(read_only=True, many=True)

    class Meta:
        model = models.Student
        fields = "__all__"
        read_only_fields = ["id", "created_by",
                            "updated_by", "created_date", "updated_date"]

    def create(self, validated_data):
        user_data = validated_data.pop("user")
        user = User.objects.create(**user_data)
        return models.Student.objects.create(user=user, **validated_data)