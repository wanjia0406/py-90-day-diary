# 001 数字组合
# 描述
# 把 1,2,3,4 四个数字组成互不相同且无重复的三位数，输出所有结果并统计个数。

count = 0
for i in range(1,5):
    for j in range(1,5):
        for k in range(1,5):
            if i!=k and i!= j and k!=j:
                count+=1
                print(i*100+j*10+k,end=" ")
print()
print("count = ",count)