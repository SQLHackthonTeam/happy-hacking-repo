import subprocess, sys, datetime, os
from inspect import getsourcefile
from myClass import PerfMon, CounterGroup, Counter

def convertBlgToCsv(path):
    result = []
    filename = datetime.datetime.now().strftime("%Y-%m-%d_%H%M%S") + ".csv"
    myDirname = os.path.normpath(path)
    fileLocation = os.path.abspath(getsourcefile(lambda:0))
    parentPath = os.path.abspath(os.path.join(fileLocation, os.pardir))
    csvpath =  parentPath +"\\csvrepo\\" + filename

    if (myDirname[-4:] == ".csv" or myDirname[-4:] == ".CSV"):
        cmd = "copy " + '"' + myDirname + '" ' + '"' + csvpath + '"'
    else:
        cmd = "relog " + '"' + myDirname + '"' + " -f csv -o "+ '"' + csvpath + '"'

    print(cmd)
    ...
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
    ...
    return csvpath



def drawPositive():
    return

def drawNegative():
    return