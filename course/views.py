from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from course import models
from course import serializer
# Create your views here.


@api_view(["GET", "POST"])
def courses(request):
    courses = models.Course.objects.all()
    se = serializer.CourseSerializer(courses, many=True)
    return Response(data=se.data, status=status.HTTP_200_OK)
