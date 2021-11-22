from django.urls import path

from . import views

urlpatterns = [
    path('', views.login),
    path('check_login',views.check_login),
    path('teacher/teacher_achievement_aduit', views.teacher_achievement_aduit),

    # teacher
    path('teacher', views.teacher_index),  # 不能使用的模板页
    path('teacher/teacher_homepage',views.teacher_homepage),
    path('teacher/teacher_assistant_volunteer_apply', views.teacher_assistant_volunteer_apply),
    path('teacher/teacher_assistant_volunteer_select', views.teacher_assistant_volunteer_select),
    path('teacher/post_teacher_assistant_volunteer_select', views.post_teacher_assistant_volunteer_select),
    path('teacher/post_teacher_assistant_volunteer_apply', views.post_teacher_assistant_volunteer_apply),
    path('teacher/end_teacher_assistant_volunteer_apply', views.end_teacher_assistant_volunteer_apply),

    path('teacher/teacher_academic_activity_aduit', views.teacher_academic_activity_aduit),
    path('teacher/teacher_academic_activity_aduit/pass_acticity',views.pass_activity),
    path('teacher/teacher_academic_activity_aduit/no_pass_acticity',views.no_pass_activity),
    path('teacher/head_teacher_academic_activity_aduit', views.head_teacher_academic_activity_aduit),
    path('teacher/head_teacher_academic_activity_aduit/pass_acticity',views.head_pass_activity),
    path('teacher/head_teacher_academic_activity_aduit/no_pass_acticity',views.head_no_pass_activity),
    path('teacher/teacher_myProject', views.teacher_myProject),
    path('teacher/teacher_myProject',views.teacher_myProject),
    path('teacher/teacher_fill_in_funds',views.teacher_fill_in_funds),
    path('teacher/post_fill_in_funds_form',views.post_fill_in_funds_form),
    path('teacher/teacher_achievement_aduit/pass_achievement',views.pass_achievement),
    path('teacher/teacher_achievement_aduit/no_pass_achievement',views.no_pass_achievement),


    # student
    path('student', views.student_index),  # 不能使用的模板页
    path('student/student_assistant_volunteer_apply', views.student_assistant_volunteer_apply),
    path('student/post_student_assistant_volunteer_apply', views.post_student_assistant_volunteer_apply),

    path('student/student_assistant_volunteer_work', views.student_assistant_volunteer_work),
    path('student/student_assistant_volunteer_export', views.student_assistant_volunteer_export),
    path('student/student_homepage', views.student_homepage),
    path('student/show_academic_activity', views.show_student_activity),
    path('student/student_activity_form', views.student_activity_form),
    path('student/student_myProject', views.student_myProject),
    path('student/student_search_project', views.student_search_project),
    path('student/student_identify_project',views.student_identify_project),
    path('student/post_identify_project_form',views.post_identify_project_form),
    path('student/post_academic_activity_form', views.post_academic_activity_form),
    path('student/export_form', views.export_form),
    path('download_evidence',views.download_evidence),
    path('student/ache_test1', views.ache_test1),
    path('student/post_reward_form', views.post_reward_form),
    path('student/student_myAchievements',views.student_myAchievements),

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
    path('manager/manager_student_basic_information_search', views.manager_student_basic_information_search),
    path('manager/manager_tutor_basic_information', views.manager_tutor_basic_information),
    path('manager/manager_tutor_basic_information_search', views.manager_tutor_basic_information_search),
    path('manager/manager_tutor_projects_information_search', views.manager_tutor_projects_information_search),
    path('manager/manager_achievement_aduit',views.manager_achievement_aduit),
    path('manager/manager_achievement_aduit/manager_pass_achievement',views.manager_pass_achievement),
    path('manager/manager_achievement_aduit/manager_no_pass_achievement',views.manager_no_pass_achievement),
    path('manager/manager_course_teacher_basic_information', views.manager_course_teacher_basic_information),
    path('manager/manager_course_teacher_basic_information_search', views.manager_course_teacher_basic_information_search),
    path('manager/manager_head_teacher_basic_information', views.manager_head_teacher_basic_information),
]
