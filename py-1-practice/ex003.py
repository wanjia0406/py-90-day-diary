# 描述
# 输出 1 ~ 9999 中所有“个位是 2 且是完全平方数”的整数；每行 5 个，空格分隔，最后输出总个数。
# 最小提示
# 完全平方数 ⇒ 存在整数 i 使得 n = i*i。
# 个位为 2 ⇒ str(n)[-1] == '2' 或 n % 10 == 2。
# 上限：√9999 ≈ 99.99 ⇒ 循环 i 到 100 即可。

count = 0
for i in range(1,101):
    n = i*i
    if n %10==1:
        count+=1
        print(f"{n:5}",end=" " if count%5 else "\n" )
print("count:",count)
