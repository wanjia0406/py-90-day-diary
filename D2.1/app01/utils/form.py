

# 导入Django表单模块，用于定义ModelForm
from django import forms

# 导入app01应用下的数据库模型（Department和UserInfo）
from app01 import models
from app01.utils.bootstrap import BootStrapModelForm

"""添加用户（ModelForm版本） - 核心功能：基于模型自动生成表单（仅展示）"""
# 1. 定义ModelForm类（推荐放在forms.py，此处临时放在views.py）
class UserModelForm(BootStrapModelForm):
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

"""增加靓号"""
class PrettyModelForm(BootStrapModelForm):
    class Meta:
        model = models.PrettyNum
        # fields = "__all__"
        fields = ["mobile", "price", "level", "status"]


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
