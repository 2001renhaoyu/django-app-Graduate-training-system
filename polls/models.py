from django.db import models
from django.db.models.fields import CharField

# Create your models here.


class AcademicActivity(models.Model):
    aca_activity_id = models.CharField(max_length=30, primary_key=True)
    aca_activity_name = models.CharField(max_length=30)
    aca_student_id = models.CharField(max_length=30)
    aca_activity_location = models.CharField(max_length=30)
    aca_activity_date = models.DateField()
    aca_report_name_zh = models.CharField(max_length=30)
    aca_report_name_en = models.CharField(max_length=50)
    aca_evidentiary_material = models.CharField(max_length=50)
    aca_audit_situation = models.CharField(max_length=20)
    aca_extra = models.CharField(max_length=100)


class AcheievementIndex(models.Model):
    ache_id = models.CharField(max_length=50, primary_key=True)
    ache_stu_if = models.CharField(max_length=30)
    ache_type = models.CharField(max_length=10)


class Book(models.Model):
    ache_id = models.CharField(max_length=50, primary_key=True)
    bo_name = models.CharField(max_length=50)
    bo_pub = models.CharField(max_length=50)
    bo_time = models.DateField()
    bo_rank = models.IntegerField()
    bo_evidence = models.CharField(50)


class Course(models.Model):
    course_id = models.CharField(max_length=30, primary_key=True)
    course_name = models.CharField(max_length=30)
    course_hours = models.CharField(max_length=50)
    course_scores = models.CharField(max_length=50)
    course_number = models.CharField(max_length=50)
    course_academy = models.CharField(max_length=50)
    course_subject = models.CharField(max_length=50)
    course_teacher_id = models.CharField(max_length=30)
    course_schedule = models.CharField(max_length=50)
    course_assessment_method = models.CharField(max_length=50)
    course_nature = models.CharField(max_length=50)


class Patent(models.Model):
    ache_id = models.CharField(max_length=50, primary_key=True)
    pa_name = models.CharField(max_length=50)
    pa_rank = models.IntegerField()
    pa_time = models.DateField()
    pa_state = models.IntegerField()
    p_evidence = models.CharField(max_length=50)
    p_num = models.CharField(max_length=50)


class Project(models.Model):
    pro_id = models.CharField(max_length=30, primary_key=True)
    pro_type = models.CharField(max_length=30)
    pro_name = models.CharField(max_length=30)
    pro_tutor_id = models.CharField(max_length=30)


class Report(models.Model):
    ache_id = models.CharField(max_length=50, primary_key=True)
    rep_name = models.CharField(max_length=50)
    rep_port = models.CharField(max_length=50)
    rep_time = models.DateField()
    rep_num = models.IntegerField()
    rep_evidence = models.CharField(max_length=100)


class Reward(models.Model):
    ache_id = models.CharField(max_length=50, primary_key=True)
    re_name = models.CharField(max_length=50)
    re_level = models.CharField(max_length=50)
    re_grade = models.CharField(max_length=50)
    re_num = models.IntegerField()
    re_time = models.DateField()
    re_evidence = models.CharField(max_length=50)


class Student(models.Model):
    stu_id = models.CharField(max_length=30, primary_key=True)
    stu_name = models.CharField(max_length=30)
    stu_subject = models.CharField(max_length=30)
    stu_sex = models.CharField(max_length=1)
    stu_type = models.CharField(max_length=10)
    stu_tutor_id = models.CharField(max_length=30)


class Teacher(models.Model):
    teacher_id = models.CharField(max_length=30, primary_key=True)
    teacher_name = models.CharField(max_length=30)
    teacher_sex = models.CharField(max_length=1)
    teacher_funds = models.DecimalField(max_digits=6, decimal_places=1)
    teacher_status = models.IntegerField()


class User(models.Model):
    log_id = models.CharField(max_length=30, primary_key=True)
    log_pwd = models.CharField(max_length=30)
    log_type = models.CharField(max_length=30)
