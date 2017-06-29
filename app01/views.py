from django.shortcuts import render

# Create your views here.


from django.shortcuts import render, HttpResponseRedirect, HttpResponse, render_to_response
from app01.tools import CheckCode
from io import StringIO
from django.contrib import auth
import os


def checkcode(request):
    # 测试文件落地的方式
    # file_path = "D:\python\mybbs02\statics\checkcodes"
    # file_name = 'checkcode'
    # img_str, img_data = CheckCode.gene_code(file_path, file_name)

    # 调用gene_code函数生成验证字符串，生成验证码图片的数据流（二进制格式）
    img_str, img_data = CheckCode.gene_code()

    # 将验证码（字符串）保存到session中，以便login函数可以调用
    request.session["checkcode"] = img_str

    # 将验证码图片以文件流的形式返回，然后前端通过<img src="/your_url/">就可以读取到图片了
    # img_data = open(file_name+".png", 'rb').read()

    return HttpResponse(img_data)


def login(request):
    if request.method == 'POST':
        # 验证用户名和密码的代码段。。。
        username = request.POST.get('username')
        password = request.POST.get('password')

        # 从form表单获取用户输入的验证码
        check_code = request.POST.get('checkcode')

        # 获取通过 checkcod函数获取保存到 session的验证码字符串
        session_code = request.session["checkcode"]

        # 将用户输入的验证码 与后台session验证码 做比对：
        if check_code.strip().lower() != session_code.lower():
            return HttpResponse('验证码不匹配')
        else:
            return HttpResponse('验证码正确')

    return render(request, 'login.html', {'error': "", 'username': '', 'password': ''})
