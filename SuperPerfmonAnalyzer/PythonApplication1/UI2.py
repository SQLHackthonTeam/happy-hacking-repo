#From ttkthemes import themed_tk as tk   
#Also imports the normal tk definitions, such as Button, Label, etc.
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from ttkthemes import ThemedStyle
from tkinter import ttk
from tkinter.ttk import *
import threading
from tkinter import  HORIZONTAL

#packages for plot
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

#Import Parser.py and Correlation.py
from Parser import *
from Correlation import *

class GUI():    

    def __init__(self,master):
        self.master = master
        master.title("Super Perfmon Analyzer 1.0")

        self.value = ("CounterName")        #Comparing Counter Name
        self.blgpath = ""                    #Temporarly Path for Perfmon Files(blg)
        self.csvpath = ""                    #Temporarly Path for Perfmon Files(csv)
        self.counterWidth = 70                #Counter Name Combobox default width


        self.lable0 = ttk.Label(master, text="").grid(column=0, row=0, sticky='W')

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
        self.counterChosen.current = self.counterChosen.current(0)  # ???????,????['values']???
        self.counterChosen.config = self.counterChosen.config(state='readonly')  # ??????
        
        self.btngo = ttk.Button(master, text="Generate Report", command=self.plot)
        self.btngo.grid(column=1, row=3, sticky='E', padx=(10,10))
        

        #Add more space
        self.lable7 = ttk.Label(master, text="").grid(column=0, row=7, sticky='W')
        self.lable8 = ttk.Label(master, text="").grid(column=0, row=8, sticky='W')
        


        # PART3
        self.lableauto = ttk.Label(master, text="AI Analyzer").grid(column=0, row=9, sticky='W', padx=(10,10)) 

        self.presetEnv = ttk.Combobox(master, width=20, value=["SQL Server", "Sharepoint","Windows"])
        self.presetEnv.current = self.presetEnv.current(0) 
        self.presetEnv.grid(column=0, row=10, sticky='W', padx=(10,10))
        
        self.btnauto = ttk.Button(master, text="Generate Report", command= self.todo)
        self.btnauto.grid(column=1, row=10, sticky='E', padx=(10,10))

        self.lable11 = ttk.Label(master, text="").grid(column=0, row=11, sticky='W')
        self.lable12 = ttk.Label(master, text="").grid(column=0, row=12, sticky='W')

        # Quit window
        self.btnquit= ttk.Button(master, text="Quit", command=master.destroy)
        self.btnquit.grid(column=0, row=13, padx=(10,5))

        self.lable13 = ttk.Label(master, text="").grid(column=0, row=14, sticky='W')

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

        #Show progress bar when job running 
        def real_traitement():
            self.progress = Progressbar(orient=HORIZONTAL,length=400,  mode='indeterminate')
            self.progress.grid(row=7)
            self.progress.start()

            correlationObj = Core(mypath)
            correlationObj.readCSV(mypath)
            correlationObj.FindCorrelation(self.chosedCounter)

            self.progress.stop()
            self.progress.grid_forget()

        threading.Thread(target=real_traitement).start()


#        messagebox.showinfo('Alter','Please upload your file first! ')
        

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
## ?????????????
for child in window.winfo_children():
    child.grid_configure(padx=10, pady=5)
window.mainloop()
