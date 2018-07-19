
# ======================
# imports
# ======================
from tkinter import *
from Parser import convertBlgToCsv
from tkinter import Menu
from os import path
from tkinter import filedialog
from ttkthemes import ThemedStyle
#from ttkthemes import themed_tk as tk   # Also imports the normal tk definitions, such as Button, Label, etc.
from tkinter import ttk
from tkinter.ttk import *
from tkinter import messagebox
import Parser
import subprocess
import sys
import datetime
import os
from inspect import getsourcefile
#packages for plot
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from Correlation import Core
from Correlation import readCounter

class GUI():	

	def __init__(self,master):
		self.master = master
		master.title("Perfmon Analyzer 1.0")

		self.value = ('Null') 
		self.path = ""

		self.lable0 = ttk.Label(master, text=" ").grid(column=0, row=0, sticky='E')

		# PART1
		self.lableupload = ttk.Label(master, text="Upload your perfmon file").grid(column=0, row=1, sticky='W')
		#first button, upload file
		self.btnupload = ttk.Button(master, text="Upload", command=self.clicked)
		self.btnupload.grid(column=1, row=2, sticky='W')


		self.var = StringVar()
		self.var.set('Please upload  "*.blg" or "*.csv" file')
		self.fileframe = Entry(master, textvariable=self.var, width = 40 )
		self.fileframe.grid(column=0, row=2, sticky='W')




		# PART2
		self.lablecounter = ttk.Label(master, text="Choose a counter:").grid(column=0, row=3, sticky='W')
		# Adding a Combobox
		self.counter = StringVar()
		print(self.path)
		self.counterChosen = ttk.Combobox(master, width=12, textvariable=self.counter)
		#===========================================================================================
		print(self.value)
		self.counterChosen['value'] = self.value 
		self.counterChosen.grid(column=0, row=4, sticky='W')

		self.counterChosen.current = self.counterChosen.current(0)  # ???????,????['values']???
		self.counterChosen.config = self.counterChosen.config(state='readonly')  # ??????

		#self.counterChosen.bind('<<ComboboxSelected>>', comboChange)
		#second button, run analyzer
		
		self.btngo = ttk.Button(master, text="Go", command=self.plot)
		self.btngo.grid(column=1, row=4, sticky='W')

		self.lable7 = ttk.Label(master, text=" ").grid(column=0, row=7, sticky='E')
		self.lable8 = ttk.Label(master, text=" ").grid(column=0, row=8, sticky='E')



		# PART3
		self.lableauto = ttk.Label(master, text="No special counter, I just want to do a general check ").grid(column=0, row=9, sticky='E') #,font='Calibri 10 bold'
		#first button, upload file
		self.btnauto = ttk.Button(master, text="Just Analyze for me", command= self.todo)
		self.btnauto.grid(column=0, row=10, sticky='W')


	def clicked(self):
		self.path = filedialog.askopenfilename(filetypes=(("blg files", "*.blg"), ("csv files", "*.csv"))) #(initialdir= path.dirname(__file__))
		self.path = convertBlgToCsv(self.path)
		print(self.path)
		names = readCounter(self.path)
		self.counterChosen['value'] = names
		messagebox.showinfo('info','counter got!')
		return self.path

	def plot (self):
		self.counterChosen.current = self.counterChosen.get()
		self.chosedCounter = self.counterChosen.get()
		print("yoo")
		print(self.counterChosen.get())
		print(self.path)
		mypath = self.path
		correlationObj = Core(mypath)
		correlationObj.readCSV(mypath)
		correlationObj.FindCorrelation(self.chosedCounter)
		messagebox.showinfo('Alter','Please upload your file first! ')
		

	def todo(self):
		
		messagebox.showinfo('Python Message Info Box', '??:????!!!')
 #Combobox change handling
	def comboChange(self,event):
		self.counterChosen.current = self.counterChosen.get()
		#self.chosedCounter = self.counterChosen.index(self.counterChosen.current)
		return self

window = Tk()

my_gui = GUI(window)
#style = ThemedStyle(window)
#style.set_theme("arc") 
## ?????????????
#for child in wino.winfo_children():
#    child.grid_configure(padx=10, pady=5)
window.mainloop()
