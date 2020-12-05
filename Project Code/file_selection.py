from tkinter import * 
from tkinter.ttk import *
from gui import *

# importing askopenfile function 
# from class filedialog 
from tkinter.filedialog import askopenfile 

def HomeScreen():
    root = Tk() 
    root.geometry('200x100') 

    # This function will be used to open 
    # file in read mode and only Python files 
    # will be opened 
    def open_file(): 
        file = askopenfile(mode ='r', filetypes =[('.csv', '*.csv')]) 
        if file is not None:
            PATH = str(file.name) 
            root.destroy()
            x = Window(PATH)
            return PATH
            
    btn = Button(root, text ='Open', command = lambda:open_file()) 
    btn.pack(side = TOP, pady = 10) 

    mainloop() 

HomeScreen()