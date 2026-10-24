"""URL patterns for OnlineCourse."""
from django.urls import path
from . import views

app_name = "onlinecourse"

urlpatterns = [
    path("", views.course_details, name="course_list"),
    path("courses/<int:course_id>/", views.course_details, name="course_details"),
    path("lessons/<int:lesson_id>/submit/", views.submit, name="submit"),
    path("exam-results/<int:submission_id>/", views.show_exam_result, name="show_exam_result"),
]
