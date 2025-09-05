result=1
v = 0
for i in range(0,100):
    v=v+1
    result=result*v
print(result)

for i in range(1,101):
    if i%2!=0:
        print(i)

# 计算1*2....*100
# 打印1-100的所有奇数


# 1x1 1x2 1x3 ...1x9
# 2x1 2x2 ...   2x9
#
# 9x1 9x2 .... 9x9

for i in range(1,10):
    for j in range(1,10):
        print(i*j)

