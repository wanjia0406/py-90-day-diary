# 007 暂停一秒输出
# 描述
# 给定一个列表（或任意长度），每输出一个元素后暂停 1 秒，再输出下一个；
# 要求：
# 必须用到标准库 time.sleep(1)；
# 禁止一次性 print 整个列表；
# 元素间无多余空格，每元素独占一行。

import time
list = [1,2,3,4,5,6,7,8]
for item in list:
    print(item)
    time.sleep(1)
