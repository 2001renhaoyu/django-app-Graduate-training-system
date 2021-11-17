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
    path('student/student_identify_project',views.student_identify_project),
    path('student/post_identify_project_form',views.post_identify_project_form),
    path('student/post_academic_activity_form',views.post_academic_activity_form),
    path('student/export_form',views.export_form),

    # manager
    path('manager', views.manager_index),  # 不能使用的模板页
    path('manager/manager_own', views.manager_own),
    path('manager/manager_users_add', views.manager_users_add),
    path('manager/manager_users_delete', views.manager_users_delete),
    path('manager/manager_users_alter', views.manager_users_alter),
    path('manager/manager_users_search', views.manager_users_search),
    path('manager/manager_courses_add', views.manager_courses_add),
    path('manager/manager_courses_delete', views.manager_courses_delete),
    path('manager/manager_courses_alter', views.manager_courses_alter),
    path('manager/manager_courses_search', views.manager_courses_search),
    path('manager/manager_projects_add', views.manager_projects_add),
    path('manager/manager_projects_delete', views.manager_projects_delete),
    path('manager/manager_projects_alter', views.manager_projects_alter),
    path('manager/manager_projects_search', views.manager_projects_search),
]
