# 006 九九乘法表（默写重点题）
# 描述
# 输出标准 9×9 乘法口诀表，格式：

for i in range(1,10):
    for j in range(1,i+1):
        print(f"{j}*{i}={i*j}",end="\t")
    print()