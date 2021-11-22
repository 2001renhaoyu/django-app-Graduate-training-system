import datetime
import random

from django.forms import model_to_dict
from django.http import HttpResponse, FileResponse
from django.shortcuts import render
from django.utils.encoding import escape_uri_path
from django.views.decorators.csrf import csrf_exempt
from reportlab.pdfgen import canvas

from polls.models import *
from django.http import HttpResponseRedirect
import os


# Create your views here.


def login(request):
    u = Users({
        'log_id': '132',
        'log_pwd': '213',
        'log_type': '12231',
    })
    print(u)

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
    id=request.session.get('log_id')
    teacher=Teacher.objects.get(teacher_id=id)
    return render(request, "teacher/teacher_index.html",{'teacher':teacher})


def teacher_homepage(request):
    id = request.session.get('log_id')
    teacher = Teacher.objects.get(teacher_id=id)  # 根据学号展示
    return render(request, "teacher/teacher_homepage.html",{'teacher':teacher})


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
    teacher_id = request.session.get('log_id')
    try:
        ip = Identifyproject.objects.get(ip_pro_id=pro_id,
                                         ip_stu_id=stu_id)
        ip.ip_funds = pro_funds
        ip.ip_mid_status = 1
        teacher = Teacher.objects.get(teacher_id=teacher_id)
        t_funds = float(teacher.teacher_funds)
        t = t_funds - pro_funds
        if (t >= 0):
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
    cur_teacher_id = request.session.get('log_id')
    cur_teacher = Teacher.objects.get(teacher_id=cur_teacher_id)
    cur_teacher_status = cur_teacher.teacher_status
    if cur_teacher_status == "4" or cur_teacher_status == "1" or cur_teacher_status == "2":
        return render(request, 'student/student_index.html', {'inf': "你没有学科负责人的权限"})
    else:
        try:
            cur_config = Volunteerapplicationconfig.objects.get(teacher_id=cur_teacher_id)
        except Volunteerapplicationconfig.DoesNotExist:
            cur_config = Volunteerapplicationconfig()
            cur_config.teacher_id = cur_teacher_id
            cur_config.subject = cur_teacher.teacher_subject
            cur_config.maxnum_volunteer = 2
            cur_config.time_start = "2000-01-01"
            cur_config.time_end = "2000-01-01"
            cur_config.state = "0"
            cur_config.save()
        finally:
            return render(request, "teacher/teacher_assistant_volunteer_apply.html", {"cur_config": cur_config})


def teacher_assistant_volunteer_select(request):
    cur_teacher_id = request.session.get('log_id')
    cur_teacher = Teacher.objects.get(teacher_id=cur_teacher_id)
    cur_teacher_status = cur_teacher.teacher_status
    if cur_teacher_status == "2" or cur_teacher_status == "3" or cur_teacher_status == "6":
        return render(request, 'teacher/teacher_index.html', {'inf': "你没有教授课程"})
    else:
        cur_config = Volunteerapplicationconfig.objects.get(subject=cur_teacher.teacher_subject)
        cur_courses = Courses.objects.filter(course_teacher=cur_teacher_id)
        cur_volsInf = []
        for course in cur_courses:
            if Assistantjob.objects.filter(ass_course_id=course.course_id):
                pass
            elif Teacherselect.objects.filter(course_id=course.course_id):
                pass
            else:
                cur_vols = Volunteerapplication.objects.filter(course_id=course.course_id)
                for cur_vol in cur_vols:
                    cur_volsInf.append([cur_vol.stu_id, cur_vol.stu.stu_name, cur_vol.course_id,
                                        cur_vol.course.course_name, cur_vol.priority])

        return render(request, 'teacher/teacher_assistant_volunteer_select.html'
                      , {"cur_config": cur_config, "cur_volsInf": cur_volsInf})
    pass

def teacher_assistant_volunteer_evaluate(request):
    cur_teacher_id = request.session.get('log_id')
    cur_teacher = Teacher.objects.get(teacher_id=cur_teacher_id)
    cur_courses = Courses.objects.filter(course_teacher=cur_teacher_id)
    cur_inf = []
    for course in cur_courses:
        cur_job = Assistantjob.objects.filter(ass_course_id=course.course_id)
        if cur_assistantjob is not None:
            pass



@csrf_exempt
def post_teacher_assistant_volunteer_evaluate(request):
    pass

@csrf_exempt
def post_teacher_assistant_volunteer_select(request):
    cur_teacher_id = request.session.get('log_id')
    cur_courses = Courses.objects.filter(course_teacher=cur_teacher_id)
    for cur_course in cur_courses:
        stu_id = request.POST.get(cur_course.course_id)
        teacherselect = Teacherselect()
        teacherselect.stu_id = stu_id
        teacherselect.course_id = cur_course.course_id
        teacherselect.save()
        pass
    return render(request, 'teacher/teacher_index.html', {'inf': "选取完毕"})


@csrf_exempt
def post_teacher_assistant_volunteer_apply(request):
    cur_teacher_id = request.session.get('log_id')
    cur_config = Volunteerapplicationconfig.objects.get(teacher_id=cur_teacher_id)
    if cur_config.state == "0" or cur_config.state == "1":
        date = request.POST.get('date-range-picker')
        t1 = date.split(' ')
        t2 = t1[0].split('/')
        t3 = t1[2].split('/')
        date_start = request.POST.get('date_start')
        date_end = request.POST.get('date_end')
        time_start = t2[2] + "-" + t2[0] + "-" + t2[1] + " " + date_start
        time_end = t3[2] + "-" + t3[0] + "-" + t3[1] + " " + date_end
        cur_config.time_start = time_start
        cur_config.time_end = time_end

    if cur_config.state == "0":
        maxNum_volunteer = request.POST.get('maxNum_volunteer')
        sort_method = request.POST.get('form-field-radio')
        cur_config.state = "1"
        cur_config.maxnum_volunteer = maxNum_volunteer
        cur_config.sort_method = sort_method

    elif cur_config.state == "1":
        cur_config.state = "2"

    elif cur_config.state == "2":
        # 即将进行新的一轮申请，此时需要
        # 根据老师选择表，学生志愿表确定一部分助教（插入assistantJob）
        cur_config.state = "0"
        ts_set=Teacherselect.objects.all()
        va_set=Volunteerapplication.objects.all().order_by("priority")
        selected_list=[]
        for va in va_set.all():
            if ts_set.filter(stu_id=va.stu_id,course_id=va.course_id).count()>0 and \
                    (va.stu_id+'-=-'+va.course_id) not in selected_list:
                Assistantjob.objects.create(
                    ass_stu_id=va.stu_id,
                    ass_course_id=va.course_id
                )
                selected_list.append((va.stu_id+'-=-'+va.course_id))
    cur_config.save()
    return render(request, "teacher/teacher_assistant_volunteer_apply.html", {"cur_config": cur_config})


@csrf_exempt
def end_teacher_assistant_volunteer_apply(request):
    cur_teacher_id = request.session.get('log_id')
    cur_config = Volunteerapplicationconfig.objects.get(teacher_id=cur_teacher_id)
    cur_config.state = "0"
    # 结束申请，此时需要
    # 根据老师选择表，学生志愿表确助教（插入assistantJob），统筹确定暂时不实现
    ts_set = Teacherselect.objects.all()
    va_set = Volunteerapplication.objects.all().order_by("priority")
    selected_list = []
    for va in va_set.all():
        if ts_set.filter(stu_id=va.stu_id, course_id=va.course_id).count() > 0 and \
                (va.stu_id + '-=-' + va.course_id) not in selected_list:
            Assistantjob.objects.create(
                ass_stu_id=va.stu_id,
                ass_course_id=va.course_id
            )
            selected_list.append((va.stu_id + '-=-' + va.course_id))
    cur_config.save()
    return render(request, "teacher/teacher_assistant_volunteer_apply.html", {"cur_config": cur_config})


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
    if a_act.aca_audit_situation in ['审核中', '未通过', '导师审核通过']:
        a_act.aca_audit_situation = '导师审核通过'
        a_act.save()
    else:
        a_act.aca_audit_situation = '通过'
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
    cur_student_id = request.session.get('log_id')
    cur_student = Student.objects.get(stu_id=cur_student_id)
    if Assistantjob.objects.filter(ass_stu_id= cur_student_id).count()>0:
        return render(request, 'student/student_index.html', {'inf': "你已经被录用"})

    if Volunteerapplication.objects.filter(stu_id= cur_student_id).count()>0:
        return render(request, 'student/student_index.html', {'inf': "申报完毕"})

    cur_subject = cur_student.stu_subject
    cur_config = Volunteerapplicationconfig.objects.get(subject=cur_subject)

    courses = Courses.objects.filter(course_subject=cur_subject)
    have_ass = []
    for a_course in courses:
        if Assistantjob.objects.filter(ass_course_id=a_course.course_id).count() > 0:
            have_ass.append(False)
        else:
            have_ass.append(True)
    pass

    if cur_config.state == "1":
        if cur_config.sort_method == "默认排序":
            pass
        elif cur_config.sort_method == "按照选课人数":
            courses = Courses.objects.filter(course_subject=cur_subject).order_by('-course_number')
            pass
        elif cur_config.sort_method == "按照学时":
            courses = Courses.objects.filter(course_subject=cur_subject).order_by('-course_hours')
            pass
        elif cur_config.sort_method == "按照选课人数、学时":
            courses = Courses.objects.filter(course_subject=cur_subject).order_by('-course_number', '-course_hours')
            pass
        dit_courses = []
        for index, i in enumerate(have_ass):
            dit_courses.append([courses[index], i])

        return render(request, 'student/student_assistant_volunteer_apply.html',
                      {'cur_config': cur_config, "dit_courses": dit_courses, "range": range(1, cur_config.maxnum_volunteer+1)})

    else:
        return render(request, 'student/student_assistant_volunteer_apply.html', {'cur_config': cur_config})


@csrf_exempt
def post_student_assistant_volunteer_apply(request):
    cur_student_id = request.session.get('log_id')
    cur_student = Student.objects.get(stu_id=cur_student_id)
    cur_subject = cur_student.stu_subject
    cur_config = Volunteerapplicationconfig.objects.get(subject=cur_subject)

    vols = []
    for i in range(1, cur_config.maxnum_volunteer + 1):
        vols.append(request.POST.get("select-vol" + str(i)))
    set_vols = set(vols)

    if len(vols) == len(set_vols):
        for i in range(0, cur_config.maxnum_volunteer):
            priority = str(i+1)
            vol = Volunteerapplication()
            vol.priority = priority
            vol.stu_id = cur_student_id
            vol.course_id = vols[i]
            vol.save()

        return render(request, 'student/student_index.html', {'inf': "申报完毕"})
    else:
        return HttpResponse("志愿有课程重复，请返回")



def student_assistant_volunteer_work(request):
    return render(request, 'student/student_assistant_volunteer_work.html', {})


def student_assistant_volunteer_export(request):
    return render(request, 'student/student_assistant_volunteer_export.html', {})


def student_myProject(request):
    stu_id = request.session.get('log_id')
    ip_list = Identifyproject.objects.filter(ip_stu_id=stu_id)  # 根据学号展示
    return render(request, 'student/student_myProject.html', {'ip_list': ip_list})


def student_myAchievements(request):
    stu_id = request.session.get('log_id')
    stu = Student.objects.get(stu_id=stu_id)
    print(stu.stu_name)
    thesis_list = ThesisV.objects.filter(学生名=stu.stu_name)
    reward_list = RewardV.objects.filter(学生名=stu.stu_name)
    standard_list = StandardV.objects.filter(学生名=stu.stu_name)
    book_list = BookV.objects.filter(学生名=stu.stu_name)
    patent_list = PatentV.objects.filter(学生名=stu.stu_name)
    report_list = ReportV.objects.filter(学生名=stu.stu_name)
    softwarehardware_list = SoftwarehardwareV.objects.filter(学生名=stu.stu_name)
    ache_lists = [
        thesis_list,
        reward_list,
        standard_list,
        book_list,
        patent_list,
        report_list,
        softwarehardware_list,
    ]
    ache_lists = [[model_to_dict(j) for j in i] for i in ache_lists]
    for i in ache_lists:
        for j in i:
            j.pop('导师id')
            j.pop('学生名')
        if i == []:
            i = None
    return render(request, 'student/student_myAchievements.html', {'ache_lists': ache_lists})


def student_homepage(request):
    stu_id = request.session.get('log_id')
    stu = Student.objects.get(stu_id=stu_id)  # 根据学号展示
    return render(request, 'student/student_homepage.html', {'stu': stu})


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

    ache_lists = [
        thesis_list,
        reward_list,
        standard_list,
        book_list,
        patent_list,
        report_list,
        softwarehardware_list,
    ]
    ache_lists = [[model_to_dict(j) for j in i] for i in ache_lists]
    return render(request, 'teacher/teacher_achievement_audit.html', {'ache_lists': ache_lists})


def download_evidence(request):
    filename = request.GET.get('filename')
    file = open(filename, 'rb')
    response = FileResponse(file)
    _, n = os.path.split(filename)
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="{}"'.format(escape_uri_path(n))
    return response


def post_identify_project_form(request):
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
    stu_id = request.session.get('log_id')
    ip = Identifyproject(
        ip_stu_id=stu_id,
        ip_pro_id=request.POST.get('pro_id'),
        ip_job_content=request.POST.get('job_content'),
        ip_begintime=request.POST.get('begin_time'),
        ip_endtime=request.POST.get('end_time'),
        ip_path=os.path.join("files", id, myFile.name),
        ip_funds=0,
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


def post_reward_form(request):
    myFile = request.FILES.get("ache_evidence", None)  # 获取上传的文件，如果没有文件，则默认为None

    if not myFile:
        return HttpResponse("no files for upload!")
    id = request.session.get('log_id')
    if not os.path.exists('files/' + id):
        os.makedirs('files/' + id)
    destination = open(os.path.join("files", id, myFile.name), 'wb+')  # 打开特定的文件进行二进制的写操作
    for chunk in myFile.chunks():  # 分块写入文件
        destination.write(chunk)
    destination.close()

    a_dict = request.POST.dict()
    a_dict.pop('csrfmiddlewaretoken')
    a_dict.pop('ache_type')
    a_dict['ache_id'] = 'a' + str(random.randint(1, 1000))
    Acheievementindex(
        ache_id=a_dict['ache_id'],
        ache_stu_id=request.session.get('log_id'),
        ache_type=request.POST.get('ache_type'),
        ache_audit_situation='审核中',
        ache_evidence=os.path.join("files", id, myFile.name),
    ).save()
    ache_type = request.POST.get('ache_type')
    if ache_type == '论文':
        Thesis(**a_dict).save()
    elif ache_type == '奖励':
        a_dict['re_num'] = int(a_dict['re_num'])
        Reward(**a_dict).save()
    elif ache_type == '标准':
        Standard(**a_dict).save()
    elif ache_type == '其他':
        return HttpResponse('error')
    elif ache_type == '教材':
        Book(**a_dict).save()
    elif ache_type == '专利':
        Patent(**a_dict).save()
    elif ache_type == '报告':
        Report(**a_dict).save()
    elif ache_type == '软硬件平台':
        Softwarehardware(**a_dict).save()
    else:
        return HttpResponse('error')
    return HttpResponseRedirect('/student')


def teacher_achievement_aduit(request):
    id = request.session.get('log_id')
    thesis_list = ThesisV.objects.filter(导师id=id)
    reward_list = RewardV.objects.filter(导师id=id)
    standard_list = StandardV.objects.filter(导师id=id)
    book_list = BookV.objects.filter(导师id=id)
    patent_list = PatentV.objects.filter(导师id=id)
    report_list = ReportV.objects.filter(导师id=id)
    softwarehardware_list = SoftwarehardwareV.objects.filter(导师id=id)
    ache_lists = [
        thesis_list,
        reward_list,
        standard_list,
        book_list,
        patent_list,
        report_list,
        softwarehardware_list,
    ]
    ache_lists = [[model_to_dict(j) for j in i] for i in ache_lists]
    for i in ache_lists:
        for j in i:
            j.pop('导师id')
        if i == []:
            i = None
    return render(request, 'teacher/teacher_achievement_audit.html', {'ache_lists': ache_lists})


def manager_achievement_aduit(request):
    thesis_list = ThesisV.objects.all()
    reward_list = RewardV.objects.all()
    standard_list = StandardV.objects.all()
    book_list = BookV.objects.all()
    patent_list = PatentV.objects.all()
    report_list = ReportV.objects.all()
    softwarehardware_list = SoftwarehardwareV.objects.all()
    ache_lists = [
        thesis_list,
        reward_list,
        standard_list,
        book_list,
        patent_list,
        report_list,
        softwarehardware_list,
    ]
    ache_lists = [[model_to_dict(j) for j in i] for i in ache_lists]
    for i in ache_lists:
        for j in i:
            j.pop('导师id')
        if i == []:
            i = None
    return render(request, 'manager/manager_achievement_audit.html', {'ache_lists': ache_lists})


def pass_achievement(request):
    ache_id = request.GET.get('ache_id')
    a_ache = Acheievementindex.objects.get(ache_id=ache_id)
    if a_ache.ache_audit_situation in ['审核中', '未通过', '导师审核通过']:
        a_ache.ache_audit_situation = '导师审核通过'
        a_ache.save()
    else:
        a_ache.ache_audit_situation = '通过'
        a_ache.save()
    return HttpResponseRedirect('/teacher/teacher_achievement_aduit')


def no_pass_achievement(request):
    ache_id = request.GET.get('ache_id')
    a_ache = Acheievementindex.objects.get(ache_id=ache_id)
    a_ache.ache_audit_situation = '未通过'
    a_ache.save()
    return HttpResponseRedirect('/teacher/teacher_achievement_aduit')


def manager_pass_achievement(request):
    ache_id = request.GET.get('ache_id')
    a_ache = Acheievementindex.objects.get(ache_id=ache_id)
    if a_ache.ache_audit_situation in ['审核中', '未通过', '管理员审核通过']:
        a_ache.ache_audit_situation = '管理员审核通过'
        a_ache.save()
    else:
        a_ache.ache_audit_situation = '通过'
        a_ache.save()
    return HttpResponseRedirect('/manager/manager_achievement_aduit')


def manager_no_pass_achievement(request):
    ache_id = request.GET.get('ache_id')
    a_ache = Acheievementindex.objects.get(ache_id=ache_id)
    a_ache.ache_audit_situation = '未通过'
    a_ache.save()
    return HttpResponseRedirect('/manager/manager_achievement_aduit')


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
                                                                               teacher_subject=list_task[
                                                                                   0].teacher_subject,
                                                                               teacher_status=4)
                elif list_task[0].teacher_status == 3:
                    Teacher.objects.all().filter(teacher_id=teacher_id).update(teacher_id=list_task[0].teacher_id,
                                                                               teacher_name=list_task[0].teacher_name,
                                                                               teacher_sex=list_task[0].teacher_sex,
                                                                               teacher_subject=list_task[
                                                                                   0].teacher_subject,
                                                                               teacher_status=5)
                elif list_task[0].teacher_status == 6:
                    Teacher.objects.all().filter(teacher_id=teacher_id).update(teacher_id=list_task[0].teacher_id,
                                                                               teacher_name=list_task[0].teacher_name,
                                                                               teacher_sex=list_task[0].teacher_sex,
                                                                               teacher_subject=list_task[
                                                                                   0].teacher_subject,
                                                                               teacher_status=7)
                Courses.objects.create(course_id=id, course_name=name, course_hours=hours, course_scores=scores,
                                       course_number=numbers, course_academy=academy, course_subject=subject,
                                       course_teacher=Teacher.objects.all().get(teacher_id=teacher_id),
                                       course_schedule=schedule,
                                       course_assessment_method=assessment, course_nature=nature)
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
                                                                               teacher_subject=list_task[
                                                                                   0].teacher_subject,
                                                                               teacher_status=4)
                elif list_task[0].teacher_status == 3:
                    Teacher.objects.all().filter(teacher_id=teacher_id).update(teacher_id=list_task[0].teacher_id,
                                                                               teacher_name=list_task[0].teacher_name,
                                                                               teacher_sex=list_task[0].teacher_sex,
                                                                               teacher_subject=list_task[
                                                                                   0].teacher_subject,
                                                                               teacher_status=5)
                elif list_task[0].teacher_status == 6:
                    Teacher.objects.all().filter(teacher_id=teacher_id).update(teacher_id=list_task[0].teacher_id,
                                                                               teacher_name=list_task[0].teacher_name,
                                                                               teacher_sex=list_task[0].teacher_sex,
                                                                               teacher_subject=list_task[
                                                                                   0].teacher_subject,
                                                                               teacher_status=7)
            else:
                return HttpResponse("""
                            <script>
                            alert('不存在该序号教师');
                            window.location='/manager/manager_courses_alter';
                            </script>
                            """
                                    )
            Courses.objects.all().filter(course_id=id).update(course_id=new_id, course_name=name, course_hours=hours,
                                                              course_scores=scores, course_number=numbers,
                                                              course_academy=academy, course_subject=subject,
                                                              course_teacher=teacher_id, course_schedule=schedule,
                                                              course_assessment_method=assessment, course_nature=nature)
    return render(request, 'manager/manager_courses_alter.html', {})


@csrf_exempt
def manager_courses_search(request):
    lists = []
    if request.method == 'POST':
        id = request.POST.get('c_id')
        lists = Courses.objects.all().filter(course_id=id)
    return render(request, 'manager/manager_courses_search.html', {'lists': lists})


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
            else:
                return HttpResponse("""
                                    <script>
                                    alert('不存在该序号教师');
                                    window.location='/manager/manager_projects_add';
                                    </script>
                                    """
                                    )
            Project.objects.create(pro_id=id, pro_name=name, pro_type=type,
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
            Project.objects.all().filter(pro_id=id).update(pro_id=id, pro_name=name, pro_type=type,
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
    if request.method == 'POST':
        id = request.POST.get('a_id')
        student_id = request.POST.get('a_student_id')
        name = request.POST.get('a_name')
        local = request.POST.get('a_local')
        date = request.POST.get('a_date')
        zh = request.POST.get('a_zh')
        en = request.POST.get('a_en')
        material = request.POST.get('a_material')
        situation = request.POST.get('a_situation')
        extra = request.POST.get('a_extra')
        if Academicactivity.objects.all().filter(aca_activity_id=id).exists():
            return HttpResponse("""
            <script>
            alert('不能添加id相同的数据');
            window.location='/manager/manager_academic_activity_add';
            </script>
            """
                                )
        else:
            list_task = Student.objects.all().filter(stu_id=student_id)
            if list_task.exists():
                Academicactivity.objects.create(aca_activity_id=id, aca_activity_name=name,
                                                aca_student=Student.objects.all().get(stu_id=student_id),
                                                aca_activity_location=local, aca_activity_date=date,
                                                aca_report_name_zh=zh, aca_report_name_en=en,
                                                aca_evidentiary_material=material, aca_audit_situation=situation,
                                                aca_extra=extra
                                                )
            else:
                return HttpResponse("""
                            <script>
                            alert('不能添加未知学生id');
                            window.location='/manager/manager_academic_activity_add';
                            </script>
                            """
                                    )
    return render(request, 'manager/manager_academic_activity_add.html', {})


@csrf_exempt
def manager_academic_activity_delete(request):
    if request.method == 'POST':
        id = request.POST.get('a_id')
        Academicactivity.objects.all().filter(aca_activity_id=id).delete()
    return render(request, 'manager/manager_academic_activity_delete.html', {})


@csrf_exempt
def manager_academic_activity_alter(request):
    if request.method == 'POST':
        id = request.POST.get('a_id')
        new_id = request.POST.get('a_new_id')
        student_id = request.POST.get('a_student_id')
        name = request.POST.get('a_name')
        local = request.POST.get('a_local')
        date = request.POST.get('a_date')
        zh = request.POST.get('a_zh')
        en = request.POST.get('a_en')
        material = request.POST.get('a_material')
        situation = request.POST.get('a_situation')
        extra = request.POST.get('a_extra')
        if Academicactivity.objects.all().filter(aca_activity_id=new_id).exists():
            return HttpResponse("""
            <script>
            alert('不能添加id相同的数据');
            window.location='/manager/manager_academic_activity_alter';
            </script>
            """
                                )
        else:
            list_task = Student.objects.all().filter(stu_id=student_id)
            if list_task.exists():
                Academicactivity.objects.filter(aca_activity_id=id).update(aca_activity_id=new_id,
                                                                           aca_activity_name=name,
                                                                           aca_student=Student.objects.all().get(
                                                                               stu_id=student_id),
                                                                           aca_activity_location=local,
                                                                           aca_activity_date=date,
                                                                           aca_report_name_zh=zh, aca_report_name_en=en,
                                                                           aca_evidentiary_material=material,
                                                                           aca_audit_situation=situation,
                                                                           aca_extra=extra
                                                                           )
            else:
                return HttpResponse("""
                            <script>
                            alert('不能添加未知学生id');
                            window.location='/manager/manager_academic_activity_alter';
                            </script>
                            """
                                    )
    return render(request, 'manager/manager_academic_activity_alter.html', {})


@csrf_exempt
def manager_academic_activity_search(request):
    lists = []
    if request.method == 'POST':
        id = request.POST.get('a_id')
        lists = Academicactivity.objects.all().filter(aca_activity_id=id)
    return render(request, 'manager/manager_academic_activity_search.html', {'lists': lists})


@csrf_exempt
def manager_student_basic_information(request):
    if request.method == 'POST':
        name = request.POST.get('s_b_name')
        id = request.POST.get('s_b_id')
        sex = request.POST.get('s_b_sex')
        subject = request.POST.get('s_b_subject')
        type = request.POST.get('s_b_type')
        tutor = request.POST.get('s_b_tutor_id')
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
                                alert('不能添加未知导师id');
                                window.location='/manager/manager_academic_activity_alter';
                                </script>
                                """
                                )
        if Student.objects.all().filter(stu_id=id).exists():
            Student.objects.all.filter(stu_id=id).update(stu_name=name, stu_id=id, stu_sex=sex,
                                                         stu_subject=subject, stu_type=type,
                                                         stu_tutor=Teacher.objects.all().get(teacher_id=tutor))
        else:
            Student.objects.create(stu_name=name, stu_id=id, stu_sex=sex,
                                   stu_subject=subject, stu_type=type,
                                   stu_tutor=Teacher.objects.all().get(teacher_id=tutor))
    return render(request, 'manager/manager_student_basic_information.html', {})


@csrf_exempt
def manager_student_basic_information_search(request):
    search_id = request.POST.get('s_b_search_id')
    lists = Student.objects.all().filter(stu_id=search_id)
    return render(request, 'manager/manager_student_basic_information_search.html', {'lists': lists})


@csrf_exempt
def manager_tutor_basic_information(request):
    if request.method == 'POST':
        id = request.POST.get('t_b_id')
        name = request.POST.get('t_b_name')
        sex = request.POST.get('t_b_sex')
        funds = request.POST.get('t_b_funds')
        subject = request.POST.get('t_b_subject')
        list_task = Teacher.objects.all().filter(teacher_id=id)
        if list_task.exists():
            if list_task[0].teacher_status == 1:
                Teacher.objects.all().filter(teacher_id=id).update(teacher_id=id,
                                                                   teacher_name=name,
                                                                   teacher_sex=sex,
                                                                   teacher_funds=funds,
                                                                   teacher_subject=subject,
                                                                   teacher_status=4)
            elif list_task[0].teacher_status == 3:
                Teacher.objects.all().filter(teacher_id=id).update(teacher_id=id,
                                                                   teacher_name=name,
                                                                   teacher_sex=sex,
                                                                   teacher_funds=funds,
                                                                   teacher_subject=subject,
                                                                   teacher_status=6)
            elif list_task[0].teacher_status == 5:
                Teacher.objects.all().filter(teacher_id=id).update(teacher_id=id,
                                                                   teacher_name=name,
                                                                   teacher_sex=sex,
                                                                   teacher_funds=funds,
                                                                   teacher_subject=subject,
                                                                   teacher_status=7)
        else:
            Teacher.objects.create(teacher_id=id,
                                   teacher_name=name,
                                   teacher_sex=sex,
                                   teacher_funds=funds,
                                   teacher_subject=subject,
                                   teacher_status=2)
    return render(request, 'manager/manager_tutor_basic_information.html', {})


@csrf_exempt
def manager_tutor_basic_information_search(request):
    search_id = request.POST.get('t_b_search_id')
    lists = Teacher.objects.all().filter(teacher_id=search_id)
    return render(request, 'manager/manager_tutor_basic_information_search.html', {'lists': lists})

@csrf_exempt
def manager_tutor_projects_information_search(request):
    search_id = request.POST.get('t_p_search_id')
    lists = Project.objects.all().filter(pro_tutor=search_id)
    return render(request, 'manager/manager_tutor_projects_information_search.html', {'lists' : lists})

@csrf_exempt
def manager_course_teacher_basic_information(request):
    if request.method == 'POST':
        id = request.POST.get('t_b_id')
        name = request.POST.get('t_b_name')
        sex = request.POST.get('t_b_sex')
        funds = request.POST.get('t_b_funds')
        subject = request.POST.get('t_b_subject')
        list_task = Teacher.objects.all().filter(teacher_id=id)
        if list_task.exists():
            if list_task[0].teacher_status == 2:
                Teacher.objects.all().filter(teacher_id=id).update(teacher_id=id,
                                                                   teacher_name=name,
                                                                   teacher_sex=sex,
                                                                   teacher_funds=funds,
                                                                   teacher_subject=subject,
                                                                   teacher_status=4)
            elif list_task[0].teacher_status == 3:
                Teacher.objects.all().filter(teacher_id=id).update(teacher_id=id,
                                                                   teacher_name=name,
                                                                   teacher_sex=sex,
                                                                   teacher_funds=funds,
                                                                   teacher_subject=subject,
                                                                   teacher_status=5)
            elif list_task[0].teacher_status == 6:
                Teacher.objects.all().filter(teacher_id=id).update(teacher_id=id,
                                                                   teacher_name=name,
                                                                   teacher_sex=sex,
                                                                   teacher_funds=funds,
                                                                   teacher_subject=subject,
                                                                   teacher_status=7)
        else:
            Teacher.objects.create(teacher_id=id,
                                   teacher_name=name,
                                   teacher_sex=sex,
                                   teacher_funds=funds,
                                   teacher_subject=subject,
                                   teacher_status=1)
    return render(request, 'manager/manager_course_teacher_basic_information.html', {})

@csrf_exempt
def manager_course_teacher_basic_information_search(request):
    lists = []
    list = []
    if request.method == 'POST':
        search_id = request.POST.get('t_b_search_id')
        lists = Teacher.objects.all().filter(teacher_id=search_id)
        list = Courses.objects.all().filter(course_teacher=search_id)
    return render(request, 'manager/manager_course_teacher_basic_information_search.html', {'lists' : lists, 'list' : list})

@csrf_exempt
def manager_head_teacher_basic_information(request):
    if request.method == 'POST':
        id = request.POST.get('t_b_id')
        name = request.POST.get('t_b_name')
        sex = request.POST.get('t_b_sex')
        funds = request.POST.get('t_b_funds')
        subject = request.POST.get('t_b_subject')
        list_task = Teacher.objects.all().filter(teacher_id=id)
        if list_task.exists():
            if list_task[0].teacher_status == 1:
                Teacher.objects.all().filter(teacher_id=id).update(teacher_id=id,
                                                                   teacher_name=name,
                                                                   teacher_sex=sex,
                                                                   teacher_funds=funds,
                                                                   teacher_subject=subject,
                                                                   teacher_status=5)
            elif list_task[0].teacher_status == 2:
                Teacher.objects.all().filter(teacher_id=id).update(teacher_id=id,
                                                                   teacher_name=name,
                                                                   teacher_sex=sex,
                                                                   teacher_funds=funds,
                                                                   teacher_subject=subject,
                                                                   teacher_status=6)
            elif list_task[0].teacher_status == 4:
                Teacher.objects.all().filter(teacher_id=id).update(teacher_id=id,
                                                                   teacher_name=name,
                                                                   teacher_sex=sex,
                                                                   teacher_funds=funds,
                                                                   teacher_subject=subject,
                                                                   teacher_status=7)
        else:
            Teacher.objects.create(teacher_id=id,
                                   teacher_name=name,
                                   teacher_sex=sex,
                                   teacher_funds=funds,
                                   teacher_subject=subject,
                                   teacher_status=3)
    return render(request, 'manager/manager_head_teacher_basic_information.html', {})