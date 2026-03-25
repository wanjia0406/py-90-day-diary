# 导入Django核心快捷函数：
# render：渲染HTML模板并返回给浏览器
# HttpResponse：直接返回字符串/简单数据响应
# redirect：重定向到指定URL（避免重复提交）
from django.shortcuts import render, redirect

from app01.utils.form import UserModelForm,PrettyModelForm

# 导入app01应用下的数据库模型（Department和UserInfo）
from app01 import models




"""部门列表 - 核心功能：查询并展示所有部门数据"""
def depart_list(request):
    # 查询Department模型对应的数据库表中所有数据，返回QuerySet（查询结果集）
    queryset = models.Department.objects.all()
    # 渲染depart_list.html模板，将部门数据传递给前端（前端用{{ queryset }}遍历）
    return render(request, "depart_list.html", {"queryset": queryset})


"""添加部门 - 核心功能：接收表单数据并新增部门"""
def depart_add(request):
    """添加部门"""
    if request.method == "GET":
        return render(request, "depart_add.html")

    # POST请求处理
    title = request.POST.get("title", "").strip()
    
    # 后端再次验证（双重保险）
    if not title:
        # 这里可以添加弹窗，但主要靠前端
        return render(request, "depart_add.html")
    
    # 保存数据
    models.Department.objects.create(title=title)
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

