from django.http import HttpResponse
from django.shortcuts import render
from reportlab.pdfgen import canvas

from polls.models import *
from polls import academic_activity
import os



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

    return render(request,'student/student_index.html',{'main_content':'提交成功'})


def export_form(request):
    # Create the HttpResponse object with the appropriate PDF headers.
    response = HttpResponse()
    response['Content-Disposition'] = 'attachment; filename=hello.pdf'

    # Create the PDF object, using the response object as its "file."
    p = canvas.Canvas(response)

    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.
    p.drawString(100, 100, "Hello world.")

    # Close the PDF object cleanly, and we're done.
    p.showPage()
    p.save()
    return response


# manager
def manager_index(request):
    return render(request, 'manager/manager_index.html', {})

def manager_own(request):
    return render(request, 'manager/manager_own.html', {})

def manager_users_add(request):
    return render(request, 'manager/manager_users_add.html', {})

def manager_users_delete(request):
    return render(request, 'manager/manager_users_delete.html', {})

def manager_users_alter(request):
    return render(request, 'manager/manager_users_alter.html', {})

def manager_users_search(request):
    return render(request, 'manager/manager_users_search.html', {})

def manager_courses_add(request):
    return render(request, 'manager/manager_users_add.html', {})

def manager_courses_delete(request):
    return render(request, 'manager/manager_users_delete.html', {})

def manager_courses_alter(request):
    return render(request, 'manager/manager_users_alter.html', {})

def manager_courses_search(request):
    return render(request, 'manager/manager_users_search.html', {})

def manager_projects_add(request):
    return render(request, 'manager/manager_users_add.html', {})

def manager_projects_delete(request):
    return render(request, 'manager/manager_users_delete.html', {})

def manager_projects_alter(request):
    return render(request, 'manager/manager_users_alter.html', {})

def manager_projects_search(request):
    return render(request, 'manager/manager_users_search.html', {})
