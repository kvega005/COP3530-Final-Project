from tkinter import *
from data import *
from tkinter.messagebox import showinfo
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


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
            prints the item chosen in the statistic dropdown menu
        purpose:
            track selections made in the statistic drop down menu
        """
        print(self.statistic.get())

    def change_graph(self, var_name, index, operation):
        """
        input: 
            @var_name: name of variable modified
            @index: index of variable if it is a list or an empty string
            @operation: the operation performed on the variable ("w": write, "r":read)
        output:
            prints the item chosen in the graph type dropdown menu
        purpose:
            track selections made in the graph type drop down menu
        """
        print(self.graph_type.get())

    def popup_showinfo(self, string = "Error!"):
        """
        input:
            @string: Error message to be displayed in popup window
        output:
            popup window with message
        purpose:
            Warn user of erroneous inputs
        """
        showinfo("Window", string)

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
            if new_size < 1:
                raise ValueError

        except ValueError:
            self.popup_showinfo("Error: Sample size must be a positive, non zero integer!") 

        self.sample_size = new_size
        self.updateGraph()
            
    def inputStats(self, mean, median, deviation, iqr):
        """
        input:
            @mean: the mean of the sample
            @median: the median of the sample
            @deviation: the standard deviation of the sample
            @iqr: the iqr of the sample
        output:
            displays statistics in the window
        purpose:
            reports results of the sampling to the user
        """

        self.mean_label.config(text="Mean: " + str(mean))
        self.median_label.config(text="Median: " + str(median))
        self.deviation_label.config(text="Standard Deviation: " + str(deviation))
        self.iqr_label.config(text="IQR: " + str(iqr))

    def updateGraph(self):
        """
        input:
            @figure: the matplotlib graph of the data
        output:
            updates the graph
        purpose:
            allows user to see the sample distribution
        """
        self.data.sample(self.statistic.get(), N = self.sample_size)
        histogram_args = self.data.histogram()
        
        plot = self.chart.figure.gca()
        plot.clear()
        plot.hist(histogram_args[0], histogram_args[1], alpha = 0.5, label = self.statistic.get())
        self.chart.draw()

    def __init__(self):
        self.root = Tk()
        self.data = Data("C:\Kevin\Code\COP3530-Final-Project\Project Code\Data\Batting.csv")
        self.sample_size = 1

        statistics = self.data.statistics()

        self.data.sample(statistics[0], N = self.sample_size)

        # Make Left Frame For Graph And Statistics
        self.left_frame = Frame(self.root)
        self.left_frame.pack(side = LEFT)

        # Make Right Frame For User Manipulation

        self.right_frame = Frame(self.root)
        self.right_frame.pack(side = LEFT)
        
        # Graph Label

        self.graph_label = Label(self.left_frame, text = "Graph", fg = "black", font = "Verdana 10 bold")
        self.graph_label.pack(side = TOP)

        # Graph
        fig = plt.Figure(figsize=(5,4), dpi = 100)
        plot = fig.gca()
        histogram_args = self.data.histogram()
        

        plot.hist(histogram_args[0], histogram_args[1], alpha = 0.5, label = statistics[0])
        self.chart = FigureCanvasTkAgg(fig,self.left_frame)
        self.chart.get_tk_widget().pack()

        # Results Labels

        self.results_label = Label(self.left_frame, text = "Statistics", fg = "black", font = "Verdana 10 underline")
        self.results_label.pack(side = TOP)

        self.mean_label = Label(self.left_frame, text = "Mean: ", fg = "black")
        self.mean_label.pack(side = TOP)

        self.median_label = Label(self.left_frame, text = "Median: ", fg = "black")
        self.median_label.pack(side = TOP)

        self.deviation_label = Label(self.left_frame, text = "Standard Deviation: ", fg = "black")
        self.deviation_label.pack(side = TOP)

        self.iqr_label = Label(self.left_frame, text = "IQR: ", fg = "black")
        self.iqr_label.pack(side = TOP)

        # Label for statistic drop down menu
        self.statistic_label = Label(self.right_frame, text = "Statistic:", fg = "black")
        self.statistic_label.pack(side = TOP, anchor = "nw")

        # Create option menu for statistic
        self.statistic = StringVar(self.root)
        self.statistic.set(statistics[0]) # default value
        self.statistic.trace("w", self.change_statistic) # track if statistic variable is written to

        
        self.statistic_dropdown = OptionMenu(*(self.right_frame, self.statistic) + tuple(statistics))
        self.statistic_dropdown.pack(side = TOP, anchor = "w")

        # Label for sample size entry box
        self.sample_size_label = Label(self.right_frame, text = "Sample Size:", fg = "black")
        self.sample_size_label.pack(side = TOP, anchor = "nw")


        # Sample size entry box
        self.right_entry = Spinbox(self.right_frame, from_ = 1, to = 10000, width = 6)
        self.right_entry.bind("<Return>", self.update_sample_size)
        self.right_entry.bind("<Leave>", self.update_sample_size)
        self.right_entry.pack(side = TOP, anchor = "nw")


         # Label for graph drop down menu
        self.graph_label = Label(self.right_frame, text = "Graph:", fg = "black")
        self.graph_label.pack(side = TOP, anchor = "nw")

        # Graph type label
        graph_statistics = ["Histogram", "Box Plot", "Frequency Plot"]

        self.graph_type = StringVar(self.root)
        self.graph_type.set(graph_statistics[0]) # default value
        self.graph_type.trace("w", self.change_graph) # track if statistic variable is written to

        # Create option menu for statistic
        self.statistic_dropdown = OptionMenu(*(self.right_frame, self.graph_type) + tuple(graph_statistics))
        self.statistic_dropdown.pack(side = TOP, anchor = "nw")
        

        #creates the first check box with a variable called cb1 to store the 0 for unchecked or 1 for checked
        checkBox_1 = Checkbutton(self.right_frame,
        text = "Normalize Data",
        anchor = "w"
        #variable = cb1,
        )
        checkBox_1.pack()
        
        #creates the second check box with a variable called cb2 to store the 0 for unchecked or 1 for checked
        checkBox_2 = Checkbutton(self.right_frame,
        text = "Compare Sample to Population",
        #variable = cb2,
        )
        checkBox_2.pack()
       
        #creates the third check box with a variable called cb3 to store the 0 for unchecked or 1 for checked
        checkBox_3 = Checkbutton(self.right_frame,
        text = "Compare to Normal Distribution",
        #variable = cb3,
        )
        checkBox_3.pack()

        #creates a label with a variable to display the run time for the first algorithm
        algorithm1 = StringVar()
        algo1 = Label( self.right_frame,
        textvariable=algorithm1, 
        text = "Algorithm 2 time:",
        )
        algorithm1.set("here would be the time in ms with the variable int as a string")
        algo1.pack()


        #creates a label with a variable to display the run time for the second algorithm
        algorithm2 = StringVar()
        algo2 = Label( self.right_frame,
        text = "Algorithm1 2 time:",
        textvariable=algorithm2, 
        
        )
        algorithm2.set("here would be the time in ms with the variable int as a string") #example usage of how to set the lable for the two times
        algo2.pack()


        self.root.mainloop()


x = Window()
