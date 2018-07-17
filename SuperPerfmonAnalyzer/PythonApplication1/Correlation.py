from math import sqrt
from myClass import Counter
from myClass import CounterGroup
from myClass import PerfMon
import re
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import heapq
import tushare as ts
import datetime

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
    print(molecular)
    print(denominator)
    if denominator == 0:
        return 0
    elif denominator == molecular:
        return 1
    else:
        return molecular/denominator


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
            SearchObj = re.search( r'\((.*)\)', str(params[3]), re.M|re.I)
            instance = ""
            if SearchObj is not None:
                instance = SearchObj.group(1)
           
            group =  str(params[3]).strip("\("+instance+"\)")

            print(group)
            counters.append(Counter(timezone,params[2], instance,group,params[4]))
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


##simple test
def calculate(xindex, yindex):
    xstats=counters[xindex].stats
    ystats=counters[yindex].stats
    x=[]
    y=[]

    for i in range(len(xstats)):
        x.append(xstats[i][1])

    for i in range(len(ystats)):
        y.append(ystats[i][1])

    if __name__=='__main__':
        pearson = cal_pearson(x,y)
        print ("x_list,y_list的Pearson相关系数为："+str(pearson))

    return pearson

def FindCorrelation(InputCounter):
    index = counters.index(Counter(InputCounter).getCounterName)
    relation = []
    for i in range(len(counters)):
        if i!=index:
            relation.append((counters[i], calculate(i, index)))
    relation.sort()

#compare peak time            
def PeakMatch(xindex, yindex):
    xstats=counters[xindex].stats
    ystats=counters[yindex].stats
    wave_guess(xstats)
    wave_guess(ystats)


    for i in range(len(xstats)):
        x.append(xstats[i][1])

    for i in range(len(ystats)):
        y.append(ystats[i][1])


def wave_guess(arr):
    wn = int(len(arr)/4) #没有经验数据，先设置成1/4。
    print(wn)
    #计算最小的N个值，也就是认为是波谷
    wave_crest = heapq.nlargest(wn, enumerate(arr), key=lambda x: x[1])
    wave_crest_mean = pd.DataFrame(wave_crest).mean()

    #计算最大的5个值，也认为是波峰
    wave_base = heapq.nsmallest(wn, enumerate(arr), key=lambda x: x[1])
    wave_base_mean = pd.DataFrame(wave_base).mean()

    print("######### result #########")
    #波峰，波谷的平均值的差，是波动周期，对于股票就是天。
    wave_period = abs(int( wave_crest_mean[0] - wave_base_mean[0]))
    print("wave_period_day:", wave_period)
    print("wave_crest_mean:", round(wave_crest_mean[1],2))
    print("wave_base_mean:", round(wave_base_mean[1],2))

    wavelist = wave_crest_mean.append(wave_base_mean)
    return wavelist