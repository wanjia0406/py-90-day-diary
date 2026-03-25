from django.shortcuts import render, redirect
from django.core.exceptions import ValidationError
from app01.utils.encrypt import md5

from app01 import models
from django import forms

from app01.utils.bootstrap import BootStrapModelForm


def admin01_list(request):
    # 搜索功能
    dict = {}
    value = request.GET.get("q")
    if value:
        dict["username__contains"] = value

    # queryset = models.Admin.objects.all()
    queryset = models.Admin.objects.filter(**dict).order_by("id")
    return render(request, "admin01_list.html", {"q": value, "queryset": queryset})


# 新增管理员forms文件
class AdminModelForm(BootStrapModelForm):
    confirm_password = forms.CharField(
        label="确认密码", widget=forms.PasswordInput(render_value=True)
    )

    class Meta:
        model = models.Admin
        fields = ["username", "password", "confirm_password"]
        widgets = {"password": forms.PasswordInput(render_value=True)}

    # 验证
    # 用户名
    def clean_username(self):
        username = self.cleaned_data.get("username")
        if models.Admin.objects.filter(username=username).exists():
            raise ValidationError("用户名已存在")
        return username

    # 密码
    def clean_password(self):
        password = self.cleaned_data.get("password")
        return md5(password)

    # 验证密码
    def clean_confirm_password(self):
        password = self.cleaned_data.get("password")
        confirm = md5(self.cleaned_data.get("confirm_password"))
        if password != confirm:
            raise ValidationError("密码不一致")
        return confirm


# 新增管理员
def admin01_add(request):

    title = "新增管理员"
    form = AdminModelForm()

    if request.method == "POST":
        form = AdminModelForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect("/admin/list/")

    return render(request, "change.html", {"form": form, "title": title})


"""修改"""


class AdminEditModelForm(BootStrapModelForm):
    class Meta:
        model = models.Admin
        fields = ["username"]


def admin01_edit(request, nid):
    row = models.Admin.objects.filter(id=nid).first()
    if not row:
        return render(request, "error.html", {"msg": "数据不存在"})

    if request.method == "GET":
        title = "编辑管理员"
        form = AdminEditModelForm(instance=row)
        return render(request, "change01.html", {"form": form, "title": title})

    form = AdminEditModelForm(data=request.POST, instance=row)
    if form.is_valid():
        form.save()
        return redirect("/admin01/list/")
    return render(request, "change01.html", {"form": form, "title": title})


"""删除"""


def admin01_delete(request, nid):
    models.Admin.objects.filter(id=nid).delete()
    return redirect("/admin01/list/")


"""重置密码"""


class Admin01ResetModelForm(BootStrapModelForm):
    confirm_password = forms.CharField(label="确认密码1", widget=forms.PasswordInput)

    class Meta:
        model = models.Admin
        fields = ["password"]
        widgets = {"password": forms.PasswordInput(render_value=False)}

    def clean_password(self):
        pwd = self.cleaned_data.get("password")
        # 补充：校验密码非空（避免用户空提交导致md5报错）
        if not pwd:
            raise ValidationError("新密码不能为空")
        md5_pwd = md5(pwd)
        # 修复：只对比当前用户的原密码（self.instance是当前管理员对象）
        if self.instance.password == md5_pwd:
            raise ValidationError("密码与上次一致")
        return md5_pwd

    def clean_confirm_password(self):
        pwd = self.cleaned_data.get("password")
        confirm = md5(self.cleaned_data.get("confirm_password"))
        if pwd != confirm:
            raise ValidationError("密码不一致")
        return confirm


def admin01_reset(request, nid):
    row_object = models.Admin.objects.filter(id=nid).first()
    if not row_object:
        return redirect("/admin/list/")

    title = "重置密码-{}".format(row_object.username)

    if request.method == "GET":
        form = Admin01ResetModelForm(instance=row_object)
        return render(request, "change.html", {"form": form, "title": title})

    form = Admin01ResetModelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        return redirect("/admin01/list/")
    return render(request, "change.html", {"form": form, "title": title})
