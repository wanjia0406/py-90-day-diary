from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import redirect

class AutoMiddleware(MiddlewareMixin):
    """中间体1"""
    def process_request(self,request):
        # 核心逻辑：登录校验
        info_dict = request.session.get("info")  # 从session获取用户登录信息
        
        # 白名单1：直接放行的路径（登录、注册、密码重置请求页）
        if request.path_info in ["/login/", "/register/","/login/reset/request/",]:
            return  # return None 表示放行，继续执行后续中间件/视图
        
        # 如果session中有登录信息，放行
        if info_dict:
            return
        
        # 白名单2：以/login/开头且以/reset/结尾的路径（比如密码重置相关页）
        if request.path_info.startswith('/login/') and request.path_info.endswith('/reset/'):
            return
        
        # 以上条件都不满足：未登录 + 访问非白名单路径 → 重定向到登录页
        return redirect('/login/')

    def process_response(self,request,response): 
        # 响应处理（当前无实际逻辑）
        # print("M1,走了")
        return response

