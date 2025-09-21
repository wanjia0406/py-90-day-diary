# 001 数字组合
# 描述
# 把 1,2,3,4 四个数字组成互不相同且无重复的三位数，输出所有结果并统计个数。

from itertools import permutations  # 从itertools模块导入permutations函数

nums = [1, 2, 3, 4]  # 定义包含4个数字的列表

# 使用permutations生成所有3个元素的排列
# a, b, c分别接收每个排列中的三个元素
for a, b, c in permutations(nums, 3):
    print(f"{a}{b}{c}", end=" ")  # 打印每个排列（无空格连接）

print("\ncount =", len(list(permutations(nums, 3))))  # 打印排列总数