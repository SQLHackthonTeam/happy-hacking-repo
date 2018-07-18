class PerfMon(object):
    
    def __init__(self, name, start_time, end_time, timezone):
        self.name = name
        self.start_time = start_time
        self.end_time = end_time
        self.timezone = timezone

    def getName(self):
        return self.name

    def getStartTime(self):
        return self.start_time

    def getEndTime(self):
        return self.end_time

    def getTimezone(self):
        return self.timezone
    
    def __str__(self):
        return "%s is captured in %s" % (self.name, self.timezone)

class CounterGroup(PerfMon):
    
    def __init__(self, name, start_time, end_time, timezone, group_name):
        PerfMon.__init__(self, name, start_time, end_time, timezone)
        self.group_name = group_name

    def getGroupName(self):
        return self.group_name

class Counter(CounterGroup):

    stats = []

    def __init__(self, name, start_time, end_time, timezone, group_name, counter_name, parent, instance, computer):
        CounterGroup.__init__(self, name, start_time, end_time, timezone, group_name)
        self.counter_name = count_name
        self.parent = parent
        self.instance = instance
        self.computer = computer
        
    def getCounterName(self):
        return self.counter_name

    def addStats(time,value):
        stats.append((time,value))
        
    def showGraph(self):
        return null

