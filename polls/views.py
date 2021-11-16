from django.shortcuts import render
# Create your views here.


def teacher_test(request):
    return render(request, "teacher/teacher_assistant_volunteer_apply.html", {})


def teacher_assistant_volunteer_apply(request):
    return render(request, "teacher/teacher_assistant_volunteer_apply.html", {})
