from django.shortcuts import render
from django.db import connection


def showdata(request):
    # 执行SQL查询
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM students")
        data = cursor.fetchall()

    # 将数据传递给模板
    context = {'data': data}

    # 渲染模板并返回响应
    return render(request, 'home.html', context)
