from django.urls import path

from . import views

urlpatterns = [
    path('', views.login),
    path('check_login',views.check_login),
    # path('', views.login),

    # teacher
    path('teacher', views.teacher_index),  # 不能使用的模板页
    path('teacher_assistant_volunteer_apply', views.teacher_assistant_volunteer_apply),
    path('teacher/teacher_academic_activity_aduit', views.teacher_academic_activity_aduit),
    path('teacher/teacher_academic_activity_aduit/pass_acticity',views.pass_activity),
    path('teacher/teacher_academic_activity_aduit/no_pass_acticity',views.no_pass_activity),
    path('teacher/teacher_myProject',views.teacher_myProject),


    # student
    path('student', views.student_index),  # 不能使用的模板页
    path('student/student_assistant_volunteer_apply', views.student_assistant_volunteer_apply),
    path('student/student_assistant_volunteer_work', views.student_assistant_volunteer_work),
    path('student/student_assistant_volunteer_export', views.student_assistant_volunteer_export),

    path('student/show_academic_activity', views.show_student_activity),
    path('student/student_activity_form', views.student_activity_form),
    path('student/student_myProject', views.student_myProject),
    path('student/student_search_project', views.student_search_project),
    path('student/student_identify_project',views.student_identify_project),
    path('student/post_identify_project_form',views.post_identify_project_form),
    path('student/post_academic_activity_form', views.post_academic_activity_form),
    path('student/export_form', views.export_form),
    path('download_evidence',views.download_evidence),
    # path('student/ache_test1', views.ache_test1),
    # path('student/post_ache_test1_form', views.post_ache_test1_form),

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
    path('manager/manager_project_identify',views.manager_project_identify),
    path('manager/manager_project_identify/pass_project', views.pass_project),
    path('manager/manager_project_identify/no_pass_project', views.pass_project),
    path('manager/manager_academic_activity_add', views.manager_academic_activity_add),
    path('manager/manager_academic_activity_delete', views.manager_academic_activity_delete),
    path('manager/manager_academic_activity_alter', views.manager_academic_activity_alter),
    path('manager/manager_academic_activity_search', views.manager_academic_activity_search),
    path('manager/manager_student_basic_information', views.manager_student_basic_information),
]
