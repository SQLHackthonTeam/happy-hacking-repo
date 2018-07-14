import subprocess
import sys
import datetime

def convertBlgToCsv(path):
    result = []
    cmd = "relog " + path.encode('unicode_escape').decode() + " -f csv -o F:\\source\\repos\\SuperPerfmonAnalyzer\\csvrepo\\" + datetime.datetime.now().strftime("%Y-%m-%d_%H%M%S") + ".csv"
    print(cmd)
    process = subprocess.Popen(cmd,
                               shell=True,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
    for line in process.stdout:
        result.append(line)
    errcode = process.returncode
    for line in result:
        print(line)
    if errcode is not None:
        raise Exception('cmd %s failed, see above for details', cmd)



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
        self.instance = instance
        self.computer = computer
        self.stats =[]
        
    def getCounterName(self):
        return self.counter_name
        
    def showGraph(self):
        return null



