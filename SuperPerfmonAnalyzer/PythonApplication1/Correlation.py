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

class Core():
    counters = []
    path = ""
    relations = []
    def __init__(self, path):
        self.path = path
        
    def multiply(self,a,b):
        #a,b两个列表的数据一一对应相乘之后求和
        sum_ab=0.0
        for i in range(len(a)):
            temp=a[i]*b[i]
            sum_ab+=temp
        return sum_ab

    def cal_pearson(self,x,y):
        n=len(x)
        #求x_list、y_list元素之和
        sum_x=sum(x)
        sum_y=sum(y)
        #求x_list、y_list元素乘积之和
        sum_xy=self.multiply(x,y)
        #求x_list、y_list的平方和
        sum_x2 = sum([pow(i,2) for i in x])
        sum_y2 = sum([pow(j,2) for j in y])
        molecular=sum_xy-(float(sum_x)*float(sum_y)/n)
        #计算Pearson相关系数，molecular为分子，denominator为分母
        bug = sum_x2-float(sum_x**2)/n
        if bug < 0:
           return 0
        denominator=sqrt((sum_x2-float(sum_x**2)/n)*(sum_y2-float(sum_y**2)/n))
        print(molecular)
        print(denominator)
        if denominator == 0:
            return 0
        elif denominator == molecular:
            return 1
        else:
            return molecular/denominator



    def readCSV(self, path):
        f=open(path,'r')
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
                    self.counters.append(Counter(timezone,params[2], instance,group,params[4]))
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
               
                    self.counters[i-1].stats.append([cols[0],cols[i]])
                    i=i+1


            numj = numj+1
        print(len(self.counters))
        return self.counters

    ##simple test
    def calculate(self, xindex, yindex):
        xstats=(self.counters)[xindex].stats
        ystats=(self.counters)[yindex].stats
        x=[]
        y=[]
        pearson = 0.0
        for i in range(len(xstats)):
            x.append(xstats[i][1])

        for i in range(len(ystats)):
            y.append(ystats[i][1])

        pearson = self.cal_pearson(x,y)
        print ("x_list,y_list的Pearson相关系数为："+str(pearson))

        return pearson

    def FindCorrelation(self, InputCounter):
        params= (str(InputCounter)).split('\\')
            #解析第一行,初始化counter数据,start time and end time is not needed
            #group counter instance computer
        SearchObj = re.search( r'\((.*)\)', str(params[3]), re.M|re.I)
        instance = ""
        if SearchObj is not None:
            instance = SearchObj.group(1)
        group =  str(params[3]).strip("\("+instance+"\)")
        counterName =  params[4]

        relation = []
        index = 0
        #find index of chosen counter
        for i in range(len(self.counters)):
            if ((self.counters)[i].getInstance() == instance) and ((self.counters)[i].getGroupName() == group) and ((self.counters)[i].getCounterName == counterName):
                    index = i
                    break
        #calculate correlation
        for i in range(len(self.counters)):
            if i != index:
                print((self.counters)[i].getGroupName())
                print((self.counters)[i].getCounterName())
                self.relations.append(((self.counters)[i], self.calculate(i, index)))
        #(self.relations).sort()
        self.relations = sorted(self.relations,key = lambda x:x[1],reverse=True) 

        for relation in self.relations:
            print(relation)
        return self.relations

    #compare peak time            
    def PeakMatch(xindex, yindex):
        xstats=counters[xindex].stats
        ystats=counters[yindex].stats
        xwave = wave_guess(xstats)
        ywave = wave_guess(ystats)


        for i in range(len(xwave)):
            x.append(xstats[i][1])

        for i in range(len(ystats)):
            y.append(ystats[i][1])


    def wave_guess(arr):
    
        wn = int(len(arr)/10) #没有经验数据，先设置成1/10。
        print(wn)
        #计算最小的N个值，也就是认为是波谷
        x= [x[1] for x in arr]

        wave_crest = heapq.nlargest(wn, enumerate(x), key= lambda x: x[1] )
        print(wave_crest)

        #计算最大的5个值，也认为是波峰
        wave_base = heapq.nsmallest(wn, enumerate(x), key= lambda x:x[1])

        print("######### result #########")
        #波峰，波谷的平均值的差，是波动周期，对于股票就是天。
        #wave_period = abs(int( wave_crest_mean[0] - wave_base_mean[0]))

       # wavelist = wave_crest_mean.append(wave_base_mean)

        ############### 以下为画图显示用 ###############
        wave_crest_x = [] #波峰x
        wave_crest_y = [] #波峰y
        for i,j in wave_crest:
            wave_crest_x.append(i)
            wave_crest_y.append(j)

        wave_base_x = [] #波谷x
        wave_base_y = [] #波谷y
        for i,j in wave_base:
            wave_base_x.append(i)
            wave_base_y.append(j)

        #将原始数据和波峰，波谷画到一张图上
        plt.figure(figsize=(20,10))
        plt.plot_date(arr[0],x)
        plt.plot(wave_base_x, wave_base_y, 'go')#红色的点
        plt.plot(wave_crest_x, wave_crest_y, 'ro')#蓝色的点
        plt.grid()
        plt.show()

  
        #return wavelist

def readCounter(path):
    f=open(path,'r')
    lines=f.readlines()
    numj = 0
    counterNames = []
    for line in lines:
        if numj == 0:
            result =  line.strip('\n').split('\",')
            for i in result:
                if i != result[0]:
                    counterNames.append(i.strip('\"'))
            numj = numj+1
        else:
            break

    #print(counterNames)
    return counterNames

'''
path = 'C:\\Users\\zhizhwan\\Source\\Repos\\happy-hacking-repo\\SuperPerfmonAnalyzer\\PythonApplication1\\csvrepo\\2018-07-21_113942.csv'
correlationObj = Core(path)
correlationObj.readCSV(path)
chosedCounter = r'\\DPCPRDSQLN05\Process(svchost#11)\Page Faults/sec'
correlationObj.FindCorrelation(chosedCounter)
'''