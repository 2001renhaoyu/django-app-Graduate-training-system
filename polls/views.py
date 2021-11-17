from django.shortcuts import render
from polls.models import *
from polls import academic_activity
import os

# Create your views here.


def login(request):
    return render(request, "login.html", {})


def test(request):
    return render(request, "student/student_index.html", {})


# teacher
def teacher_assistant_volunteer_apply(request):
    return render(request, "teacher/teacher_assistant_volunteer_apply.html", {})


# student
def student_index(request):
    return render(request, 'student/student_index.html', {})


def student_assistant_volunteer_apply(request):
    return render(request, 'student/student_assistant_volunteer_apply.html', {'assistantVolunteer': {3}})


def student_assistant_volunteer_work(request):
    return render(request, 'student/student_assistant_volunteer_work.html', {'assistantWork': {0}})


def student_assistant_volunteer_export(request):
    return render(request, 'student/student_assistant_volunteer_export.html', {'assistantWork': {0}})


def show_student_activity(request):
    lists = academic_activity.get_academic_activity_list('s002')
    return render(request, 'student/student_academic_activity.html', {'activity_list': lists})


def student_activity_form(request):
    return render(request, 'student/student_academic_activity.html', {'activity_list': None})


def post_academic_activity_form(request):
    myFile = request.FILES.get("evidence", None)  # 获取上传的文件，如果没有文件，则默认为None

    if not myFile:
        return HttpResponse("no files for upload!")
    destination = open(os.path.join("files",'s002'+'_' + myFile.name), 'wb+')  # 打开特定的文件进行二进制的写操作
    for chunk in myFile.chunks():  # 分块写入文件
        destination.write(chunk)
    destination.close()
    a_activity = Academicactivity(
        aca_student_id='s002',
        aca_activity_id=request.POST.get('act_id'),
        aca_activity_name=request.POST.get('act_name'),
        aca_activity_location=request.POST.get('act_location'),
        aca_activity_date=request.POST.get('act_date'),
        aca_report_name_zh=request.POST.get('act_report_zh'),
        aca_report_name_en=request.POST.get('act_report_en'),
        aca_extra=request.POST.get('act_extra'),
        aca_evidentiary_material=os.path.join("files",'s002'+'_' + myFile.name),
        aca_audit_situation='审核中'
    )
    a_activity.save()
    return render(request,'student/student_index.html',{'main_content':'提交成功'})



# manager
def manager_index(request):
    return render(request, 'manager/manager_index.html', {})


def manager_users_add(request):
    return render(request, 'manager/manager_users_add.html', {})
