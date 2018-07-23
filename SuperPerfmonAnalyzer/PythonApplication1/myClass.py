import numpy as np

class PerfMon(object):
    
    def __init__(self, name, timezone):
        self.name = name
        self.timezone = timezone

    def getName(self):
        return self.name

    def getStartTime(self):
        return self.start_time

    def getEndTime(self):
        return self.end_time

    def getTimezone(self):
        return self.timezone

    def setStartTime(time):
        self.start_time = time

    def setEndTime(time):
        self.end_time = time
    
    def __str__(self):
        return "%s is captured in %s" % (self.name, self.timezone)

class CounterGroup(PerfMon):
    
    def __init__(self, timezone, group_name):
        PerfMon.__init__(self, "Perfmon",timezone)
        self.group_name = group_name

    def setStartTime(time):
        self.start_time = time

    def setEndTime(time):
        self.end_time = time

    def getGroupName(self):
        return self.group_name

class Counter(CounterGroup):

    stats = []
    
    def __init__(self, timezone,computer,instance, group_name, counter_name ):
        CounterGroup.__init__(self, timezone, group_name)
        self.counter_name = counter_name
        self.group_name = group_name
        self.instance = instance
        self.computer = computer
        self.stats =[]
        self.xVal = []
        self.yVal = []
        
    def getCounterName(self):
        return self.counter_name

    def getInstance(self):
        return self.instance

    def getGroupName(self):
        return self.group_name

    def transform(self):
        data = np.array(self.stats)
        self.xVal,self.yVal = data.T
        return self

    def showGraph(self):
        return null