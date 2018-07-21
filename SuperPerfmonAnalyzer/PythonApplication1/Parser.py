import subprocess, sys, datetime, os
from inspect import getsourcefile
from myClass import PerfMon, CounterGroup, Counter



def convertBlgToCsv(path):
    result = []

    filename = datetime.datetime.now().strftime("%Y-%m-%d_%H%M%S") + ".csv"

#    cmd = "relog " + path.encode('unicode_escape').decode() + " -f csv -o " + abspath(getsourcefile(lambda:0)) +"csvrepo\\" + filename
    myDirname = os.path.normpath(path)
    fileLocation = os.path.abspath(getsourcefile(lambda:0))
    print (fileLocation)
    parentPath = os.path.abspath(os.path.join(fileLocation, os.pardir))
    print (parentPath)
    cmd = "relog " + '"' + myDirname + '"' + " -f csv -o " + parentPath +"\\csvrepo\\" + filename

    csvpath =  parentPath +"\\csvrepo\\" + filename
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
