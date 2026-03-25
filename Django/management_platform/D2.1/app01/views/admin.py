from django.shortcuts import render, redirect
from django.core.exceptions import ValidationError

from django import forms
from app01.utils.bootstrap import BootStrapModelForm
from app01.utils.encrypt import md5


# 导入app01应用下的数据库模型（Department和UserInfo）
from app01 import models

"""管理员列表"""


def admin_list(request):

    data_dict = {}
    value = request.GET.get("q")
    if value:
        data_dict["username__contains"] = value

    # 1. 获取所有符合条件的数据（用于计算总条数/总页数）
    queryset_all = models.Admin.objects.filter(**data_dict).order_by("id")
    total_count = queryset_all.count()  # 总数据条数

    # 2. 分页核心配置
    per_page = 10  # 每页显示10条，可调整
    total_pages = (total_count + per_page - 1) // per_page  # 计算总页数（向上取整）

    # 3. 处理页码（防止页码越界）
    page = int(request.GET.get("page", 1))
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
                page_list = [1, 2, 3, 4, 5, "...", total_pages]
            # 当前页在最后三页：显示 首页 + 省略号 + 最后5页
            elif page >= total_pages - 2:
                page_list = [1, "..."] + list(range(total_pages - 4, total_pages + 1))
            # 中间页：显示 首页 + 省略号 + 当前页前后2页 + 省略号 + 尾页
            else:
                page_list = (
                    [1, "..."] + list(range(page - 2, page + 3)) + ["...", total_pages]
                )

    # 6. 传递分页相关数据给前端
    context = {
        "queryset": queryset,
        "current_page": page,  # 当前页码
        "total_pages": total_pages,  # 总页数
        "total_count": total_count,  # 总数据条数
        "q": value,  # 保留搜索关键词
        "page_list": page_list,  # 折叠后的页码列表（含省略号）
    }
    return render(request, "admin_list.html", context)


class AdminModelForm(BootStrapModelForm):
    # 额外字段：确认密码（不在模型中）
    confirm_password = forms.CharField(label="确认密码", widget=forms.PasswordInput)

    class Meta:
        model = models.Admin  # 关联的模型
        fields = ["username", "password", "confirm_password"]  # 表单包含的字段
        widgets = {
            "password": forms.PasswordInput(render_value=True)
        }  # 密码字段使用密码输入框

    def clean_username(self):
        # 1. 获取清洗后的用户名（cleaned_data里的是已过基础验证的有效值）
        username = self.cleaned_data.get("username")

        # 2. 用exists()判断是否存在，比first()更高效（只查是否存在，不查具体数据）
        if models.Admin.objects.filter(username=username).exists():
            raise ValidationError("用户名已存在")

        # 3. 验证通过，返回清洗后的字段值（必须return）
        return username

    def clean_password(self):
        pwd = self.cleaned_data.get("password")
        # if not pwd:
        #     raise ValidationError('请输入密码')
        return md5(pwd)

    # 自定义验证方法
    def clean_confirm_password(self):
        pwd = self.cleaned_data.get("password")  # 从已验证数据中获取密码
        confirm = md5(self.cleaned_data.get("confirm_password"))  # 获取确认密码

        if confirm != pwd:  # 比较两者是否一致
            raise ValidationError("密码不一致")

        return confirm  # 验证通过，返回确认密码


class AdminEditModelForm(BootStrapModelForm):
    class Meta:
        model = models.Admin
        fields = ["username"]


class AdminResetModelForm(AdminModelForm):
    class Meta(AdminModelForm.Meta):
        fields = ["password"]  # 表单包含的字段
        widgets = {
            'password':forms.PasswordInput(render_value=False)
        }

    def clean_password(self):
        pwd = self.cleaned_data.get("password")

        md5_pwd = md5(pwd)
        exists = models.Admin.objects.filter(
            id=self.instance.pk, password=md5_pwd
        ).exists()
        if exists:
            raise ValidationError("密码与上一次的一致")

        return md5(pwd)


"""添加管理员"""

#初始代码
# def admin_add(request):
#     title = "新建管理员"
#     if request.method == "GET":
#         form = AdminModelForm()
#         return render(request, "change.html", {"form": form, "title": title})

#     form = AdminModelForm(data=request.POST)
#     if form.is_valid():
#         form.save()
#         return redirect("/admin/list/")

#     return render(request, "change.html", {"form": form, "title": title})

#优化版本
def admin_add(request):
    title = "新建管理员"
    form = AdminModelForm()  # 先初始化空表单（覆盖GET场景）

    if request.method == "POST":
        # 仅POST请求时，重新赋值为带提交数据的表单
        form = AdminModelForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect("/admin/list/")

    # 无论GET请求，还是POST校验失败，都走这一行render
    return render(request, "change.html", {"form": form, "title": title})


"""编辑管理员"""


def admin_edit(request, nid):

    row_object = models.Admin.objects.filter(id=nid).first()
    # 数据不存在
    if not row_object:
        return render(request, "error.html", {"msg": "数据不存在"})
    # 或者直接跳转到本页面
    # return redirect("/admin/list/")

    if request.method == "GET":
        # 只能修改一样数据，以修改名字为例
        form = AdminEditModelForm(instance=row_object)  # 默认值

        title = "编辑管理员"
        return render(request, "change.html", {"title": title, "form": form})

    form = AdminEditModelForm(data=request.POST, instance=row_object)
    # is_valid()会检查：字段是否为空、长度是否超限、格式是否正确等
    if form.is_valid():
        # 验证通过，保存修改到数据库
        # 因为有instance参数，这里执行的是UPDATE更新操作，而不是INSERT插入
        form.save()
        return redirect("/admin/list/")
    return render(request, "change.html", {"title": title, "form": form})


"""删除管理员"""


def admin_delete(request, nid):
    models.Admin.objects.filter(id=nid).delete()
    return redirect("/admin/list/")


"""重置密码"""


def admin_reset(request, nid):
    row_object = models.Admin.objects.filter(id=nid).first()
    if not row_object:
        return redirect("/admin/list/")

    title = "重置密码-{}".format(row_object.username)

    if request.method == "GET":
        form = AdminResetModelForm(instance =row_object)
        return render(request, "change.html", {"form": form, "title": title})

    form = AdminResetModelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        return redirect("/admin/list/")
    return render(request, "change.html", {"form": form, "title": title})
