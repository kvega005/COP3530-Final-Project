from tkinter import *
from tkinter.messagebox import showinfo

# https://www.tutorialspoint.com/python/tk_pack.htm
# For making tkinter GUI

class Window:
    def change_statistic(self, var_name, index, operation):
        """
        input: 
            @var_name: name of variable modified
            @index: index of variable if it is a list or an empty string
            @operation: the operation performed on the variable ("w": write, "r":read)
        output:
            prints the item chosen in the dropdown menu
        purpose:
            track selections made in the statistic drop down menu
        """
        print(self.variable.get())

    def popup_showinfo(self):
        """
        input:
            NaN
        output:
            popup window with message
        purpose:
            Warn user of erroneous inputs
        """
        showinfo("Window", "Sample size must be an integer!!")

    def update_sample_size(self, event):
        """
        input:
            @event: event peformed on sample size entry widget
        output:
            prints new sample size
        purpose:
            track inputs to sample size entry box
        """
        try:
            new_size = int(self.right_entry.get())
            print(new_size)

        except ValueError:
            self.popup_showinfo()  
            

    def __init__(self):
        self.root = Tk()

        # Make Left Frame For Graph And Statistics
        self.left_frame = Frame(self.root)
        self.left_frame.pack(side = LEFT)

        # Make Right Frame For User Manipulation

        self.right_frame = Frame(self.root)
        self.right_frame.pack(side = LEFT)

        # Label for statistic drop down menu
        self.statistic_label = Label(self.right_frame, text = "Statistic:", fg = "black")
        self.statistic_label.pack(side = TOP)

        # Options to be used in the drop down menu
        options = ["Hits", "Homeruns", "Batting Average"]

        self.variable = StringVar(self.root)
        self.variable.set(options[0]) # default value
        self.variable.trace("w", self.change_statistic) # track if statistic variable is written to

        # Create option menu for statistic
        self.statistic_dropdown = OptionMenu(*(self.right_frame, self.variable) + tuple(options))
        self.statistic_dropdown.pack()

        # Label for sample size entry box
        self.sample_size_label = Label(self.right_frame, text = "Sample Size:", fg = "black")
        self.sample_size_label.pack(side = TOP)

        # Sample size entry box
        self.right_entry = Entry(self.right_frame, text = "0")
        self.right_entry.bind("<Return>", self.update_sample_size)
        self.right_entry.pack(side = TOP)

        self.root.mainloop()

x = Window()