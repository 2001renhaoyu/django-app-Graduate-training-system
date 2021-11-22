# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Academicactivity(models.Model):
    aca_activity_id = models.CharField(primary_key=True, max_length=30)
    aca_activity_name = models.CharField(max_length=30)
    aca_student = models.ForeignKey('Student', models.DO_NOTHING)
    aca_activity_location = models.CharField(max_length=30)
    aca_activity_date = models.DateField()
    aca_report_name_zh = models.CharField(max_length=30)
    aca_report_name_en = models.CharField(max_length=50)
    aca_evidentiary_material = models.CharField(max_length=50)
    aca_audit_situation = models.CharField(max_length=20)
    aca_extra = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'AcademicActivity'


class Acheievementindex(models.Model):
    ache_id = models.CharField(primary_key=True, max_length=50)
    ache_stu_id = models.CharField(max_length=30)
    ache_type = models.CharField(max_length=10)
    ache_evidence = models.CharField(max_length=100)
    ache_audit_situation = models.CharField(max_length=10)

    class Meta:
        managed = False
        db_table = 'AcheievementIndex'


class Assistantjob(models.Model):
    ass_stu = models.ForeignKey('Student', models.DO_NOTHING)
    ass_course = models.ForeignKey('Courses', models.DO_NOTHING)
    ass_teacher_evaluate = models.CharField(max_length=100, blank=True, null=True)
    ass_stu_evaluate = models.CharField(max_length=100, blank=True, null=True)
    ass_result = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'AssistantJob'


class Book(models.Model):
    bo_name = models.CharField(max_length=50)
    bo_pub = models.CharField(max_length=50)
    bo_time = models.DateField()
    bo_rank = models.IntegerField()
    ache = models.ForeignKey(Acheievementindex, models.DO_NOTHING, primary_key=True)

    class Meta:
        managed = False
        db_table = 'Book'


class BookV(models.Model):
    id = models.CharField(max_length=50, primary_key=True)
    书名 = models.CharField(max_length=50)
    出版社 = models.CharField(max_length=50)
    出版时间 = models.DateField()
    贡献度 = models.IntegerField()
    学生名 = models.CharField(max_length=30)
    材料 = models.CharField(max_length=100)
    导师id = models.CharField(max_length=30)
    审核情况 = models.CharField(max_length=10)

    class Meta:
        managed = False  # Created from a view. Don't remove.
        db_table = 'Book_v'


class Courses(models.Model):
    course_id = models.CharField(primary_key=True, max_length=30)
    course_name = models.CharField(max_length=30)
    course_hours = models.CharField(max_length=50)
    course_scores = models.CharField(max_length=50)
    course_number = models.CharField(max_length=50)
    course_academy = models.CharField(max_length=50)
    course_subject = models.CharField(max_length=50)
    course_teacher = models.ForeignKey('Teacher', models.DO_NOTHING)
    course_schedule = models.CharField(max_length=50)
    course_assessment_method = models.CharField(max_length=50)
    course_nature = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'Courses'


class Identifyproject(models.Model):
    ip_stu = models.ForeignKey('Student', models.DO_NOTHING)
    ip_pro = models.ForeignKey('Project', models.DO_NOTHING)
    ip_job_content = models.CharField(max_length=100)
    ip_begintime = models.DateField()
    ip_endtime = models.DateField()
    ip_funds = models.DecimalField(max_digits=6, decimal_places=1)
    ip_status = models.IntegerField()
    ip_mid_status = models.IntegerField()
    ip_path = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'IdentifyProject'


class Patent(models.Model):
    pa_name = models.CharField(max_length=50)
    pa_type = models.CharField(max_length=50)
    pa_rank = models.IntegerField()
    pa_time = models.DateField()
    pa_state = models.CharField(max_length=50)
    pa_num = models.CharField(max_length=50)
    ache = models.ForeignKey(Acheievementindex, models.DO_NOTHING, primary_key=True)

    class Meta:
        managed = False
        db_table = 'Patent'


class PatentV(models.Model):
    id = models.CharField(max_length=50, primary_key=True)
    专利名称 = models.CharField(max_length=50)
    专利类型 = models.CharField(max_length=50)
    专利号 = models.IntegerField()
    专利发布时间 = models.DateField()
    专利状态 = models.CharField(max_length=50)
    贡献度 = models.CharField(max_length=50)
    材料 = models.CharField(max_length=100)
    学生名 = models.CharField(max_length=30)
    导师id = models.CharField(max_length=30)
    审核情况 = models.CharField(max_length=10)

    class Meta:
        managed = False  # Created from a view. Don't remove.
        db_table = 'Patent_v'


class Project(models.Model):
    pro_id = models.CharField(primary_key=True, max_length=30)
    pro_type = models.CharField(max_length=30)
    pro_name = models.CharField(max_length=30)
    pro_tutor = models.ForeignKey('Teacher', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'Project'


class Report(models.Model):
    rep_name = models.CharField(max_length=50)
    rep_type = models.CharField(max_length=50)
    rep_port = models.CharField(max_length=50)
    rep_time = models.DateField()
    rep_num = models.IntegerField()
    ache = models.ForeignKey(Acheievementindex, models.DO_NOTHING, primary_key=True)

    class Meta:
        managed = False
        db_table = 'Report'


class ReportV(models.Model):
    id = models.CharField(max_length=50, primary_key=True)
    报告名 = models.CharField(max_length=50)
    报告类型 = models.CharField(max_length=50)
    服务单位 = models.CharField(max_length=50)
    报告时间 = models.DateField()
    贡献度排名 = models.IntegerField()
    材料 = models.CharField(max_length=100)
    学生名 = models.CharField(max_length=30)
    导师id = models.CharField(max_length=30)
    审核情况 = models.CharField(max_length=10)

    class Meta:
        managed = False  # Created from a view. Don't remove.
        db_table = 'Report_v'


class Reward(models.Model):
    re_name = models.CharField(max_length=50)
    re_level = models.CharField(max_length=50)
    re_grade = models.CharField(max_length=50)
    re_num = models.IntegerField()
    re_time = models.DateField()
    ache = models.ForeignKey(Acheievementindex, models.DO_NOTHING, primary_key=True)

    class Meta:
        managed = False
        db_table = 'Reward'


class RewardV(models.Model):
    id = models.CharField(max_length=50, primary_key=True)
    奖励名称 = models.CharField(max_length=50)
    奖励等级 = models.CharField(max_length=50)
    获奖等级 = models.CharField(max_length=50)
    排名 = models.IntegerField()
    获奖时间 = models.DateField()
    材料 = models.CharField(max_length=100)
    学生名 = models.CharField(max_length=30)
    导师id = models.CharField(max_length=30)
    审核情况 = models.CharField(max_length=10)

    class Meta:
        managed = False  # Created from a view. Don't remove.
        db_table = 'Reward_v'


class Softwarehardware(models.Model):
    so_name = models.CharField(max_length=50)
    so_server = models.CharField(max_length=50)
    so_time = models.DateField()
    so_rank = models.IntegerField()
    ache = models.ForeignKey(Acheievementindex, models.DO_NOTHING, primary_key=True)

    class Meta:
        managed = False
        db_table = 'SoftwareHardware'


class SoftwarehardwareV(models.Model):
    id = models.CharField(max_length=50, primary_key=True)
    名称 = models.CharField(max_length=50)
    服务单位 = models.CharField(max_length=50)
    上线时间 = models.DateField()
    贡献度 = models.IntegerField()
    材料 = models.CharField(max_length=100)
    学生名 = models.CharField(max_length=30)
    审核情况 = models.CharField(max_length=10)
    导师id = models.CharField(max_length=30)

    class Meta:
        managed = False  # Created from a view. Don't remove.
        db_table = 'SoftwareHardware_v'


class Standard(models.Model):
    sta_name = models.CharField(max_length=50)
    sta_level = models.CharField(max_length=50)
    sta_time = models.DateField()
    ache = models.ForeignKey(Acheievementindex, models.DO_NOTHING, primary_key=True)

    class Meta:
        managed = False
        db_table = 'Standard'


class StandardV(models.Model):
    id = models.CharField(max_length=50, primary_key=True)
    标准名称 = models.CharField(max_length=50)
    标准级别 = models.CharField(max_length=50)
    标准时间 = models.DateField()
    材料 = models.CharField(max_length=100)
    学生名 = models.CharField(max_length=30)
    审核情况 = models.CharField(max_length=10)
    导师id = models.CharField(max_length=30)

    class Meta:
        managed = False  # Created from a view. Don't remove.
        db_table = 'Standard_v'


class Student(models.Model):
    stu_name = models.CharField(max_length=30)
    stu_id = models.CharField(primary_key=True, max_length=30)
    stu_subject = models.CharField(max_length=30, blank=True, null=True)
    stu_sex = models.CharField(max_length=1)
    stu_type = models.CharField(max_length=10)
    stu_tutor = models.ForeignKey('Teacher', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'Student'


class Teacher(models.Model):
    teacher_id = models.CharField(primary_key=True, max_length=30)
    teacher_name = models.CharField(max_length=30)
    teacher_sex = models.CharField(max_length=1)
    teacher_funds = models.DecimalField(max_digits=6, decimal_places=1, blank=True, null=True)
    teacher_status = models.IntegerField()
    teacher_subject = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = 'Teacher'


class Teacherselect(models.Model):
    course = models.ForeignKey(Courses, models.DO_NOTHING)
    stu = models.ForeignKey(Student, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'TeacherSelect'


class Thesis(models.Model):
    the_name = models.CharField(max_length=100)
    the_book_name = models.CharField(max_length=100)
    the_state = models.CharField(max_length=50)
    the_time = models.DateField(blank=True, null=True)
    the_type = models.CharField(max_length=50)
    the_pub = models.CharField(max_length=50)
    ache = models.ForeignKey(Acheievementindex, models.DO_NOTHING, primary_key=True)

    class Meta:
        managed = False
        db_table = 'Thesis'


class ThesisV(models.Model):
    id = models.CharField(max_length=50, primary_key=True)
    学生名 = models.CharField(max_length=30)
    材料 = models.CharField(max_length=100)
    论文名 = models.CharField(max_length=100)
    刊物名称 = models.CharField(max_length=100)
    论文状态 = models.CharField(max_length=50)
    发表时间 = models.DateField(blank=True, null=True)
    类型 = models.CharField(max_length=50)
    归属库 = models.CharField(max_length=50)
    审核情况 = models.CharField(max_length=10)
    导师id = models.CharField(max_length=30)

    class Meta:
        managed = False  # Created from a view. Don't remove.
        db_table = 'Thesis_v'


class Users(models.Model):
    log_id = models.CharField(primary_key=True, max_length=30)
    log_pwd = models.CharField(max_length=30)
    log_type = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = 'Users'


class Volunteerapplication(models.Model):
    stu = models.ForeignKey(Student, models.DO_NOTHING)
    course = models.ForeignKey(Courses, models.DO_NOTHING)
    priority = models.CharField(max_length=10)

    class Meta:
        managed = False
        db_table = 'VolunteerApplication'


class Volunteerapplicationconfig(models.Model):
    state = models.CharField(max_length=10)
    maxnum_volunteer = models.IntegerField(db_column='maxNum_volunteer')  # Field name made lowercase.
    time_start = models.DateTimeField()
    time_end = models.DateTimeField()
    teacher = models.ForeignKey(Teacher, models.DO_NOTHING, primary_key=True)
    sort_method = models.CharField(max_length=50, blank=True, null=True)
    subject = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'VolunteerApplicationConfig'


class DjangoContentType(models.Model):
    name = models.CharField(max_length=100)
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'
