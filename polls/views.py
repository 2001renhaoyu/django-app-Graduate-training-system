from django.forms import model_to_dict
from django.http import HttpResponse, FileResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from reportlab.pdfgen import canvas

from polls.models import *
from django.http import HttpResponseRedirect
import os


# Create your views here.


def login(request):
    if request.session.get('is_login'):
        id = request.session.get('log_id')
        passwd = request.session.get('log_pwd')
        user_type = request.session.get('log_type')
        if user_type == '管理员':
            return HttpResponseRedirect('/manager/manager_own')
        elif user_type == '学生':
            return HttpResponseRedirect('/student')
        elif user_type == '老师':
            return HttpResponseRedirect('/teacher')
        else:
            pass
    else:
        return render(request, "login.html", {})


def check_login(request):
    id = request.POST.get('log_id')
    passwd = request.POST.get('log_pwd')
    user_set = Users.objects.filter(log_id=id, log_pwd=passwd)
    count = user_set.count()
    if count == 1:
        request.session['log_id'] = id
        request.session['log_pwd'] = passwd
        request.session['log_type'] = user_set[0].log_type
        request.session['is_login'] = True
        user_type = user_set[0].log_type
        if user_type == '管理员':
            return HttpResponseRedirect('/manager/manager_own')
        elif user_type == '学生':
            return HttpResponseRedirect('/student')
        elif user_type == '老师':
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
    pro_tutor_id = request.session.get('log_id')
    pro_list = Project.objects.filter(pro_tutor_id=pro_tutor_id)
    ip_list = []
    for pro in pro_list:
        t_list = Identifyproject.objects.filter(ip_pro_id=pro.pro_id)
        ip_list += t_list
    return render(request, "teacher/teacher_myProject.html", {'pro_list': pro_list,
                                                              'ip_list': ip_list})


def teacher_fill_in_funds(request):
    pro_tutor_id = request.session.get('log_id')
    teacher = Teacher.objects.get(teacher_id=pro_tutor_id)
    pro_list = Project.objects.filter(pro_tutor_id=pro_tutor_id)
    ip_list = []
    for pro in pro_list:
        t_list = Identifyproject.objects.filter(ip_pro_id=pro.pro_id,
                                                ip_mid_status=0)
        ip_list += t_list
    return render(request, "teacher/teacher_fill_in_funds.html", {'ip_list': ip_list,
                                                                  'teacher': teacher})


def post_fill_in_funds_form(request):
    pro_id = request.POST.get('pro_id')
    stu_id = request.POST.get('stu_id')
    pro_funds = float(request.POST.get('pro_funds'))
    teacher_id=request.session.get('log_id')
    try:
        ip = Identifyproject.objects.get(ip_pro_id=pro_id,
                                         ip_stu_id=stu_id)
        ip.ip_funds = pro_funds
        ip.ip_mid_status = 1
        teacher=Teacher.objects.get(teacher_id=teacher_id)
        t_funds=float(teacher.teacher_funds)
        t=t_funds-pro_funds
        if(t >= 0):
            teacher.teacher_funds = t
            ip.save()
            teacher.save()
            return HttpResponseRedirect('/teacher/teacher_fill_in_funds')
        else:
            return HttpResponseRedirect('/teacher/teacher_fill_in_funds')
    except:
        return HttpResponseRedirect('/teacher/teacher_fill_in_funds')


def teacher_test(request):
    return render(request, "teacher/teacher_assistant_volunteer_apply.html", {})


def teacher_assistant_volunteer_apply(request):
    return render(request, "teacher/teacher_assistant_volunteer_apply.html", {})


def teacher_academic_activity_aduit(request):
    id = request.session.get('log_id')
    result_set1 = Teacher.objects.get(teacher_id=id).student_set.all()
    result_set2 = []
    for a_stu in result_set1:
        l = list(Student.objects.get(stu_id=a_stu.stu_id).academicactivity_set.all())
        l = [model_to_dict(i)
             for i in l
             ]
        for t in l:
            t['student_name'] = a_stu.stu_name
        result_set2 += l
    return render(request, 'teacher/teacher_academic_activity_aduit.html', {'activity_list': result_set2})


def head_teacher_academic_activity_aduit(request):
    id = request.session.get('log_id')
    a_teacher = Teacher.objects.get(teacher_id=id)
    if a_teacher.teacher_status not in [3, 5, 6, 7]:
        return render(request, 'teacher/head_teacher_academic_activity_aduit.html', {'is_head_teacher': False})
    else:
        subject = a_teacher.teacher_subject
        result_set1 = Student.objects.filter(stu_subject=subject)
        result_set2 = []
        for a_stu in result_set1:
            l = list(Student.objects.get(stu_id=a_stu.stu_id).academicactivity_set.all())
            l = [model_to_dict(i)
                 for i in l
                 ]
            for t in l:
                t['student_name'] = a_stu.stu_name
            result_set2 += l
        return render(request, 'teacher/head_teacher_academic_activity_aduit.html',
                      {'is_head_teacher': True, 'activity_list': result_set2})

    return render(requset, 'teacher/teacher_academic_activity_aduit.html', {'activity_list': result_set2})



def pass_activity(request):
    act_id = request.GET.get('act_id')
    a_act = Academicactivity.objects.get(aca_activity_id=act_id)
    if a_act.aca_audit_situation == '审核中':
        a_act.aca_audit_situation = '学科负责人审核通过'
        a_act.save()
    else:
        a_act.aca_audit_situation='通过'
        a_act.save()
    return HttpResponseRedirect('/teacher/teacher_academic_activity_aduit')


def no_pass_activity(request):
    act_id = request.GET.get('act_id')
    a_act = Academicactivity.objects.get(aca_activity_id=act_id)
    a_act.aca_audit_situation = '未通过'
    a_act.save()
    return HttpResponseRedirect('/teacher/teacher_academic_activity_aduit')


def head_pass_activity(request):
    act_id = request.GET.get('act_id')
    a_act = Academicactivity.objects.get(aca_activity_id=act_id)
    if a_act.aca_audit_situation in ['审核中', '未通过', '负责人审核通过']:
        a_act.aca_audit_situation = '负责人审核通过'
        a_act.save()
    else:
        a_act.aca_audit_situation = '通过'
        a_act.save()
    return HttpResponseRedirect('/teacher/head_teacher_academic_activity_aduit')


def head_no_pass_activity(request):
    act_id = request.GET.get('act_id')
    a_act = Academicactivity.objects.get(aca_activity_id=act_id)
    a_act.aca_audit_situation = '未通过'
    a_act.save()
    return HttpResponseRedirect('/teacher/head_teacher_academic_activity_aduit')


def teacher_ache_commit(request):
    return render(request, "teacher/teacher_ache_commit", {})


def student_index(request):
    return render(request, 'student/student_index.html', {})


def student_assistant_volunteer_apply(request):
    return render(request, 'student/student_assistant_volunteer_apply.html', {'assistantVolunteer': 1})


def student_assistant_volunteer_work(request):
    return render(request, 'student/student_assistant_volunteer_work.html', {})


def student_assistant_volunteer_export(request):
    return render(request, 'student/student_assistant_volunteer_export.html', {})


def student_myProject(request):
    stu_id = request.session.get('log_id')
    ip_list = Identifyproject.objects.filter(ip_stu_id=stu_id)  # 根据学号展示
    return render(request, 'student/student_myProject.html', {'ip_list': ip_list})


def student_search_project(request):
    return render(request, 'student/student_search_project.html', {})


@csrf_exempt
def student_identify_project(request):
    try:
        pro_id = request.GET.get('pro_id')
        stu_id = request.session.get('log_id')
        project = Project.objects.get(pro_id=pro_id)
        ip_list = Identifyproject.objects.filter(ip_pro_id=pro_id)
        for ip in ip_list:
            if (ip.ip_stu_id == stu_id):  # 判断是否重复认定
                issame = True
                return render(request, 'student/student_search_project.html', {'issame': issame})
        return render(request, 'student/student_identify_project.html', {'project': project})
    except:
        isexist = False
        return render(request, 'student/student_search_project.html', {'isexist': isexist})


def download_evidence(request):
    filename = request.GET.get('filename')
    file = open(filename, 'rb')
    response = FileResponse(file)
    _, n = os.path.split(filename)
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="{}"'.format(n)
    return response


def post_identify_project_form(request):
    myFile = request.FILES.get("evidence", None)  # 获取上传的文件，如果没有文件，则默认为None
    if not myFile:
        return HttpResponse("no files for upload!")
    destination = open(os.path.join('files', 's002' + '_' + myFile.name), 'wb+')  # 打开特定的文件进行二进制的写操作
    for chunk in myFile.chunks():  # 分块写入文件
        destination.write(chunk)
    destination.close()
    ip = Identifyproject(
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
    student_id = request.session.get('log_id')
    lists = Academicactivity.objects.all().filter(aca_student_id=student_id)
    return render(request, 'student/student_academic_activity.html', {'activity_list': lists, 'have_list': True})


def student_activity_form(request):
    return render(request, 'student/student_academic_activity.html', {'have_list': False})


def post_academic_activity_form(request):
    myFile = request.FILES.get("evidence", None)  # 获取上传的文件，如果没有文件，则默认为None

    if not myFile:
        return HttpResponse("no files for upload!")
    id = request.session.get('log_id')
    if not os.path.exists('files/' + id):
        os.makedirs('files/' + id)
    destination = open(os.path.join("files", id, myFile.name), 'wb+')  # 打开特定的文件进行二进制的写操作
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
        aca_evidentiary_material=os.path.join("files", id, myFile.name),
        aca_audit_situation='审核中'
    )
    a_activity.save()

    return render(request, 'student/student_index.html', {'main_content': '提交成功'})


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


def ache_test1(request):
    return render(request, 'student/ache_test1.html', {})


# manager
def manager_index(request):
    return render(request, 'manager/manager_index.html', {})


def manager_own(request):
    return render(request, 'manager/manager_own.html', {})


@csrf_exempt
def manager_users_add(request):
    if request.method == 'POST':
        id = request.POST.get('u_id')
        pwd = request.POST.get('u_pwd')
        type = request.POST.get('type')
        if Users.objects.all().filter(log_id=id).exists():
            return HttpResponse("""
            <script>
            alert('不能添加id相同的数据');
            window.location='/manager/manager_users_add';
            </script>
            """
                                )
        else:
            Users.objects.create(log_id=id, log_pwd=pwd, log_type=type)
    return render(request, 'manager/manager_users_add.html', {})


@csrf_exempt
def manager_users_delete(request):
    if request.method == 'POST':
        id = request.POST.get('u_id')
        type = request.POST.get('type')
        Users.objects.all().filter(log_id=id, log_type=type).delete()
    return render(request, 'manager/manager_users_delete.html', {})


@csrf_exempt
def manager_users_alter(request):
    if request.method == 'POST':
        id = request.POST.get('u_id')
        new_id = request.POST.get('u_new_id')
        new_pwd = request.POST.get('u_new_pwd')
        new_type = request.POST.get('type')
        if id == new_id and id != None:
            return HttpResponse("""
            <script>
            alert('旧用户名不能与新用户名一致');
            window.location='/manager/manager_users_alter';
            </script>
            """
                                )
        else:
            Users.objects.all().filter(log_id=id).update(log_id=new_id, log_pwd=new_pwd, log_type=new_type)
    return render(request, 'manager/manager_users_alter.html', {})


@csrf_exempt
def manager_users_search(request):
    lists = []
    if request.method == 'POST':
        id = request.POST.get('u_id')
        lists = Users.objects.all().filter(log_id=id)
    return render(request, 'manager/manager_users_search.html', {'lists': lists})


@csrf_exempt
def manager_courses_add(request):
    if request.method == 'POST':
        id = request.POST.get('c_id')
        name = request.POST.get('c_name')
        hours = request.POST.get('c_hours')
        scores = request.POST.get('c_scores')
        numbers = request.POST.get('c_numbers')
        academy = request.POST.get('c_academy')
        subject = request.POST.get('c_subject')
        teacher_id = request.POST.get('c_teacher_id')
        teacher_name = request.POST.get('c_teacher_name')
        teacher_sex = request.POST.get('c_teacher_sex')
        teacher_subject = request.POST.get('c_teacher_subject')
        schedule = request.POST.get('c_schedule')
        assessment = request.POST.get('c_assessment_method')
        nature = request.POST.get('c_nature')
        if Courses.objects.all().filter(course_id=id).exists():
            return HttpResponse("""
            <script>
            alert('不能添加id相同的数据');
            window.location='/manager/manager_courses_add';
            </script>
            """
                                )
        else:
            list_task = Teacher.objects.all().filter(teacher_id=teacher_id)
            if list_task.exists():
                if list_task[0].teacher_status == 2:
                    Teacher.objects.all().filter(teacher_id=teacher_id).update(teacher_id=list_task[0].teacher_id,
                                                                               teacher_name=list_task[0].teacher_name,
                                                                               teacher_sex=list_task[0].teacher_sex,
                                                                               teacher_subject=list_task[0].teacher_subject,
                                                                               teacher_status=4)
                elif list_task[0].teacher_status == 3:
                    Teacher.objects.all().filter(teacher_id=teacher_id).update(teacher_id=list_task[0].teacher_id,
                                                                               teacher_name=list_task[0].teacher_name,
                                                                               teacher_sex=list_task[0].teacher_sex,
                                                                               teacher_subject=list_task[0].teacher_subject,
                                                                               teacher_status=5)
                elif list_task[0].teacher_status == 6:
                    Teacher.objects.all().filter(teacher_id=teacher_id).update(teacher_id=list_task[0].teacher_id,
                                                                               teacher_name=list_task[0].teacher_name,
                                                                               teacher_sex=list_task[0].teacher_sex,
                                                                               teacher_subject=list_task[0].teacher_subject,
                                                                               teacher_status=7)
                Courses.objects.create(course_id=id,course_name=name,course_hours=hours,course_scores=scores,
                                       course_number=numbers,course_academy=academy,course_subject=subject,
                                       course_teacher=Teacher.objects.all().get(teacher_id=teacher_id),
                                       course_schedule=schedule,
                                       course_assessment_method=assessment,course_nature=nature)
            else:
                Courses.objects.create(course_id=id, course_name=name, course_hours=hours, course_scores=scores,
                                       course_number=numbers, course_academy=academy, course_subject=subject,
                                       course_teacher=Teacher.objects.create(teacher_id=teacher_id,
                                                                             teacher_name=teacher_name,
                                                                             teacher_sex=teacher_sex,
                                                                             teacher_subject=teacher_subject,
                                                                             teacher_status=1),
                                       course_schedule=schedule,
                                       course_assessment_method=assessment, course_nature=nature)
    return render(request, 'manager/manager_courses_add.html', {})


@csrf_exempt
def manager_courses_delete(request):
    if request.method == 'POST':
        id = request.POST.get('c_id')
        Courses.objects.all().filter(course_id=id).delete()
    return render(request, 'manager/manager_courses_delete.html', {})


@csrf_exempt
def manager_courses_alter(request):
    if request.method == 'POST':
        id = request.POST.get('c_id')
        new_id = request.POST.get('c_new_id')
        name = request.POST.get('c_name')
        hours = request.POST.get('c_hours')
        scores = request.POST.get('c_scores')
        numbers = request.POST.get('c_numbers')
        academy = request.POST.get('c_academy')
        subject = request.POST.get('c_subject')
        teacher_id = request.POST.get('c_teacher_id')
        schedule = request.POST.get('c_schedule')
        assessment = request.POST.get('c_assessment_method')
        nature = request.POST.get('c_nature')
        if id == new_id and id != None:
            return HttpResponse("""
            <script>
            alert('旧课程号不能与新课程号一致');
            window.location='/manager/manager_courses_alter';
            </script>
            """
                                )
        else:
            list_task = Teacher.objects.all().filter(teacher_id=teacher_id)
            if list_task.exists():
                if list_task[0].teacher_status == 2:
                    Teacher.objects.all().filter(teacher_id=teacher_id).update(teacher_id=list_task[0].teacher_id,
                                                                               teacher_name=list_task[0].teacher_name,
                                                                               teacher_sex=list_task[0].teacher_sex,
                                                                               teacher_subject=list_task[0].teacher_subject,
                                                                               teacher_status=4)
                elif list_task[0].teacher_status == 3:
                    Teacher.objects.all().filter(teacher_id=teacher_id).update(teacher_id=list_task[0].teacher_id,
                                                                               teacher_name=list_task[0].teacher_name,
                                                                               teacher_sex=list_task[0].teacher_sex,
                                                                               teacher_subject=list_task[0].teacher_subject,
                                                                               teacher_status=5)
                elif list_task[0].teacher_status == 6:
                    Teacher.objects.all().filter(teacher_id=teacher_id).update(teacher_id=list_task[0].teacher_id,
                                                                               teacher_name=list_task[0].teacher_name,
                                                                               teacher_sex=list_task[0].teacher_sex,
                                                                               teacher_subject=list_task[0].teacher_subject,
                                                                               teacher_status=7)
            else:
                return HttpResponse("""
                            <script>
                            alert('不存在该序号教师');
                            window.location='/manager/manager_courses_alter';
                            </script>
                            """
                                    )
            Courses.objects.all().filter(course_id=id).update(course_id=new_id,course_name=name,course_hours=hours,
                                                              course_scores=scores,course_number=numbers,
                                                              course_academy=academy,course_subject=subject,
                                                              course_teacher=teacher_id,course_schedule=schedule,
                                                              course_assessment_method=assessment,course_nature=nature)
    return render(request, 'manager/manager_courses_alter.html', {})


@csrf_exempt
def manager_courses_search(request):
    lists = []
    if request.method == 'POST':
        id = request.POST.get('c_id')
        lists = Courses.objects.all().filter(course_id=id)
    return render(request, 'manager/manager_courses_search.html', {'lists' : lists})

@csrf_exempt
def manager_projects_add(request):
    if request.method == 'POST':
        id = request.POST.get('p_id')
        name = request.POST.get('p_name')
        type = request.POST.get('p_type')
        tutor = request.POST.get('p_tutor')
        if Project.objects.all().filter(pro_id=id).exists():
            return HttpResponse("""
            <script>
            alert('不能添加id相同的数据');
            window.location='/manager/manager_projects_add';
            </script>
            """
                                )
        else:
            list_task = Teacher.objects.all().filter(teacher_id=tutor)
            if list_task.exists():
                if list_task[0].teacher_status == 1:
                    Teacher.objects.all().filter(teacher_id=tutor).update(teacher_id=list_task[0].teacher_id,
                                                                               teacher_name=list_task[0].teacher_name,
                                                                               teacher_sex=list_task[0].teacher_sex,
                                                                               teacher_subject=list_task[0].teacher_subject,
                                                                               teacher_status=4)
                elif list_task[0].teacher_status == 3:
                    Teacher.objects.all().filter(teacher_id=tutor).update(teacher_id=list_task[0].teacher_id,
                                                                               teacher_name=list_task[0].teacher_name,
                                                                               teacher_sex=list_task[0].teacher_sex,
                                                                               teacher_subject=list_task[0].teacher_subject,
                                                                               teacher_status=6)
                elif list_task[0].teacher_status == 5:
                    Teacher.objects.all().filter(teacher_id=tutor).update(teacher_id=list_task[0].teacher_id,
                                                                               teacher_name=list_task[0].teacher_name,
                                                                               teacher_sex=list_task[0].teacher_sex,
                                                                               teacher_subject=list_task[0].teacher_subject,
                                                                               teacher_status=7)
                Project.objects.create(pro_id=id,pro_name=name,pro_type=type,
                                       pro_tutor=Teacher.objects.all().get(teacher_id=tutor))
            else:
                Project.objects.create(pro_id=id,pro_name=name,pro_type=type,
                                       pro_tutor=Teacher.objects.all().get(teacher_id=tutor))
    return render(request, 'manager/manager_projects_add.html', {})

@csrf_exempt
def manager_projects_delete(request):
    if request.method == 'POST':
        id = request.POST.get('p_id')
        Project.objects.all().filter(pro_id=id).delete()
    return render(request, 'manager/manager_projects_delete.html', {})

@csrf_exempt
def manager_projects_alter(request):
    if request.method == 'POST':
        id = request.POST.get('p_id')
        new_id = request.POST.get('p_new_id')
        name = request.POST.get('p_name')
        type = request.POST.get('p_type')
        tutor = request.POST.get('p_tutor')
        if id == new_id and id != None:
            return HttpResponse("""
            <script>
            alert('旧项目号不能与新项目号一致');
            window.location='/manager/manager_projects_alter';
            </script>
            """
                                )
        else:
            list_task = Teacher.objects.all().filter(teacher_id=tutor)
            if list_task.exists():
                if list_task[0].teacher_status == 1:
                    Teacher.objects.all().filter(teacher_id=tutor).update(teacher_id=list_task[0].teacher_id,
                                                                          teacher_name=list_task[0].teacher_name,
                                                                          teacher_sex=list_task[0].teacher_sex,
                                                                          teacher_subject=list_task[0].teacher_subject,
                                                                          teacher_status=4)
                elif list_task[0].teacher_status == 3:
                    Teacher.objects.all().filter(teacher_id=tutor).update(teacher_id=list_task[0].teacher_id,
                                                                          teacher_name=list_task[0].teacher_name,
                                                                          teacher_sex=list_task[0].teacher_sex,
                                                                          teacher_subject=list_task[0].teacher_subject,
                                                                          teacher_status=6)
                elif list_task[0].teacher_status == 5:
                    Teacher.objects.all().filter(teacher_id=tutor).update(teacher_id=list_task[0].teacher_id,
                                                                          teacher_name=list_task[0].teacher_name,
                                                                          teacher_sex=list_task[0].teacher_sex,
                                                                          teacher_subject=list_task[0].teacher_subject,
                                                                          teacher_status=7)
            else:
                return HttpResponse("""
                            <script>
                            alert('不存在该序号教师');
                            window.location='/manager/manager_projects_alter';
                            </script>
                            """
                                    )
            Project.objects.all().filter(pro_id=id).update(pro_id=id,pro_name=name,pro_type=type,
                                                              pro_tutor=Teacher.objects.all().get(teacher_id=tutor))
    return render(request, 'manager/manager_projects_alter.html', {})

@csrf_exempt
def manager_projects_search(request):
    lists = []
    if request.method == 'POST':
        id = request.POST.get('p_id')
        lists = Project.objects.all().filter(pro_id=id)
    return render(request, 'manager/manager_projects_search.html', {'lists': lists})


def manager_project_identify(request):
    ip_list = Identifyproject.objects.filter(ip_status=0,
                                             ip_mid_status=1)
    return render(request, 'manager/manager_project_identify.html', {'ip_list': ip_list})


def pass_project(request):  # 通过项目
    pro_id = request.GET.get('pro_id')
    stu_id = request.GET.get('stu_id')
    ip = Identifyproject.objects.get(ip_pro_id=pro_id, ip_stu_id=stu_id)
    ip.ip_status = 1  # 设置为通过
    ip.save()
    return HttpResponseRedirect('/manager/manager_project_identify')


def no_pass_project(request):
    pro_id = request.GET.get('pro_id')
    stu_id = request.GET.get('stu_id')
    ip = Identifyproject.objects.get(ip_pro_id=pro_id, ip_stu_id=stu_id)
    ip.ip_status = -1  # 设置为不通过
    ip.save()
    return HttpResponseRedirect('/manager/manager_project_identify')

@csrf_exempt
def manager_academic_activity_add(request):
    return render(request, 'manager/manager_academic_activity_add.html', {})

@csrf_exempt
def manager_academic_activity_delete(request):
    return render(request, 'manager/manager_academic_activity_delete.html', {})

@csrf_exempt
def manager_academic_activity_alter(request):
    return render(request, 'manager/manager_academic_activity_alter.html', {})

@csrf_exempt
def manager_academic_activity_search(request):
    return render(request, 'manager/manager_academic_activity_search.html', {})

@csrf_exempt
def manager_student_basic_information(request):
    return render(request, 'manager/manager_student_basic_information.html', {})
