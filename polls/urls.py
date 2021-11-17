from django.urls import path

from . import views

urlpatterns = [
    # path('', views.login),
    path('', views.student_index),
    path('student_myproject',views.student_myproject),
    path('teacher_assistant_volunteer_apply', views.teacher_assistant_volunteer_apply),

]