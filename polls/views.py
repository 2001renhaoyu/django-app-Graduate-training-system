from django.shortcuts import render
from polls.models import *
from polls import academic_activity


# Create your views here.


def login(request):
    return render(request, "login.html", {})


def teacher_index(request):
    return render(request, "teacher/teacher_index.html")


def teacher_project(request):
    return render(request, "teacher/teacher_project.html")


def teacher_test(request):
    return render(request, "teacher/teacher_assistant_volunteer_apply.html", {})


def teacher_assistant_volunteer_apply(request):
    return render(request, "teacher/teacher_assistant_volunteer_apply.html", {})


def student_index(request):
    return render(request, 'student/student_index.html', {})


def student_assistant_volunteer_apply(request):
    return render(request, 'student/student_assistant_volunteer_apply', {})


def student_assistant_volunteer_work(request):
    return render(request, 'student/student_assistant_volunteer_work', {})


def student_assistant_volunteer_export(request):
    return render(request, 'student/student_assistant_volunteer_export', {})


def student_myproject(request):
    ip_list = Identifyproject.objects.filter(ip_stu_id='s001')
    return render(request, 'student/student_myproject.html', {'ip_list': ip_list})


def show_student_activity(request):
    lists = academic_activity.get_academic_activity_list('s002')
    return render(request, 'student/student_academic_activity.html', {'activity_list': lists})


def student_activity_form(request):
    return render(request, 'student/student_academic_activity.html', {'activity_list': None})


# manager
def manager_index(request):
    return render(request, 'manager/manager_index.html', {})


def manager_users_add(request):
    return render(request, 'manager/manager_users_add.html', {})
