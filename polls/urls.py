from django.urls import path

from . import views

urlpatterns = [
    # path('', views.login),
    # path('', views.teacher_test),
    path('',views.teacher_project),
    path('teacher_assistant_volunteer_apply', views.teacher_assistant_volunteer_apply),

]