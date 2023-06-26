from django.db import connection
from django.http import JsonResponse
from django.shortcuts import render
import json


# 查询所有
def showdata(request):
    if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':  # 检查是否是AJAX请求
        # 执行SQL查询
        with connection.cursor() as cursor:
            sql = "SELECT stu.stu_id AS `id`, stu.stu_name AS `学生`, stu.stu_number AS `学号`, stu.stu_password AS `学生密码`, stu.stu_phone AS `学生号码`, stu.stu_wechat AS `学生微信`, spe.spe_name AS `专业`, sch.sch_name AS `学校`, pap.pap_title AS `题目`, pap.pap_count AS `字数`, pap.pap_check AS `查重率`, pap.pap_character AS `论文性质`, pro.pro_newadd AS `新增时间`, pro.pro_opening AS `开题时间`, pro.pro_main AS `正文时间`, wri.wri_name AS `写手`, wri.wri_class AS `写手性质`, age.age_name AS `代理` FROM students AS stu JOIN relations AS rel ON rel.stu_id = stu.stu_id JOIN papers AS pap ON rel.pap_id = pap.pap_id JOIN schools AS sch ON rel.sch_id = sch.sch_id JOIN specialists AS spe ON rel.spe_id = spe.spe_id JOIN writers AS wri ON rel.wri_id = wri.wri_id JOIN agents AS age ON rel.age_id = age.age_id JOIN progress AS pro ON rel.pro_id = pro.pro_id;"
            cursor.execute(sql)
            data = cursor.fetchall()

        # 构建JSON响应
        response_data = []
        for item in data:
            response_data.append({
                'id': item[0],
                '学生': item[1],
                '学号': item[2],
                '学生密码': item[3],
                '学生号码': item[4],
                '学生微信': item[5],
                '专业': item[6],
                '学校': item[7],
                '题目': item[8],
                '字数': item[9],
                '查重率': item[10],
                '论文性质': item[11],
                '新增时间': item[12],
                '开题时间': item[13],
                '正文时间': item[14],
                '写手': item[15],
                '写手性质': item[16],
                '代理': item[17],
            })

        return JsonResponse({'data': response_data})
    else:
        return render(request, 'home.html')


# 显示列
def choose(request):
    if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        if request.method == 'GET':
            selected_values = request.GET.getlist('selected[]')

        with connection.cursor() as cursor:
            column_names = ', '.join(selected_values)
            sql = f"SELECT {column_names} FROM students AS stu JOIN relations AS rel ON rel.stu_id = stu.stu_id JOIN papers AS pap ON rel.pap_id = pap.pap_id JOIN schools AS sch ON rel.sch_id = sch.sch_id JOIN specialists AS spe ON rel.spe_id = spe.spe_id JOIN writers AS wri ON rel.wri_id = wri.wri_id JOIN agents AS age ON rel.age_id = age.age_id JOIN progress AS pro ON rel.pro_id = pro.pro_id;"
            cursor.execute(sql)
            results = cursor.fetchall()

        return JsonResponse({'data': results})
    else:
        return render(request, 'choose.html')


# 配合显示列查询
def select(request):
    if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        if request.method == 'GET':
            selected = request.GET.getlist('selected[]')
            inputNames = request.GET.getlist('inputNames[]')
            selectData = request.GET.getlist('selectData[]')
            conditions = []
            # 判断多选框的值，为空则显示全部列，否则显示多选框列
            if selected:
                selected_columns = ', '.join(selected)  # 将选中的列拼接起来
            else:
                selected_columns = """
                    stu.stu_name AS `学生`,
                    stu.stu_number AS `学号`,
                    stu.stu_password AS `学生密码`,
                    stu.stu_phone AS `学生号码`,
                    stu.stu_wechat AS `学生微信`,
                    spe.spe_name AS `专业`,
                    sch.sch_name AS `学校`,
                    pap.pap_title AS `题目`,
                    pap.pap_count AS `字数`,
                    pap.pap_check AS `查重率`,
                    pap.pap_character AS `论文性质`,
                    pro.pro_newadd AS `新增时间`,
                    pro.pro_opening AS `开题时间`,
                    pro.pro_main AS `正文时间`,
                    wri.wri_name AS `写手`,
                    wri.wri_class AS `写手性质`,
                    age.age_name AS `代理`
                """

            for column, value in zip(inputNames, selectData):
                if column and value:  # 检查 column 和 value 是否都不为空
                    condition = {'column': column, 'value': value}
                    conditions.append(condition)

            # 构建 WHERE 子句
            where_clause = ' AND '.join([f"{condition['column']} = %s" for condition in conditions])

            # 提取所有条件的值
            values = [condition['value'] for condition in conditions]

            # 构建完整的 SQL 查询语句
            sql = f"SELECT {selected_columns} FROM students AS stu JOIN relations AS rel ON rel.stu_id = stu.stu_id JOIN papers AS pap ON rel.pap_id = pap.pap_id JOIN schools AS sch ON rel.sch_id = sch.sch_id JOIN specialists AS spe ON rel.spe_id = spe.spe_id JOIN writers AS wri ON rel.wri_id = wri.wri_id JOIN agents AS age ON rel.age_id = age.age_id JOIN progress AS pro ON rel.pro_id = pro.pro_id"

            if where_clause:
                sql += f" WHERE {where_clause};"

            with connection.cursor() as cursor:
                cursor.execute(sql, values)
                results = cursor.fetchall()
            return JsonResponse({'data': results})
    else:
        return render(request, 'choose.html')


# 下拉栏数据逻辑
def bar(request):
    school_sql = 'SELECT sch_name FROM schools'
    spe_sql = 'SELECT spe_name FROM specialists'
    wri_sql = 'SELECT wri_name FROM writers'
    age_sql = 'SELECT age_name FROM agents'

    # 学校下拉栏
    with connection.cursor() as cursor:
        cursor.execute(school_sql)
        school_results = cursor.fetchall()
    # 专业下拉栏
    with connection.cursor() as cursor:
        cursor.execute(spe_sql)
        spe_results = cursor.fetchall()
    # 写手下拉栏
    with connection.cursor() as cursor:
        cursor.execute(wri_sql)
        wri_results = cursor.fetchall()
    # 代理下拉栏
    with connection.cursor() as cursor:
        cursor.execute(age_sql)
        age_results = cursor.fetchall()
    data = {'schools': school_results, 'specialists': spe_results, 'writers': wri_results, 'agents': age_results}
    return JsonResponse(data)


# 新增论文逻辑
def insert(request):
    if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        if request.method == 'GET':
            inputData = request.GET.getlist('input[]')  # 拿到新增论文输入框的值

            # 有论文表除了论文性质外的值就接着传
            pap_lists = ['pap_character']
            pap_val = inputData[10]
            if inputData[7]:
                pap_lists.insert(0, 'pap_title')
                pap_val = inputData[7] + inputData[10]  # 论文表表赋值下标7.10
                if inputData[8]:
                    pap_lists.insert(1, 'pap_count')
                    pap_val = ''.join(inputData[7:9]) + inputData[10]  # 论文表表赋值下标7.8.10
                    if inputData[9]:
                        pap_lists.insert(2, 'pap_check')
                        pap_val = inputData[7:11]  # 论文表表赋值下标7-10

            # 有学生表除了名字外的值就接着传
            stu_lists = ['stu_name']
            stu_val = inputData[0]
            if inputData[1]:
                stu_lists.append('stu_number')
                stu_val = inputData[0:2]  # 学生表赋值下标0.1
                if inputData[2]:
                    stu_lists.append('stu_password')
                    stu_val = inputData[0:3]  # 学生表赋值下标0-2
                    if inputData[3]:
                        stu_lists.append('stu_phone')
                        stu_val = inputData[0:4]  # 学生表赋值下标0-3
                        if inputData[4]:
                            stu_lists.append('stu_wechat')
                            stu_val = inputData[0:5]  # 学生表赋值下标0-4

            # 有开题和正文时间就接着传
            pro_lists = ['pro_newadd']
            pro_val = inputData[11]
            if inputData[12]:
                pro_lists.append('pro_opening')
                pro_val = inputData[11:13]  # 进度表赋值11.12
                if inputData[13]:
                    pro_lists.append('pro_main')
                    pro_val = inputData[11:14]  # 进度表赋值11-13

            spe_val = inputData[5]  # 专业赋值
            sch_val = inputData[6]  # 学校赋值
            wri_val = inputData[14]  # 写手赋值
            age_val = inputData[15]  # 代理赋值
            sql = f"START TRANSACTION; "

            # 检查学生表的值，单个赋值多个拼接
            if isinstance(stu_val, list):
                stu_val_str = ', '.join([repr(val) for val in stu_val])
            else:
                stu_val_str = repr(stu_val)
            sql += f"INSERT INTO students ({', '.join(stu_lists)}) VALUES ({stu_val_str}); "

            # 检查论文表的值，单个赋值多个拼接
            if isinstance(pap_val, list):
                pap_val_str = ', '.join([repr(val) for val in pap_val])
            else:
                pap_val_str = repr(pap_val)
            sql += f"INSERT INTO papers ({', '.join(pap_lists)}) VALUES ({pap_val_str}); "

            # 检查进度表的值，单个赋值多个拼接
            if isinstance(pro_val, list):
                pro_val_str = ', '.join([repr(val) for val in pro_val])
            else:
                pro_val_str = repr(pro_val)
            sql += f"INSERT INTO progress ({', '.join(pro_lists)}) VALUES ({pro_val_str}); "

            sql += f"INSERT INTO relations (stu_id, spe_id, sch_id, pap_id, wri_id, age_id, pro_id) "
            sql += f"SELECT stu.stu_id, spe.spe_id, sch.sch_id, pap.pap_id, wri.wri_id, age.age_id, pro.pro_id FROM students stu "
            sql += f"JOIN specialists spe ON spe.spe_name = '{spe_val}' "
            sql += f"JOIN schools sch ON sch.sch_name = '{sch_val}' "
            sql += f"JOIN (SELECT pap_id FROM papers ORDER BY pap_id DESC LIMIT 1) pap ON 1=1 "
            sql += f"JOIN writers wri ON wri.wri_name = '{wri_val}' "
            sql += f"JOIN agents age ON age.age_name = '{age_val}' "
            sql += f"JOIN (SELECT pro_id FROM progress ORDER BY pro_id DESC LIMIT 1) pro ON 1=1 "
            sql += f"ORDER BY stu.stu_id DESC LIMIT 1; "
            sql += f"COMMIT;"
            with connection.cursor() as cursor:
                cursor.execute(sql)
                results = cursor.fetchall()
            return JsonResponse({'data': results})
    else:
        return render(request, 'choose.html')


# 修改论文前搜索逻辑
def modifyselect(request):
    if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        if request.method == 'GET':
            stu_name = request.GET.get('stu_name')
            pap_title = request.GET.get('pap_title')
            if stu_name:
                sql = f"SELECT stu.stu_id AS id, stu.stu_name AS 学生, stu.stu_number AS 学号, stu.stu_password AS 学生密码, stu.stu_phone AS 学生号码, stu.stu_wechat AS 学生微信, spe.spe_name AS 专业, sch.sch_name AS 学校, pap.pap_title AS 题目, pap.pap_count AS 字数, pap.pap_check AS 查重率, pap.pap_character AS 论文性质, pro.pro_newadd AS 新增时间, pro.pro_opening AS 开题时间, pro.pro_main AS 正文时间, wri.wri_name AS 写手, wri.wri_class AS 写手性质, age.age_name AS 代理 FROM students AS stu JOIN relations AS rel ON rel.stu_id = stu.stu_id JOIN papers AS pap ON rel.pap_id = pap.pap_id JOIN schools as sch ON rel.sch_id = sch.sch_id JOIN specialists AS spe ON rel.spe_id = spe.spe_id JOIN writers AS wri ON rel.wri_id = wri.wri_id JOIN agents AS age ON rel.age_id = age.age_id JOIN progress AS pro ON rel.pro_id = pro.pro_id WHERE stu.stu_name = '{stu_name}'"
                if pap_title:
                    sql = f"SELECT stu.stu_id AS id, stu.stu_name AS 学生, stu.stu_number AS 学号, stu.stu_password AS 学生密码, stu.stu_phone AS 学生号码, stu.stu_wechat AS 学生微信, spe.spe_name AS 专业, sch.sch_name AS 学校, pap.pap_title AS 题目, pap.pap_count AS 字数, pap.pap_check AS 查重率, pap.pap_character AS 论文性质, pro.pro_newadd AS 新增时间, pro.pro_opening AS 开题时间, pro.pro_main AS 正文时间, wri.wri_name AS 写手, wri.wri_class AS 写手性质, age.age_name AS 代理 FROM students AS stu JOIN relations AS rel ON rel.stu_id = stu.stu_id JOIN papers AS pap ON rel.pap_id = pap.pap_id JOIN schools as sch ON rel.sch_id = sch.sch_id JOIN specialists AS spe ON rel.spe_id = spe.spe_id JOIN writers AS wri ON rel.wri_id = wri.wri_id JOIN agents AS age ON rel.age_id = age.age_id JOIN progress AS pro ON rel.pro_id = pro.pro_id WHERE stu.stu_name = '{stu_name}' AND pap.pap_title = '{pap_title}'"

                with connection.cursor() as cursor:
                    cursor.execute(sql)
                    results = cursor.fetchall()
        return JsonResponse({'data': results})
    else:
        return render(request, 'choose.html')


def modify(request):
    results = []  # 默认空列表
    if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        if request.method == 'GET':
            rowName = request.GET.getlist('rowName[]')
            modify = request.GET.getlist('modify[]')
            id = request.GET.get('id')

            # 修改表
            tabName = []
            rowNamePrev = []
            whereID = []
            for i in range(len(rowName)):
                rowNamePrev.append(rowName[i][:3])  # 获取前三个字符
                if rowNamePrev[i] == "stu":
                    tabName.append("students")
                if rowNamePrev[i] == "pap":
                    tabName.append("papers")
                if rowNamePrev[i] == "pro":
                    tabName.append("progress")
                if rowNamePrev[i] == "spe":
                    tabName.append("specialists")
                if rowNamePrev[i] == "sch":
                    tabName.append("schools")
                if rowNamePrev[i] == "wri":
                    tabName.append("writers")
                if rowNamePrev[i] == "age":
                    tabName.append("agents")

            # 修改列
            for i in range(len(rowName)):
                rowName[i] = rowName[i][4:]
                whereID.append(rowName[i][:4] + 'id')

            print(tabName)
            print(rowName)
            print(modify)
            print(whereID)

            for i in range(len(tabName)):
                if tabName[i] == "students" or tabName[i] == "papers" or tabName[i] == "progress":
                    sql = f"UPDATE {tabName[i]} SET {rowName[i]} = '{modify[i]}' WHERE {whereID[i]} = {id}"
                    print(sql)
                    with connection.cursor() as cursor:
                        cursor.execute(sql)
                        results = cursor.fetchall()

                else:
                    sql = f"UPDATE relations SET {whereID[i]} = (SELECT {whereID[i]} FROM {tabName[i]} WHERE {rowName[i]} = '{modify[i]}') WHERE rel_id = {id}"
                    print(sql)
                    with connection.cursor() as cursor:
                        cursor.execute(sql)
                        results = cursor.fetchall()

        return JsonResponse({'data': results})
    else:
        return render(request, 'choose.html')


def speselect(request):
    sql = 'SELECT * FROM specialists'
    with connection.cursor() as cursor:
        cursor.execute(sql)
        results = cursor.fetchall()
    return JsonResponse({'data': results})


def speselid(request):
    if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        if request.method == 'GET':
            input_id = request.GET.get('input_id')
            sql = f'SELECT spe_name FROM specialists WHERE spe_id = {input_id}'
            with connection.cursor() as cursor:
                cursor.execute(sql)
                results = cursor.fetchall()
        return JsonResponse({'data': results})
    else:
        return render(request, 'specialists.html')


def modifyspe(request):
    if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        if request.method == 'GET':
            spe_id = request.GET.get('spe_id')
            spe_name = request.GET.get('spe_name')
            sql = f"UPDATE specialists SET spe_name ='{spe_name}' WHERE spe_id = {spe_id}"
            with connection.cursor() as cursor:
                cursor.execute(sql)
                results = cursor.fetchall()
        return JsonResponse({'data': results})
    else:
        return render(request, 'specialists.html')


def insertspe(request):
    if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        if request.method == 'GET':
            spe_name = request.GET.get('spe_name')
            sql = f"INSERT IGNORE INTO specialists(spe_name) VALUES ('{spe_name}')"
            with connection.cursor() as cursor:
                cursor.execute(sql)
                results = cursor.fetchall()
        return JsonResponse({'data': results})
    else:
        return render(request, 'specialists.html')


def deletespe(request):
    if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        if request.method == 'GET':
            spe_id = request.GET.get('spe_id')
            sql = f"DELETE FROM specialists WHERE spe_id='{spe_id}';"
            with connection.cursor() as cursor:
                cursor.execute(sql)
                results = cursor.fetchall()
        return JsonResponse({'data': results})
    else:
        return render(request, 'specialists.html')


def writers(request):
    sql = 'SELECT * FROM writers'
    with connection.cursor() as cursor:
        cursor.execute(sql)
        results = cursor.fetchall()
    return JsonResponse({'data': results})


def wriselid(request):
    if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        if request.method == 'GET':
            wri_id = request.GET.get('wri_id')
            sql = f'SELECT wri_name,wri_class FROM writers WHERE wri_id = {wri_id}'
            with connection.cursor() as cursor:
                cursor.execute(sql)
                results = cursor.fetchall()
        return JsonResponse({'data': results})
    else:
        return render(request, 'writers.html.html')


def modifywri(request):
    if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        if request.method == 'GET':
            wri_id = request.GET.get('wri_id')
            wri_name = request.GET.get('wri_name')
            wri_class = request.GET.get('wri_class')
            sql = f"UPDATE writers SET wri_name ='{wri_name}',wri_class = '{wri_class}' WHERE wri_id = {wri_id}"
            with connection.cursor() as cursor:
                cursor.execute(sql)
                results = cursor.fetchall()
        return JsonResponse({'data': results})
    else:
        return render(request, 'writers.html')


def insertwri(request):
    if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        if request.method == 'GET':
            wri_name = request.GET.get('wri_name')
            wri_class = request.GET.get('wri_class')
            sql = f"INSERT IGNORE INTO writers(wri_name,wri_class) VALUES ('{wri_name}','{wri_class}')"
            with connection.cursor() as cursor:
                cursor.execute(sql)
                results = cursor.fetchall()
        return JsonResponse({'data': results})
    else:
        return render(request, 'specialists.html')


def deletewri(request):
    if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        if request.method == 'GET':
            wri_id = request.GET.get('wri_id')
            sql = f"DELETE FROM writers WHERE wri_id='{wri_id}';"
            with connection.cursor() as cursor:
                cursor.execute(sql)
                results = cursor.fetchall()
        return JsonResponse({'data': results})
    else:
        return render(request, 'writers.html')


def schselect(request):
    sql = 'SELECT * FROM schools'
    with connection.cursor() as cursor:
        cursor.execute(sql)
        results = cursor.fetchall()
    return JsonResponse({'data': results})


def schselid(request):
    if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        if request.method == 'GET':
            input_id = request.GET.get('input_id')
            sql = f'SELECT sch_name FROM schools WHERE sch_id = {input_id}'
            with connection.cursor() as cursor:
                cursor.execute(sql)
                results = cursor.fetchall()
        return JsonResponse({'data': results})
    else:
        return render(request, 'schools.html')


def modifysch(request):
    if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        if request.method == 'GET':
            sch_id = request.GET.get('sch_id')
            sch_name = request.GET.get('sch_name')
            sql = f"UPDATE schools SET sch_name ='{sch_name}' WHERE sch_id = {sch_id}"
            with connection.cursor() as cursor:
                cursor.execute(sql)
                results = cursor.fetchall()
        return JsonResponse({'data': results})
    else:
        return render(request, 'schools.html')


def insertspe(request):
    if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        if request.method == 'GET':
            sch_name = request.GET.get('sch_name')
            sql = f"INSERT IGNORE INTO schools(sch_name) VALUES ('{sch_name}')"
            with connection.cursor() as cursor:
                cursor.execute(sql)
                results = cursor.fetchall()
        return JsonResponse({'data': results})
    else:
        return render(request, 'schools.html')


def deletesch(request):
    if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        if request.method == 'GET':
            sch_id = request.GET.get('sch_id')
            sql = f"DELETE FROM schools WHERE sch_id='{sch_id}';"
            with connection.cursor() as cursor:
                cursor.execute(sql)
                results = cursor.fetchall()
        return JsonResponse({'data': results})
    else:
        return render(request, 'schools.html')


def ageselect(request):
    sql = 'SELECT * FROM agents'
    with connection.cursor() as cursor:
        cursor.execute(sql)
        results = cursor.fetchall()
    return JsonResponse({'data': results})


def ageselid(request):
    if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        if request.method == 'GET':
            input_id = request.GET.get('input_id')
            sql = f'SELECT age_name FROM agents WHERE age_id = {input_id}'
            with connection.cursor() as cursor:
                cursor.execute(sql)
                results = cursor.fetchall()
        return JsonResponse({'data': results})
    else:
        return render(request, 'agents.html')


def modifyage(request):
    if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        if request.method == 'GET':
            age_id = request.GET.get('age_id')
            age_name = request.GET.get('age_name')
            sql = f"UPDATE agents SET age_name ='{age_name}' WHERE age_id = {age_id}"
            with connection.cursor() as cursor:
                cursor.execute(sql)
                results = cursor.fetchall()
        return JsonResponse({'data': results})
    else:
        return render(request, 'agents.html')


def insertage(request):
    if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        if request.method == 'GET':
            age_name = request.GET.get('age_name')
            sql = f"INSERT IGNORE INTO agents(age_name) VALUES ('{age_name}')"
            with connection.cursor() as cursor:
                cursor.execute(sql)
                results = cursor.fetchall()
        return JsonResponse({'data': results})
    else:
        return render(request, 'agents.html')


def deleteage(request):
    if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        if request.method == 'GET':
            age_id = request.GET.get('age_id')
            sql = f"DELETE FROM agents WHERE age_id='{age_id}';"
            with connection.cursor() as cursor:
                cursor.execute(sql)
                results = cursor.fetchall()
        return JsonResponse({'data': results})
    else:
        return render(request, 'agents.html')
