
from polls.models import *


def get_academic_activity_list(student_id):
    # 初始化
    response = ""
    response1 = ""

    # 通过objects这个模型管理器的all()获得所有数据行，相当于SQL中的SELECT * FROM
    lists = Academicactivity.objects.all().filter(aca_student_id=student_id)

    # 输出所有数据
    return lists
