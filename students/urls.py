from django.urls import path
from students import views

urlpatterns = [
    path("hello-world", views.hello_world),
    path("hello-world/<int:id>", views.hello_world)
]
