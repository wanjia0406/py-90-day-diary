# 009 兔子数列（递归版）★官方第9题 + 后期默写重点
# 描述
# 经典斐波那契变形：
# 第 1 个月 1 对兔子；
# 第 2 个月仍 1 对；
# 从第 3 个月开始，每个月生 1 对新兔子（即 F(n)=F(n-1)+F(n-2) ）。
# 输入一个整数 n（1≤n≤30），用递归函数输出第 n 个月的兔子对数。

def fibonacci(n):
    # 递归基线条件
    if n == 1 or n == 2:
        return 1
    # 递归关系：F(n) = F(n-1) + F(n-2)
    else:
        return fibonacci(n - 1) + fibonacci(n - 2)

# 输入月份
n = int(input())
# 输出结果
print(fibonacci(n))