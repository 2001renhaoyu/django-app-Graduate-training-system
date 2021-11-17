from django.shortcuts import render
# Create your views here.


def login(request):
    return render(request, "login.html", {})

def teacher_index(request):
    return render(request,"teacher/teacher_index.html")

def teacher_project(request):
    return render(request,"teacher/teacher_project.html")

def teacher_test(request):
    return render(request, "teacher/teacher_assistant_volunteer_apply.html", {})


def teacher_assistant_volunteer_apply(request):
    return render(request, "teacher/teacher_assistant_volunteer_apply.html", {})
