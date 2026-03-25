from django import forms


class BootStrap:
    # 1. 重写初始化方法（__init__）：表单实例化时自动执行
    def __init__(self, *args, **kwargs):
        # 2. 调用父类的初始化方法：保留原有表单的核心功能
        super().__init__(*args, **kwargs)

        # 3. 遍历表单的所有字段（比如username、password、confirm_password）
        for name, field in self.fields.items():
            # 4. 判断字段是否已有自定义的attrs（属性）
            if field.widget.attrs:
                # 4.1 已有attrs：追加class和placeholder（不覆盖原有属性）
                field.widget.attrs["class"] = "form-control"
                field.widget.attrs["placeholder"] = field.label
            else:
                # 4.2 无attrs：直接设置attrs，包含class和placeholder
                field.widget.attrs = {
                    "class": "form-control",
                    "placeholder": field.label,
                }


class BootStrapModelForm(BootStrap, forms.ModelForm):
    # Meta类是ModelForm的核心配置类，用于关联模型和指定字段
    pass


class BootStrapForm(BootStrap, forms.Form):
    pass
