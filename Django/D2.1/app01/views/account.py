from django.shortcuts import render,redirect,HttpResponse
from django.core.exceptions import ValidationError
from django import forms
from app01 import models

from app01.utils.bootstrap import BootStrapForm,BootStrapModelForm
from app01.utils.encrypt import md5

class LoginForm(BootStrapForm):
    username = forms.CharField(label="用户名",widget=forms.TextInput)
    password = forms.CharField(label="密码",widget=forms.PasswordInput)
    
    def clean_password(self):
        pwd = self.cleaned_data.get('password')
        return md5(pwd)

class LoginModelForm(BootStrapModelForm):
    class Meta:
        model = models.Admin
        fields = ['username','password']

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
        """自定义用户名验证：检查用户名是否已存在"""
        username = self.cleaned_data.get("username")
        # 检查数据库中是否已有该用户名的管理员
        exists = models.Admin.objects.filter(username=username).exists()
        if exists:
            raise ValidationError("该账户已注册")
        return username

    def clean_password(self):
        pwd = self.cleaned_data.get("password")
        return md5(pwd)

    # 自定义验证方法
    def clean_confirm_password(self):
        pwd = self.cleaned_data.get("password")  # 从已验证数据中获取密码
        confirm = md5(self.cleaned_data.get("confirm_password"))  # 获取确认密码

        if confirm != pwd:  # 比较两者是否一致
            raise ValidationError("密码不一致")

        return confirm  # 验证通过，返回确认密码

class AdminResetModelForm(AdminModelForm):
    class Meta(AdminModelForm.Meta):
        fields = ["password", "confirm_password"]  # 表单包含的字段

    def clean_password(self):
        pwd = self.cleaned_data.get("password")

        md5_pwd = md5(pwd)
        exists = models.Admin.objects.filter(id =self.instance.pk,password = md5_pwd).exists()
        if exists:
            raise ValidationError("密码与上一次的一致")

        return md5(pwd)
    

class ResetPwdRequestForm(BootStrapForm):
    username = forms.CharField(label="用户名", widget=forms.TextInput)

    def clean_username(self):
        """验证用户名是否存在"""
        username = self.cleaned_data.get("username")
        admin_obj = models.Admin.objects.filter(username=username).first()
        if not admin_obj:
            raise ValidationError("该用户名不存在，请检查后重新输入")
        return username


class ResetPwdForm(BootStrapForm):
    password = forms.CharField(label="新密码", widget=forms.PasswordInput(render_value=True))
    confirm_password = forms.CharField(label="确认新密码", widget=forms.PasswordInput)

    def clean_confirm_password(self):
        """验证两次密码一致"""
        pwd = self.cleaned_data.get("password")
        confirm = self.cleaned_data.get("confirm_password")
        if md5(pwd) != md5(confirm):
            raise ValidationError("两次密码不一致")
        # 验证通过返回加密后的密码，方便后续保存
        return md5(pwd)


"""登录"""
def login(request):
    if request.method =="GET":
        form = LoginForm()
        return render(request,'login.html',{"form":form})
    
    form = LoginForm(data=request.POST)
    if form.is_valid():
        ##校验密码
        admin_object = models.Admin.objects.filter(**form.cleaned_data).first()
        if not admin_object:
            form.add_error("password","用户名或密码错误")
            return render(request,'login.html',{"form":form})
        
        request.session["info"] = {"id":admin_object.id,'name':admin_object.username}  #用户名
        request.session.set_expiry(60 * 30)  # 可选：设置session过期时间（30分钟）
        return redirect('/admin/list/')
    return render(request,'login.html',{"form":form})
    
"""注销"""
def logout(request):
    request.session.clear()
    return redirect('/login/')

"""注册"""
def register(request):

    if request.method == "GET":
        form = AdminModelForm()
        return render(request, "register.html", {"form": form})

    form = AdminModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        # 注意：原代码是 /login/list/，大概率是笔误，应改为 /admin/list/
        return redirect("/admin/list/")

    return render(request, "register.html", {"form": form})


"""忘记密码"""
def reset_pwd_request(request):
    """第一步：输入用户名，验证存在后跳转到重置页"""
    if request.method == "GET":
        form = ResetPwdRequestForm()
        return render(request, 'reset_pwd_request.html', {"form": form})
    
    form = ResetPwdRequestForm(data=request.POST)
    if form.is_valid():
        # 验证通过，获取用户名并跳转到第二步
        username = form.cleaned_data.get("username")
        return redirect(f'/login/{username}/reset/')
    
    # 验证失败，返回页面显示错误
    return render(request, 'reset_pwd_request.html', {"form": form})

def reset_pwd(request, name):
    """第二步：带用户名参数，重置密码"""
    # 二次校验：防止直接拼接URL访问
    admin_obj = models.Admin.objects.filter(username=name).first()
    if not admin_obj:
        return HttpResponse("用户名不存在，无法重置密码")
    
    title = f"重置 {name} 的密码"
    if request.method == "GET":
        form = ResetPwdForm()
        return render(request, 'reset_pwd.html', {"form": form, "title": title})
    
    # 提交新密码，验证并保存
    form = ResetPwdForm(data=request.POST)
    if form.is_valid():
        # 获取加密后的新密码
        new_pwd = form.cleaned_data.get("confirm_password")
        # 更新密码
        models.Admin.objects.filter(username=name).update(password=new_pwd)
        # 重置成功，跳回登录页
        return redirect('/login/')
    
    # 验证失败，返回页面显示错误
    return render(request, 'reset_pwd.html', {"form": form, "title": title})