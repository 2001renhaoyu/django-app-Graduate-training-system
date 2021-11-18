from django.http import HttpResponse
from django.shortcuts import render
from reportlab.pdfgen import canvas

from polls.models import *
from django.http import HttpResponseRedirect
import os

# Create your views here.


def login(request):
    if request.session.get('is_login'):
        id=request.session.get('log_id')
        passwd=request.session.get('log_pwd')
        user_type=request.session.get('log_type')
        if user_type=='管理员':
            return HttpResponseRedirect('/manager/manager_own')
        elif user_type=='学生':
            return HttpResponseRedirect('/student')
        elif user_type=='老师':
            return HttpResponseRedirect('/teacher')
        else:
            pass
    else:
        return render(request, "login.html", {})

def check_login(request):
    id=request.POST.get('log_id')
    passwd=request.POST.get('log_pwd')
    user_set=Users.objects.filter(log_id=id,log_pwd=passwd)
    count= user_set.count()
    if count==1:
        request.session['log_id']=id
        request.session['log_pwd']=passwd
        request.session['log_type']=user_set[0].log_type
        request.session['is_login']=True
        user_type=user_set[0].log_type
        if user_type=='管理员':
            return HttpResponseRedirect('/manager/manager_own')
        elif user_type=='学生':
            return HttpResponseRedirect('/student')
        elif user_type=='老师':
            return HttpResponseRedirect('/teacher')
        else:
            pass
    else:
        return HttpResponse("""
        <script>
        alert('账号/密码错误');
        window.location='/';
        </script>
        """)


def teacher_index(request):
    return render(request, "teacher/teacher_index.html")


def teacher_myProject(request):
    pro_list=Project.objects.filter(pro_tutor_id='d001')
    ip_list=[]
    for pro in pro_list:
        t_list=Identifyproject.objects.filter(ip_pro_id=pro.pro_id)
        ip_list+=t_list
    return render(request, "teacher/teacher_myProject.html",{'pro_list':pro_list,
                                                             'ip_list':ip_list})


def teacher_test(request):
    return render(request, "teacher/teacher_assistant_volunteer_apply.html", {})


def teacher_assistant_volunteer_apply(request):
    return render(request, "teacher/teacher_assistant_volunteer_apply.html", {})


def student_index(request):
    return render(request, 'student/student_index.html', {})


def student_assistant_volunteer_apply(request):
    return render(request, 'student/student_assistant_volunteer_apply.html', {'assistantVolunteer':1})


def student_assistant_volunteer_work(request):
    return render(request, 'student/student_assistant_volunteer_work.html', {})


def student_assistant_volunteer_export(request):
    return render(request, 'student/student_assistant_volunteer_export.html', {})


def student_myProject(request):
    ip_list = Identifyproject.objects.filter(ip_stu_id='s001')
    return render(request, 'student/student_myProject.html', {'ip_list': ip_list})

def student_identify_project(request):
    return render(request, 'student/student_identify_project.html', {})

def post_identify_project_form(request):
    myFile = request.FILES.get("evidence", None)  # 获取上传的文件，如果没有文件，则默认为None
    if not myFile:
        return HttpResponse("no files for upload!")
    destination = open(os.path.join('files','s002' + '_' + myFile.name), 'wb+')  # 打开特定的文件进行二进制的写操作
    for chunk in myFile.chunks():  # 分块写入文件
        destination.write(chunk)
    destination.close()
    ip=Identifyproject(
        ip_stu_id='s002',
        ip_pro_id=request.POST.get('pro_id'),
        ip_job_content=request.POST.get('job_content'),
        ip_begintime=request.POST.get('begin_time'),
        ip_endtime=request.POST.get('end_time'),
        ip_funds=request.POST.get('pro_funds'),
        ip_status=0
    )
    ip.save()
    return render(request, 'student/student_index.html', {'main_content': '提交成功'})


def show_student_activity(request):
    student_id=request.session.get('log_id')
    lists = Academicactivity.objects.all().filter(aca_student_id=student_id)
    return render(request, 'student/student_academic_activity.html', {'activity_list': lists,'have_list':True})


def student_activity_form(request):
    return render(request, 'student/student_academic_activity.html', {'have_list':False})


def post_academic_activity_form(request):
    myFile = request.FILES.get("evidence", None)  # 获取上传的文件，如果没有文件，则默认为None

    if not myFile:
        return HttpResponse("no files for upload!")
    id=request.session.get('log_id')
    if not os.path.exists('files/'+id):
        os.makedirs('files/'+id)
    destination = open(os.path.join("files",id , myFile.name), 'wb+')  # 打开特定的文件进行二进制的写操作
    for chunk in myFile.chunks():  # 分块写入文件
        destination.write(chunk)
    destination.close()
    a_activity = Academicactivity(
        aca_student_id=id,
        aca_activity_id=request.POST.get('act_id'),
        aca_activity_name=request.POST.get('act_name'),
        aca_activity_location=request.POST.get('act_location'),
        aca_activity_date=request.POST.get('act_date'),
        aca_report_name_zh=request.POST.get('act_report_zh'),
        aca_report_name_en=request.POST.get('act_report_en'),
        aca_extra=request.POST.get('act_extra'),
        aca_evidentiary_material=os.path.join("files",id , myFile.name),
        aca_audit_situation='审核中'
    )
    a_activity.save()

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


@csrf_exempt
def manager_users_add(request):
    return render(request, 'manager/manager_users_add.html', {})


@csrf_exempt
def manager_users_delete(request):
    return render(request, 'manager/manager_users_delete.html', {})


@csrf_exempt
def manager_users_alter(request):
    return render(request, 'manager/manager_users_alter.html', {})


@csrf_exempt
def manager_users_search(request):
    return render(request, 'manager/manager_users_search.html', {})

def manager_courses_add(request):
    return render(request, 'manager/manager_courses_add.html', {})

def manager_courses_delete(request):
    return render(request, 'manager/manager_courses_delete.html', {})

def manager_courses_alter(request):
    return render(request, 'manager/manager_courses_alter.html', {})

def manager_courses_search(request):
    return render(request, 'manager/manager_courses_search.html', {})

def manager_projects_add(request):
    return render(request, 'manager/manager_projects_add.html', {})

def manager_projects_delete(request):
    return render(request, 'manager/manager_projects_delete.html', {})

def manager_projects_alter(request):
    return render(request, 'manager/manager_projects_alter.html', {})

def manager_projects_search(request):
    return render(request, 'manager/manager_projects_search.html', {})


def manager_project_identify(request):
    ip_list = Identifyproject.objects.filter(ip_status=0)
    return render(request, 'manager/manager_project_identify.html', {'ip_list':ip_list})


def manager_academic_activity_add(request):
    return render(request, 'manager/manager_academic_activity_add.html', {})

def manager_academic_activity_delete(request):
    return render(request, 'manager/manager_academic_activity_delete.html', {})

def manager_academic_activity_alter(request):
    return render(request, 'manager/manager_academic_activity_alter.html', {})

def manager_academic_activity_search(request):
    return render(request, 'manager/manager_academic_activity_search.html', {})

def manager_student_basic_information(request):
    return render(request, 'manager/manager_student_basic_information.html', {})