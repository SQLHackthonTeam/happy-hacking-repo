# ======================
# imports
# ======================
from tkinter import *
from tkinter import Menu
from os import path
from tkinter import filedialog
#from ttkthemes import themed_tk as tk   # Also imports the normal tk definitions, such as Button, Label, etc.
from tkinter import ttk
from tkinter.ttk import *
from tkinter import messagebox

#window = ttk.Style()
#window.theme_use('alt')
window = Tk()
window.title("Perfmon Analyzer 1.0")


# Tab Control introduced here --------------------------------------
tabControl = ttk.Notebook(window)  # Create Tab Control

tab1 = ttk.Frame(tabControl)  # Create a tab
tabControl.add(tab1, text='Home')  # Add the tab

tab2 = ttk.Frame(tabControl)  # Add a second tab
tabControl.add(tab2, text='Report')  # Make second tab visible

tabControl.pack(expand=1, fill="both")  # Pack to make visible
# ~ Tab Control introduced here -----------------------------------------


# ---------------Tab1控件介绍------------------#
# Modified Button Click Function
def clicked():
    file = filedialog.askopenfilename(filetypes=(("blg files", "*.blg"), ("csv files", "*.csv"))) #(initialdir= path.dirname(__file__))
    filename= file#print(file)
    return file

def multiply(a,b):
    #a,b两个列表的数据一一对应相乘之后求和
    sum_ab=0.0
    for i in range(len(a)):
        temp=a[i]*b[i]
        sum_ab+=temp
    return sum_ab

def todo():
    messagebox.showinfo('Python Message Info Box', '通知：还没开发！！！')

# PART1-----------------------------------------------------
ttk.Label(tab1, text="Upload your perfmon file").grid(column=0, row=0, sticky='W')
#first button, upload file
btn1 = ttk.Button(tab1, text="Upload", command=clicked)
btn1.grid(column=2, row=0, sticky='W')

# PART2-----------------------------------------------------
ttk.Label(tab1, text="Choose a counter:").grid(column=0, row=3, sticky='W')
# Adding a Combobox
counter = StringVar()
counterChosen = ttk.Combobox(tab1, width=12, textvariable=counter)
counterChosen['values'] = ('memory', 'cpu', 'io', 'etc')
counterChosen.grid(column=1, row=3, sticky='W')
counterChosen.current(0)  # 设置初始显示值，值为元组['values']的下标
counterChosen.config(state='readonly')  # 设为只读模式
#second button, run analyzer
btn2 = ttk.Button(tab1, text="Go", command=multiply)
btn2.grid(column=2, row=3, sticky='W')

# PART3-----------------------------------------------------
ttk.Label(tab1, text="No special counter, I just want to do a general check ").grid(column=0, row=4, sticky='W')
#first button, upload file
btn3 = ttk.Button(tab1, text="Just Analyze for me", command= todo)
btn3.grid(column=0, row=5, sticky='W')

# Using a scrolled Text control
'''scrolW = 30;
scrolH = 5
scr = scrolledtext.ScrolledText(monty, width=scrolW, height=scrolH, wrap=tk.WORD)
scr.grid(column=0, row=3, sticky='WE', columnspan=3)
'''

# 一次性控制各控件之间的距离
for child in tab1.winfo_children():
    child.grid_configure(padx=10, pady=5)


# ---------------Tab2控件介绍------------------#
ttk.Label(tab2, text="Top 1 counter:").grid(column=0, row=0, sticky='W')
canvas1 = Canvas(tab2, width=400, height=95, highlightthickness=0, bg='#FFFF00')
canvas1.grid(row=1, column=0)
ttk.Label(tab2, text="Top 2 counter:").grid(column=0, row=2, sticky='W')
canvas2 = Canvas(tab2, width=400, height=95, highlightthickness=0, bg='#FFFF00')
canvas2.grid(row=3, column=0)
ttk.Label(tab2, text="Top 3 counter:").grid(column=0, row=4, sticky='W')
canvas3 = Canvas(tab2, width=400, height=95, highlightthickness=0, bg='#FFFF00')
canvas3.grid(row=5, column=0)



# ----------------菜单栏介绍-------------------#


# Change the main windows icon
#win.iconbitmap(r'C:\Users\feng\Desktop\研.ico')

# Place cursor into name Entry
#nameEntered.focus()
# ======================
# Start GUI
# ======================
window.mainloop()





