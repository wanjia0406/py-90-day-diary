# 004 三数排序
# 描述
# 输入三个整数 x, y, z，请由小到大输出，数与数之间空一格。
# 要求：
# 不允许用 sorted() 或 sort()。
# 必须手写三数比较逻辑。


x, y, z = map(int, input().split())

if x > y: x, y = y, x
if x > z: x, z = z, x
if y > z: y, z = z, y

print(f"{x} {y} {z}")

# def sort_num(a,b,c):
#     if a>b: a ,b = b, a
#     if a>c:a,c = c,a
#     if b>c:b,c = c,b
#     return a,b,c

# x,y,z = map(int,input().split())
# number = sort_num(x,y,z)
# print(f"{number[0]} {number[1]} {number[2]}")


    