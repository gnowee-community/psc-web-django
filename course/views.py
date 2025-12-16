from django.shortcuts import render
from rest_framework import views
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework import status
from course import models
from course import serializer
from students.models import Student
from students.serializer import StudentMinSerializer
# Create your views here.


@api_view(["GET", "POST"])
def courses(request):
    if request.method == "GET":
        courses = models.Course.objects.all()
        se = serializer.CourseSerializer(courses, many=True)
        return Response(data=se.data, status=status.HTTP_200_OK)
    else:
        se = serializer.CourseSerializer(data=request.data)
        if not se.is_valid():
            return Response(data=se.errors, status=status.HTTP_400_BAD_REQUEST)
        obj = se.save()
        _se = serializer.CourseSerializer(obj)
        return Response(data=_se.data, status=status.HTTP_201_CREATED)


@api_view(["GET", "PUT", "PATCH", "DELETE"])
def course_detail(request, id):
    if request.method == "GET":
        try:
            model = models.Course.objects.get(id=id)
            se = serializer.CourseSerializer(model)
            return Response(data=se.data, status=status.HTTP_200_OK)
        except models.Course.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    elif request.method == "PUT":
        try:
            model = models.Course.objects.get(id=id)
            se = serializer.CourseSerializer(model, data=request.data)
            if not se.is_valid():
                return Response(data=se.errors, status=status.HTTP_400_BAD_REQUEST)
            se.save()
            return Response(data=se.data, status=status.HTTP_200_OK)
        except models.Course.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    elif request.method == "PATCH":
        try:
            model = models.Course.objects.get(id=id)
            se = serializer.CourseSerializer(
                model, data=request.data, partial=True)
            if not se.is_valid():
                return Response(data=se.errors, status=status.HTTP_400_BAD_REQUEST)
            se.save()
            return Response(data=se.data, status=status.HTTP_200_OK)
        except models.Course.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    elif request.method == "DELETE":
        try:
            model = models.Course.objects.get(id=id)
            model.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except models.Course.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(["GET"])
def course_actions(request, id, action):
    if action == "students":
        students = Student.objects.filter(enrollment__course__id=id)
        se = StudentMinSerializer(students, many=True)
        return Response(data=se.data, status=status.HTTP_200_OK)
    return Response(status=status.HTTP_200_OK)


class CourseListCreateView(views.APIView):
    def get(self, request):
        courses = models.Course.objects.all()
        se = serializer.CourseSerializer(courses, many=True)
        return Response(data=se.data, status=status.HTTP_200_OK)

    def post(self, request):
        se = serializer.CourseSerializer(data=request.data)
        if not se.is_valid():
            return Response(data=se.errors, status=status.HTTP_400_BAD_REQUEST)
        obj = se.save()
        _se = serializer.CourseSerializer(obj)
        return Response(data=_se.data, status=status.HTTP_201_CREATED)


class CourseDetailView(views.APIView):

    def get(self, request, id):
        try:
            model = models.Course.objects.get(id=id)
            se = serializer.CourseSerializer(model)
            return Response(data=se.data, status=status.HTTP_200_OK)
        except models.Course.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self, request, id):
        try:
            model = models.Course.objects.get(id=id)
            se = serializer.CourseSerializer(model, data=request.data)
            if not se.is_valid():
                return Response(data=se.errors, status=status.HTTP_400_BAD_REQUEST)
            se.save()
            return Response(data=se.data, status=status.HTTP_200_OK)
        except models.Course.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def patch(self, request, id):
        try:
            model = models.Course.objects.get(id=id)
            se = serializer.CourseSerializer(
                model, data=request.data, partial=True)
            if not se.is_valid():
                return Response(data=se.errors, status=status.HTTP_400_BAD_REQUEST)
            se.save()
            return Response(data=se.data, status=status.HTTP_200_OK)
        except models.Course.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, id):
        try:
            model = models.Course.objects.get(id=id)
            model.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except models.Course.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


class CourseGenericListCreateView(ListCreateAPIView):
    queryset = models.Course.objects.all()
    serializer_class = serializer.CourseSerializer


class CourseGenericRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = models.Course.objects.all()
    serializer_class = serializer.CourseSerializer


class CourseViewSet(ModelViewSet):
    queryset = models.Course.objects.all()
    serializer_class = serializer.CourseSerializer

    @action(methods=["GET"], detail=True)
    def students(self, request, pk):
        students = Student.objects.filter(enrollment__course__id=pk)
        se = StudentMinSerializer(students, many=True)
        return Response(data=se.data, status=status.HTTP_200_OK)


class CourseMixinViewSet(GenericViewSet, ListModelMixin, RetrieveModelMixin):
    queryset = models.Course.objects.all()
    serializer_class = serializer.CourseSerializer

    @action(methods=["GET"], detail=True)
    def students(self, request, pk):
        students = Student.objects.filter(enrollment__course__id=pk)
        se = StudentMinSerializer(students, many=True)
        return Response(data=se.data, status=status.HTTP_200_OK)
