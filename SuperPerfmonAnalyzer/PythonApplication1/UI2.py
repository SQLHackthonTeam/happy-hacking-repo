#From ttkthemes import themed_tk as tk   
#Also imports the normal tk definitions, such as Button, Label, etc.
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from ttkthemes import ThemedStyle
from tkinter import ttk
from tkinter.ttk import *

#packages for plot
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from itertools import groupby
from math import *

#Import Parser.py and Correlation.py
from Parser import *
from Correlation import *

class GUI():    

    def __init__(self,master):
        self.master = master
        master.title("Super Perfmon Analyzer 1.0")

        self.value = ("CounterName")        #Comparing Counter Name
        self.blgpath = ""                   #Temporarly Path for Perfmon Files(blg)
        self.csvpath = ""                   #Temporarly Path for Perfmon Files(csv)
        self.counterWidth = 70              #Counter Name Combobox default width
        self.comparingResult = []			#Comparing result after correlation calculation
        self.baseCounter = Counter("","","","","")
        self.posComparingResult = []
        self.negComparingResult = []
        self.posGroup = []
        self.negGroup = []



        self.lable0 = ttk.Label(master, text="").grid(column=0, row=0, sticky='E')

        #Uploading Part
        self.lableupload = ttk.Label(master, text="Choose your perfmon file").grid(column=0, row=0, sticky='W', padx=(10,10))

        self.var = StringVar()
        self.var.set('Please upload "*.blg" or "*.csv" file')
        self.fileframe = Entry(master, textvariable=self.var, width = 40 )
        self.fileframe.grid(column=0, row=1, sticky='W', padx=(10,10))

        self.btnupload = ttk.Button(master, text="Upload", command=self.clicked)
        self.btnupload.grid(column=1, row=1, sticky='E', padx=(10,10))


        #Comparing Part
        self.lablecounter = ttk.Label(master, text="Choose a counter").grid(column=0, row=2, sticky='W', padx=(10,10))

        self.counter = StringVar()
        self.counterChosen = ttk.Combobox(master, width=self.counterWidth, textvariable=self.counter)
        self.counterChosen['value'] = self.value 
        self.counterChosen.grid(column=0, row=3, sticky='W', padx=(10,10))
        self.counterChosen.current = self.counterChosen.current(0)  
        self.counterChosen.config = self.counterChosen.config(state='readonly')  
        
        self.btngo = ttk.Button(master, text="Generate Report", command=self.plot)
        self.btngo.grid(column=1, row=3, sticky='E', padx=(10,10))


        #Add more space
        self.lable7 = ttk.Label(master, text="").grid(column=0, row=7, sticky='E')
        self.lable8 = ttk.Label(master, text="").grid(column=0, row=8, sticky='E')
        
        
        #AI Analyzer
        self.lableauto = ttk.Label(master, text="AI Analyzer").grid(column=0, row=9, sticky='W', padx=(10,10)) 

        self.presetEnv = ttk.Combobox(master, width=20, value=["SQL Server", "Sharepoint","Windows"])
        self.presetEnv.grid(column=0, row=10, sticky='W', padx=(10,10))
        
        self.btnauto = ttk.Button(master, text="Generate Report", command= self.todo)
        self.btnauto.grid(column=1, row=10, sticky='W', padx=(10,10))

        self.lable9 = ttk.Label(master, text="").grid(column=0, row=11, sticky='E')

    def clicked(self):
        self.blgpath = filedialog.askopenfilename(filetypes=(("blg files", "*.blg"), ("csv files", "*.csv"))) 
        self.var.set(self.blgpath)

        self.csvpath = convertBlgToCsv(self.blgpath)
        self.counterChosen['value'] = readCounter(self.csvpath)
        messagebox.showinfo('info','Perfmon is loaded successfully!')
        return self.csvpath

    def plot (self):
        self.counterChosen.current = self.counterChosen.get()
        self.chosedCounter = self.counterChosen.get()
        print(self.counterChosen.get())
        print(self.csvpath)
        mypath = self.csvpath
        correlationObj = Core(mypath)
        correlationObj.readCSV(mypath)
        
        correlationObj.FindCorrelation(self.chosedCounter, 0.75, -0.75)
        self.posComparingResult = correlationObj.posRelations
        self.negComparingResult = correlationObj.negRelations

        self.posComparingResult = sorted(self.posComparingResult,key = lambda x:x[0].getGroupName(),reverse=False)
        self.negComparingResult = sorted(self.negComparingResult,key = lambda x:x[0].getGroupName(),reverse=False)

        self.posGroup = [list(it) for k,it in groupby(self.posComparingResult, lambda x:x[0].getGroupName())]
        self.negGroup = [list(it) for k,it in groupby(self.negComparingResult, lambda x:x[0].getGroupName())]

        self.baseCounter = correlationObj.baseCounter
        baseCounterName = self.baseCounter.getGroupName()+self.baseCounter.getCounterName()+self.baseCounter.getInstance()
        baseData = np.array(self.baseCounter.stats)
        baseX, baseY = baseData.T

        self.draw()
        
#        for relation in self.comparingResult[1:6]:
#            print(relation[0].getInstance()+relation[0].getGroupName()+relation[0].getCounterName())
#            print(relation[1])
#            data = np.array(relation[0].stats)
#            x,y = data.T
#            print(y)
#            print(baseY)
#
#            plt.plot(x, y, label=relation[0].getInstance()+relation[0].getGroupName()+relation[0].getCounterName())
#            plt.plot(baseX, baseY, label = baseCounterName)
#            plt.title("Comparing Graph")
#            plt.xlabel("Timestamp")
#            plt.ylabel("Value")
#            plt.legend()
#            plt.show()

    def calGrid(self,num):
        x = int(sqrt(num))
        if x*x > num:
            return x,x
        elif x*(x+1) > num:
            return (x+1),x
        else:
            return (x+1),(x+1)

    def draw(self):
        posLength = len(self.posGroup)
        negLength = len(self.negGroup)

        posGrid = []
        negGrid = []

        posX, posY = self.calGrid(posLength)
        negX, negY = self.calGrid(negLength)

        posFig = plt.figure(figsize=(posX*4,posY*4))

#        x,y = self.transform(self.baseCounter.stats)
        self.baseCounter.transform()
        x = self.baseCounter.xVal
        y = self.baseCounter.yVal

        
        for j in range(posLength):
            ax = plt.subplot2grid((posX,posY), (int(j/posY),(j%posY)), rowspan=1, colspan=1)
            for i in range(len(self.posGroup[j])):
                self.posGroup[j][i][0].transform()
#                print(self.posGroup[j][i][0].yVal) 
                ax.plot(x, self.posGroup[j][i][0].yVal, label=self.posGroup[j][i][0].getGroupName()+self.posGroup[j][i][0].getCounterName()+self.posGroup[j][i][0].getInstance())
                ax.set_title(self.posGroup[j][i][0].getGroupName())
                ax.set_xlabel("TIMESTAMP")
                ax.set_ylabel("VALUE")
#        plt.tight_layout()
#        plt.legend() 
#            plt.subplot2grid((posLength,1), (0,0), rowspan=1, colspan=1).plot(x,[pt[i][0].yVal for pt in self.posGroup[0]],label="base counter")

        negFig = plt.figure(figsize=(negX*4,negY*4))
      
        for j in range(negLength):
            ax = plt.subplot2grid((negX,negY), (int(j/negY),(j%negY)), rowspan=1, colspan=1)
            for i in range(len(self.negGroup[j])):
                self.negGroup[j][i][0].transform()
                print(self.negGroup[j][i][0].yVal) 
                ax.plot(x, self.negGroup[j][i][0].yVal, label=self.negGroup[j][i][0].getGroupName()+self.negGroup[j][i][0].getCounterName()+self.negGroup[j][i][0].getInstance())
                ax.set_title(self.negGroup[j][i][0].getGroupName())
                ax.set_xlabel("TIMESTAMP")
                ax.set_ylabel("VALUE")
        plt.tight_layout()
        plt.legend() 
        plt.show()
           

    def todo(self):
        
        messagebox.showinfo('Python Message Info Box', '??:????!!!')
 #Combobox change handling
    def comboChange(self,event):
        self.counterChosen.current = self.counterChosen.get()
        #self.chosedCounter = self.counterChosen.index(self.counterChosen.current)
        return self

window = Tk()

my_gui = GUI(window)
style = ThemedStyle(window)
style.set_theme("arc") 
for child in window.winfo_children():
    child.grid_configure(padx=10, pady=5)
window.mainloop()
