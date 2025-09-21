# 002 个税计算器
# 描述
# 企业发放的奖金根据利润 profit 分段提成：
# 表格
# 复制
# 利润区间（万元）	提成比例
# ≤10	10 %
# 10 ~ 20	超出 10 万部分 7.5 %
# 20 ~ 40	超出 20 万部分 5 %
# 40 ~ 60	超出 40 万部分 3 %
# 60 ~ 100	超出 60 万部分 1.5 %
# ＞100	超出 100 万部分 1 %
# 输入一个整数 profit（单位：元），输出应发放奖金总数（单位：元），保留 2 位小数。
profit = int(input("请输入利润:"))
if profit<=100000:
    bouns = profit*0.1
elif profit<=200000:
    bouns = (profit-100000)*0.075+10000
elif profit<=400000:
    bouns = (profit-200000)*0.05+17500
elif profit <=600000:
    bouns = (profit-400000)*0.03+27500
elif profit <=1000000:
    bouns = (profit-600000)*0.015+33500
else:
    bouns = (profit-1000000)*0.01+39500
print(f"{bouns:.2f}")