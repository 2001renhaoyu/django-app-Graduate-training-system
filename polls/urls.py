from django.urls import path

from . import views

urlpatterns = [
    # path('', views.login),
    path('', views.teacher_test),
    path('teacher_assistant_volunteer_apply',
         views.teacher_assistant_volunteer_apply),

    # student
    path('student', views.student_index),
    path('student/show_academic_activity', views.show_student_avtivity),
    path('student/student_activity_form', views.student_activity_form),

    # manager
    path('manager/')
]
