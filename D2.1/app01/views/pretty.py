# 导入Django核心快捷函数：
# render：渲染HTML模板并返回给浏览器
# HttpResponse：直接返回字符串/简单数据响应
# redirect：重定向到指定URL（避免重复提交）
from django.shortcuts import render, HttpResponse, redirect

from app01.utils.form import UserModelForm,PrettyModelForm

# 导入app01应用下的数据库模型（Department和UserInfo）
from app01 import models




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

