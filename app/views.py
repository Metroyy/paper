from django.shortcuts import render
from django.db import connection


def showdata(request):
    # 执行SQL查询
    with connection.cursor() as cursor:
        cursor.execute("SELECT stu.stu_id AS `id`, stu.stu_name AS `学生`, sch.sch_name AS `学校`, spe.spe_name AS `专业`, pap.pap_title AS `题目`, pap.pap_count AS `字数`, pap.pap_check AS `查重率`, pap.pap_character AS `性质`, pro.pro_newadd AS `新增时间`, pro.pro_opening AS `开题时间`, pro.pro_main AS `正文时间`, wri.wir_name AS `写手` FROM students AS stu JOIN relations AS rel ON rel.stu_id = stu.stu_id JOIN papers AS pap ON rel.pap_id = pap.pap_id JOIN schools AS sch ON rel.sch_id = sch.sch_id JOIN specialists AS spe ON rel.spe_id = spe.spe_id JOIN writers AS wri ON rel.wri_id = wri.wri_id JOIN agents AS age ON rel.age_id = age.age_id JOIN progress AS pro ON rel.pro_id = pro.pro_id;")
        data = cursor.fetchall()

    # 将数据传递给模板
    context = {'data': data}

    # 渲染模板并返回响应
    return render(request, 'home.html', context)
