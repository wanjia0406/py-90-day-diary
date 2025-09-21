# 004 三数排序
# 描述
# 输入三个整数 x, y, z，请由小到大输出，数与数之间空一格。
# 要求：
# 不允许用 sorted() 或 sort()。
# 必须手写三数比较逻辑。

x = int(input())
y = int(input())
z = int(input())

a = min(x,y,z)
c = max(x,y,z)
b = x+y+z-a-c
print(a,b,c)

