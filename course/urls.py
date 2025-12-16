from django.urls import path, include
from course import views

from rest_framework.routers import DefaultRouter

router = DefaultRouter(trailing_slash=False)

router.register("courses", views.CourseViewSet, basename="courses")
router.register("mx-courses", views.CourseMixinViewSet, basename="mx-courses")


urlpatterns = [
    path('fbv/courses', views.courses),
    path('fbv/courses/<int:id>', views.course_detail),
    path('fbv/courses/<int:id>/<str:action>', views.course_actions),

    path('cbv/courses', views.CourseListCreateView.as_view()),
    path('cbv/courses/<int:id>', views.CourseDetailView.as_view()),

    path('gv/courses', views.CourseListCreateView.as_view()),
    path('gv/courses/<int:pk>',
         views.CourseGenericRetrieveUpdateDestroyView.as_view()),
    path("vs/", include(router.urls))
]
