from django.urls import path

from . import views

urlpatterns = [
    path('', views.teacher_test, name='teacher_test'),
    path('', views.teacher_assistant_volunteer_apply, name='teacher_assistant_volunteer_apply'),
]