from django.db import models

# Create your models here.


class AcademicActivity(models.Model):
    aca_activity_id = models.CharField(max_length=30)
    aca_activity_name = models.CharField(max_length=30)
    aca_student_id = models.CharField(max_length=30)
    aca_activity_location = models.CharField(max_length=30)
    aca_activity_date = models.CharField(max_length=20)
    aca_report_name_zh = models.CharField(max_length=30)
    aca_report_name_en = models.CharField(max_length=50)
    aca_evidentiary_material = models.CharField(max_length=50)
    aca_audit_situation = models.CharField(max_length=20)
    aca_extra = models.CharField(max_length=100)
