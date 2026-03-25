from django.shortcuts import render,HttpResponse,redirect
# Create your views here.

def index(request):
    return HttpResponse("华宁")


# from app01.models import UserInfo
# from app01 import models

def login(request):
    
    # models.UserInfo.objects.create(name = '程亿豪',password = '0503',age = 19)
    # models.UserInfo.objects.create(name = '张嘉怡',password = '0426',age = 19)
    
    ###删除
    # models.UserInfo.objects.filter(id__gt=20).delete()
    #models.UserInfo.objects.all().delect()

    ###获取数据
    # data_list = [行，行，行]

    ##查询所有信息
    # data_list = models.UserInfo.objects.all()
    # for o in data_list:
    #     print(o.id,o.name,o.password,o.age)

    ##条件查询
    # data = models.UserInfo.objects.filter(id = 2).first()
    # print(data.id,data.name,data.password,data.age)

    ###更新数据
    # models.UserInfo.objects.all().update(password=999)
    # models.UserInfo.objects.filter(id = 2).update(password=999)

     return HttpResponse("成功")




from app01.models import UserInfo


def love(request):
    #获取数据
    data_list = UserInfo.objects.all()

    return render(request,'love.html',{"data_list":data_list})

def info_add(request):
    if request.method == "GET":
        return render(request,'info_add.html')
    #获取用户提交的数据
    user = request.POST.get("user")
    pwd = request.POST.get("pwd")
    age = request.POST.get("age")

    #添加到数据库
    UserInfo.objects.create(name = user,password = pwd,age =age)
    # return HttpResponse("添加成功")

    #自动跳转
    return redirect("/info/list/")

def info_delete(request):
    nid = request.GET.get('nid')
    UserInfo.objects.filter(id = nid).delete()
    return redirect("/info/list/")




