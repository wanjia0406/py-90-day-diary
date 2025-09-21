# 008 当前时间格式化输出
# 描述
# 获取当前系统时间，并按下面两种格式各打印一行：
# 2025-06-25 14:30:25
# 06/25/2025 02:30:25 PM（12 小时制，带 AM/PM）
# 要求
# 必须用标准库 datetime；
# 不准手动拼字符串，全用格式化指令；
# 两行顺序不能反。

from datetime import datetime
#获取当前的时间
now = datetime.now()

format1 = now.strftime("%Y-%m-%d %H:%M:%S")
print(format1)

format2 = now.strftime("%m/%d/%Y %I:%M:%S %p")
print(format2)