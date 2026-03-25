# 导入Django核心快捷函数：
# render：渲染HTML模板并返回给浏览器
# HttpResponse：直接返回字符串/简单数据响应
# redirect：重定向到指定URL（避免重复提交）
from django.shortcuts import render, HttpResponse, redirect

# 导入app01应用下的数据库模型（Department和UserInfo）
from app01 import models

# Create your views here.  # Django自动生成的注释，标识视图函数存放位置

# 以下是测试用的视图函数（已注释），仅演示最基础的HttpResponse用法
# def index(request):
#     return HttpResponse('shdfis')

"""部门列表 - 核心功能：查询并展示所有部门数据"""


def depart_list(request):
    # 查询Department模型对应的数据库表中所有数据，返回QuerySet（查询结果集）
    queryset = models.Department.objects.all()
    # 渲染depart_list.html模板，将部门数据传递给前端（前端用{{ queryset }}遍历）
    return render(request, "depart_list.html", {"queryset": queryset})


"""添加部门 - 核心功能：接收表单数据并新增部门"""


def depart_add(request):
    # 区分请求方法：GET请求（用户访问添加页面）返回空表单
    if request.method == "GET":
        return render(request, "depart_add.html")

    # POST请求：用户提交表单，处理数据保存
    # 从POST请求中获取前端表单name="title"的字段值（部门名称）
    title = request.POST.get("title")
    # 向数据库中插入新的部门记录
    models.Department.objects.create(title=title)
    # 新增完成后重定向回部门列表页（注：代码中"会"是笔误，应为"回"）
    return redirect("/depart/list")


"""删除部门 - 核心功能：根据ID删除指定部门"""


def depart_delete(request):
    # 获取前端提交的要删除部门的ID（表单name="nid"）
    nid = request.POST.get("nid")
    # 根据ID筛选部门并执行删除操作
    models.Department.objects.filter(id=nid).delete()
    # 删除完成后重定向回部门列表页
    return redirect("/depart/list")


"""修改部门 - 核心功能：根据ID修改部门名称"""


def depart_edit(request, nid):
    # GET请求：展示修改表单，回显原有部门名称
    if request.method == "GET":
        # 根据URL传递的nid（部门ID）查询单条部门数据（first()取第一条结果）
        row = models.Department.objects.filter(id=nid).first()
        # 将查询到的部门数据传递给模板，供前端回显
        return render(request, "depart_edit.html", {"row_object": row})

    # POST请求：接收修改后的部门名称并更新数据库
    title = request.POST.get("title")
    # 根据ID更新部门名称
    models.Department.objects.filter(id=nid).update(title=title)
    # 修改完成后重定向回部门列表页
    return redirect("/depart/list/")


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


"""添加用户（ModelForm版本） - 核心功能：基于模型自动生成表单（仅展示）"""
# 导入Django表单模块，用于定义ModelForm
from django import forms


# 1. 定义ModelForm类（推荐放在forms.py，此处临时放在views.py）
class UserModelForm(forms.ModelForm):
    # Meta类是ModelForm的核心配置类，用于关联模型和指定字段
    class Meta:
        # 关联到UserInfo模型（Django会自动根据模型生成表单字段）
        model = models.UserInfo
        # 指定表单要包含的字段（需与模型字段名完全一致）
        fields = [
            "name",
            "password",
            "age",
            "account",
            "create_time",
            "gender",
            "depart",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs = {"class": "form-control", "placeholder": field.label}


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


"""靓号管理"""

def pretty_list(request):
    data_dict = {}
    value = request.GET.get("q")
    if value:
        data_dict["mobile__contains"] = value

    # 1. 获取所有符合条件的数据（用于计算总条数/总页数）
    queryset_all = models.PrettyNum.objects.filter(**data_dict).order_by("id")
    total_count = queryset_all.count()  # 总数据条数
    
    # 2. 分页核心配置
    per_page = 10  # 每页显示10条，可调整
    total_pages = (total_count + per_page - 1) // per_page  # 计算总页数（向上取整）
    
    # 3. 处理页码（防止页码越界）
    page = int(request.GET.get('page', 1))
    page = max(1, min(page, total_pages)) if total_pages > 0 else 1
    
    # 4. 截取当前页数据
    start = (page - 1) * per_page
    end = page * per_page
    queryset = queryset_all[start:end]

    # 5. 生成【折叠的页码列表】（核心修改）
    page_list = []
    if total_pages > 0:
        # 规则：
        # - 总页数≤7：显示所有页码（无需折叠）
        # - 总页数>7：显示 首页 + 省略号 + 当前页前后2页 + 省略号 + 尾页
        if total_pages <= 7:
            page_list = list(range(1, total_pages + 1))
        else:
            # 当前页在前三页：显示 1-5 + 省略号 + 尾页
            if page <= 3:
                page_list = [1,2,3,4,5, "...", total_pages]
            # 当前页在最后三页：显示 首页 + 省略号 + 最后5页
            elif page >= total_pages - 2:
                page_list = [1, "..."] + list(range(total_pages - 4, total_pages + 1))
            # 中间页：显示 首页 + 省略号 + 当前页前后2页 + 省略号 + 尾页
            else:
                page_list = [1, "..."] + list(range(page-2, page+3)) + ["...", total_pages]

    # 6. 传递分页相关数据给前端
    context = {
        "queryset": queryset,
        "current_page": page,  # 当前页码
        "total_pages": total_pages,  # 总页数
        "total_count": total_count,  # 总数据条数
        "q": value,  # 保留搜索关键词
        "page_list": page_list  # 折叠后的页码列表（含省略号）
    }
    return render(request, "pretty_list.html", context)


"""增加靓号"""


class PrettyModelForm(forms.ModelForm):
    class Meta:
        model = models.PrettyNum
        # fields = "__all__"
        fields = ["mobile", "price", "level", "status"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs = {"class": "form-control", "placeholder": field.label}

    # 替换后的正确代码（只保留这一个clean_mobile方法）
    def clean_mobile(self):
        txt_mobile = self.cleaned_data["mobile"]

        # 1. 验证手机号长度
        if len(txt_mobile) != 11:
            raise forms.ValidationError("手机号格式错误，必须是11位")

        # 2. 验证唯一性：区分新增/编辑
        # self.instance 存在 → 编辑场景（有主键id）；不存在 → 新增场景
        if self.instance.pk:  # 编辑
            # 排除当前编辑的这条数据，检查其他数据是否有重复
            exists = (
                models.PrettyNum.objects.exclude(id=self.instance.pk)
                .filter(mobile=txt_mobile)
                .exists()
            )
        else:  # 新增
            # 检查所有数据是否有重复
            exists = models.PrettyNum.objects.filter(mobile=txt_mobile).exists()

        if exists:
            raise forms.ValidationError("该手机号已存在")

        # 验证通过，返回手机号
        return txt_mobile


def pretty_add(request):
    if request.method == "GET":
        form = PrettyModelForm()
        return render(request, "pretty_add.html", {"form": form})

    # 提交数据
    form = PrettyModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect("/pretty/list/")

    return render(request, "pretty_add.html", {"form": form})


def pretty_edit(request, nid):
    row = models.PrettyNum.objects.filter(id=nid).first()

    # 步骤2：处理GET请求（用户访问编辑页面，展示回显后的表单）
    if request.method == "GET":
        # 核心：instance=row 让表单加载已有数据（实现数据回显）
        form = PrettyModelForm(instance=row)
        # 传递带回显数据的表单给模板，前端渲染后能看到用户原有信息
        return render(request, "pretty_edit.html", {"form": form})

    # post请求
    form = PrettyModelForm(data=request.POST, instance=row)
    if form.is_valid():
        form.save()
        return redirect("/pretty/list/")
    # 步骤5：验证失败：返回表单页面，保留错误信息和用户输入的内容
    return render(request, "pretty_edit.html", {"form": form})


def pretty_delete(request, nid):
    models.PrettyNum.objects.filter(id=nid).delete()
    return redirect("/pretty/list/")
