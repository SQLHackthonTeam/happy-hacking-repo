from math import sqrt
from Parser import CounterGroup
import os
from Parser import Counter

def multiply(a,b):
    #a,b两个列表的数据一一对应相乘之后求和
    sum_ab=0.0
    for i in range(len(a)):
        temp=a[i]*b[i]
        sum_ab+=temp
    return sum_ab

def cal_pearson(x,y):
    n=len(x)
    #求x_list、y_list元素之和
    sum_x=sum(x)
    sum_y=sum(y)
    #求x_list、y_list元素乘积之和
    sum_xy=multiply(x,y)
    #求x_list、y_list的平方和
    sum_x2 = sum([pow(i,2) for i in x])
    sum_y2 = sum([pow(j,2) for j in y])
    molecular=sum_xy-(float(sum_x)*float(sum_y)/n)
    #计算Pearson相关系数，molecular为分子，denominator为分母
    denominator=sqrt((sum_x2-float(sum_x**2)/n)*(sum_y2-float(sum_y**2)/n))
    if denominator == molecular:
        return 1
    elif denominator == 0:
        return 0
    else:
        return molecular/denominator


print(os.path.abspath('.'))
f=open('D:\\test.csv','r')
counters=[]
numj=0
lines=f.readlines()
items = []
for line in lines:
   #strip用于去掉换行符,split()通过指定分隔符对字符串进行切片,返回子字符串
   
    if numj == 0:
         cols=line.strip('\n').split('\",')
         timezone = ((str(cols[0])).split(') ('))[1]
         i=1
         while(i < len(cols)):
            params= (str(cols[i])).split('\\')
            #解析第一行,初始化counter数据,start time and end time is not needed
            #group counter instance computer
            counters.append(Counter(timezone,params[2],"", params[3],params[4]))
            i= i+1
    else:
        cols=line.strip('\n').split(',')
        i = 1
        while( i < len(cols)):
            #添加counter的时间点和值信息
            if cols[i] == '" "' :
                cols[i] = 0
            else:
                cols[i] = float(cols[i].strip('"'))
               
            counters[i-1].stats.append([cols[0],cols[i]])
            i=i+1


    numj = numj+1


xstats=counters[100].stats
ystats=counters[700].stats
x=[]
y=[]

for i in range(len(xstats)):
    x.append(xstats[i][1])

for i in range(len(ystats)):
    y.append(ystats[i][1])

if __name__=='__main__':
    print ("x_list,y_list的Pearson相关系数为："+str(cal_pearson(x,y)))
