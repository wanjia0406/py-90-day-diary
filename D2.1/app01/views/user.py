# 导入Django核心快捷函数：
# render：渲染HTML模板并返回给浏览器
# HttpResponse：直接返回字符串/简单数据响应
# redirect：重定向到指定URL（避免重复提交）
from django.shortcuts import render, HttpResponse, redirect

from app01.utils.form import UserModelForm

# 导入app01应用下的数据库模型（Department和UserInfo）
from app01 import models


"""用户列表 - 核心功能：查询并展示所有用户数据"""


def user_list(request):
    # 查询UserInfo模型对应的数据库表中所有数据
    queryset = models.UserInfo.objects.all()
    # 渲染user_list.html模板，将用户数据传递给前端
    return render(request, "user_list.html", {"queryset": queryset})


"""添加用户（原生方式） - 核心功能：手动接收表单数据并新增用户"""


def user_add(request):
    # GET请求：返回添加用户表单，并传递下拉框所需数据
    if request.method == "GET":
        # 组装前端需要的数据：
        # gender_choices：UserInfo模型中定义的性别选项（如(1,'男'),(2,'女')）
        # depart_list：所有部门数据（用于所属部门下拉框）
        context = {
            "gender_choices": models.UserInfo.gender_choices,
            "depart_list": models.Department.objects.all(),
        }
        # 渲染添加用户表单，传递下拉框数据
        return render(request, "user_add.html", context)

    # POST请求：接收前端提交的所有用户数据
    user = request.POST.get("user")  # 用户名（表单name="user"）
    pwd = request.POST.get("pwd")  # 密码（表单name="pwd"）
    age = request.POST.get("age")  # 年龄（表单name="age"）
    account = request.POST.get(
        "salary"
    )  # 薪资（表单name="salary"，对应模型account字段）
    time = request.POST.get("time")  # 创建时间（表单name="time"）
    gender = request.POST.get("gender")  # 性别（表单name="gender"）
    depart = request.POST.get("depart")  # 所属部门ID（表单name="depart"）

    # 向数据库插入新的用户记录
    models.UserInfo.objects.create(
        name=user,  # 模型name字段 ← 前端user字段
        password=pwd,
        age=age,
        account=account,  # 模型account字段 ← 前端salary字段
        create_time=time,
        gender=gender,
        depart_id=depart,  # 外键关联：通过depart_id直接赋值部门ID
    )

    # 新增完成后重定向回用户列表页
    return redirect("/user/list/")


# 2. 视图函数：处理ModelForm添加用户的请求（仅展示空表单）
def user_model_form_add(request):
    if request.method == "GET":
        # 初始化空的ModelForm表单（无初始数据）
        form = UserModelForm()
        # 将表单对象传递给模板，供前端渲染
        return render(request, "user_model_form_add.html", {"form": form})

    # 用户提交数据
    form = UserModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect("/user/list/")

    # 校验失败
    return render(request, "user_model_form_add.html", {"form": form})


"""编辑用户"""


def user_edit(request, nid):
    # 步骤1：根据nid查询要编辑的用户数据（提前查询，GET/POST请求都能用）
    row = models.UserInfo.objects.filter(id=nid).first()

    # 步骤2：处理GET请求（用户访问编辑页面，展示回显后的表单）
    if request.method == "GET":
        # 核心：instance=row 让表单加载已有数据（实现数据回显）
        form = UserModelForm(instance=row)
        # 传递带回显数据的表单给模板，前端渲染后能看到用户原有信息
        return render(request, "user_edit.html", {"form": form})

    # 步骤3：处理POST请求（用户提交修改后的表单）
    # 核心：data=request.POST 接收提交的新数据，instance=row 指定要更新的对象
    form = UserModelForm(data=request.POST, instance=row)

    # 步骤4：表单数据验证
    if form.is_valid():
        # 验证通过：保存修改（因为传了instance，会更新而非新增数据）
        form.save()
        # 重定向回用户列表页，避免刷新重复提交
        return redirect("/user/list/")

    # 步骤5：验证失败：返回表单页面，保留错误信息和用户输入的内容
    return render(request, "user_edit.html", {"form": form})


def user_delete(request, nid):
    models.UserInfo.objects.filter(id=nid).delete()
    return redirect("/user/list/")
