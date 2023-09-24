from datetime import date
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseForbidden
from pjapp import models
import ctypes
import os
from django.conf import settings
from pjapp import merge
from pjapp.utils import login_required_decorator
from pjapp.visual1 import Visualize

PRE_DIR = os.path.join(settings.BASE_DIR, "predict_data.txt")
SOU_DIR = os.path.join(settings.BASE_DIR, "source_data.txt")
OUT_SOURCE = os.path.join(settings.BASE_DIR, "out.txt")
OUT_DESTINATION = os.path.join(settings.BASE_DIR, "outfile")
OPERATION = os.path.join(settings.BASE_DIR, "function.so")
IMG_DIR = os.path.join(settings.BASE_DIR,"img")


# Create your views here.
def login(request):
    method = request.method
    if method == "GET":
        return render(request, "login.html")
    elif method == "POST":
        userid = request.POST.get("userid")
        password = request.POST.get("password")

        try:
            user = models.Users.objects.get(userId=userid)
            if password == user.passWord:
                request.session['mainpage'] = True
                html = "<div><h1>恭喜！登录成功！</h1><div><a href='/mainpage/'>进入首页</a></div></div>"
                # 将用户信息存储到session里面
                # request.session['username'] = user.username

            else:
                html = "<div><h1>sorry,密码错误，请重新输入密码</h1><div><a href=''>重新登录</a></div></div>"

            return HttpResponse(html)

        except models.Users.DoesNotExist:
            html = "<div><h1>sorry,用户名不存在</h1><div><a href=''>重新登录</a></div></div>"
            return HttpResponse(html)


def register(request):
    method = request.method  # 请求方法
    if method == "GET":
        return render(request, "register.html")
    elif method == "POST":
        userid = request.POST.get("id")
        username = request.POST.get("username")
        res = models.Users.objects.filter(userId=userid)

        """验证用户名是否存在"""
        if res:
            html = "<div><h1>sorry,用户id已被注册，请尝试新的用户id</h1><div><a href='/register/'>重新注册</a></div></div>"
            return HttpResponse(html)

        password = request.POST.get("password")

        """添加数据"""
        models.Users.objects.create(userId=userid, userName=username, passWord=password)

        html = "<div><h1>恭喜，注册成功！</h1><div><a href='/'>前往登录</div></div>"
        return HttpResponse(html)


def upload_file(request):
    if not request.session.get('mainpage'):
        return HttpResponseForbidden('Access Forbidden')
    if request.method == 'GET':
        project = models.Project.objects.all()
        return render(request, "upload_file.html", {"project": project})
    if request.method == 'POST':
        pfile = request.FILES['pfile']  # 获取上传的文件
        sfile = request.FILES['sfile']
        data_name = request.POST.get('data_name')
        project_id = request.POST.get('project_id')
        current_date = date.today()
        # 保存文件到磁盘或云存储中，这里以保存到本地的'static/uploads/'目录为例
        p_file_path = os.path.join(os.path.join(settings.BASE_DIR, 'prifile'), pfile.name)
        s_file_path = os.path.join(os.path.join(settings.BASE_DIR, 'prifile'), sfile.name)
        with open(p_file_path, 'wb') as pdestination1:
            with open(PRE_DIR, 'wb') as pdestination2:
                for chunk in pfile.chunks():
                    pdestination1.write(chunk)
                    pdestination2.write(chunk)
        with open(s_file_path, 'wb') as sdestination1:
            with open(SOU_DIR, 'wb') as sdestination2:
                for chunk in sfile.chunks():
                    sdestination1.write(chunk)
                    sdestination2.write(chunk)

        mylib = ctypes.cdll.LoadLibrary(OPERATION)
        mylib.main()
        out_path = OUT_DESTINATION
        out_filename = "predicted_" + sfile.name.split('.')[0]
        merge.merge_csv_columns(p_file_path, OUT_SOURCE, OUT_DESTINATION, out_filename)
        # shutil.copy2(OUT_SOURCE,out_path)
        # os.rename(os.path.join(OUT_DESTINATION,'out.txt'),os.path.join(OUT_DESTINATION,'predicted_'+sfile.name))
        # 创建对象并保存到数据库
        out_filename = out_filename + '.csv'
        try:
            project = models.Project.objects.get(projectId=project_id)
            models.PrimaryData.objects.create(projectId=project, dataName=data_name, pfilename=pfile.name,
                                              sfilename=sfile.name,
                                              filepath=p_file_path)
            models.PredictedData.objects.create(projectId=project, dataName=data_name, filename=out_filename,
                                                filepath=out_path)
            models.Operation.objects.create(OperationTime=current_date,Operationdata=data_name,DorAorC='add')
            return render(request, "upload_file.html", {"error_message": "上传成功！预测文件已生成！"})
        except:
            return render(request, "upload_file.html",
                          {"project": models.Project.objects.all(),
                           "error_message": "添加格式出错，请检查格式"})


def create_project(request):
    if not request.session.get('mainpage'):
        return HttpResponseForbidden('Access Forbidden')
    if request.method == 'GET':
        users = models.Users.objects.all()
        return render(request, "createproject.html", {"users": users})
    if request.method == 'POST':
        project_id = request.POST.get('project_id')
        project_name = request.POST.get('project_name')
        ctime = request.POST.get('ctime')
        id_incharge = request.POST.get('id_incharge')
        current_date = date.today()
        # 创建Project对象并保存到数据库
        try:
            models.Project.objects.create(projectId=project_id, projectName=project_name, ctime=ctime,
                                          Idincharge_id=id_incharge)
            models.Operation.objects.create(OperationTime=current_date,Operationdata=project_name,DorAorC='add')
            return render(request, "createproject.html", {"error_message": "创建成功！"})
        except:
            return render(request, "createproject.html",
                          {"users": models.Users.objects.all(), "error_message": "添加格式出错，请检查格式"})
        # html = "<div><h1>创建成功！</h1><div><a href='/mainpage/'>回到主页</a></div></div>"

        # return redirect('/mainpage/')  # 重定向到主页面


def data(request):
    if not request.session.get('mainpage'):
        return HttpResponseForbidden('Access Forbidden')
    if request.method == 'GET':
        predata = models.PredictedData.objects.all()
        return render(request, "data.html", {"predict": predata})


def filedrop(request):
    nid1 = request.GET.get('nid1')
    nid2 = request.GET.get('nid2')
    nid3 = request.GET.get('nid3')
    current_date = date.today()
    os.remove(os.path.join(nid1, nid2))
    models.PredictedData.objects.filter(filename=nid2).delete()
    models.PrimaryData.objects.filter(dataName=nid3).delete()
    models.Operation.objects.create(OperationTime=current_date,Operationdata=nid3,DorAorC='delete')
    predata = models.PredictedData.objects.all()
    return render(request, "data.html", {"Notice": "删除成功！","predict": predata})


def mainpage(request):
    return render(request, "mainpage.html")


def img(request):
    nid1 = request.GET.get('nid1')
    nid2 = request.GET.get('nid2')
    path = os.path.join(nid1, nid2)
    out_path = os.path.join(settings.BASE_DIR, 'img')
    filename = nid2
    filename = filename.split('.')[0]
    imgpath = os.path.join(IMG_DIR,filename+'.png')
    Visualize(path, out_path, filename)
    txtname = models.PredictedData.objects.get(filename=nid2)
    models.Image.objects.create(imgname=filename+'.png',imgpath=imgpath,txtname=txtname)
    predata = models.PredictedData.objects.all()
    return render(request, "data.html", {"Notice": "生成成功！", "predict": predata})

def logout(request):
    request.session.pop('mainpage', None)
    html = "<div><h1>成功退出！</h1><div><a href='/'>重新登录</a></div></div>"
    return HttpResponse(html)