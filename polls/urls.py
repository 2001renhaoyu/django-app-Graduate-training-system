from django.urls import path

from . import views

urlpatterns = [
    path('', views.login),
    # path('', views.test),

    # teacher
    path('teacher', views.student_index),  # 不能使用的模板页
    path('teacher_assistant_volunteer_apply', views.teacher_assistant_volunteer_apply),

    # student
    path('student', views.student_index),  # 不能使用的模板页
    path('student/student_assistant_volunteer_apply', views.student_assistant_volunteer_apply),
    path('student/student_assistant_volunteer_work', views.student_assistant_volunteer_work),
    path('student/student_assistant_volunteer_export', views.student_assistant_volunteer_export),
    path('student/show_academic_activity', views.show_student_activity),
    path('student/student_activity_form', views.student_activity_form),
    path('student/student_myproject', views.student_myproject),
    path('student/post_academic_activity_form',views.post_academic_activity_form),

    # manager
    path('manager', views.manager_index),  # 不能使用的模板页
    path('manager/manager_own', views.manager_own),
    path('manager/manager_users_add', views.manager_users_add),
    path('manager/manager_users_delete', views.manager_users_delete),
    path('manager/manager_users_alter', views.manager_users_alter),
    path('manager/manager_users_search', views.manager_users_search),
]
