from django.urls import path, include
from course import views

urlpatterns = [
    path('fbv/courses', views.courses),
    path('fbv/courses/<int:id>', views.course_detail),
    path('fbv/courses/<int:id>/<str:action>', views.course_actions),
]
