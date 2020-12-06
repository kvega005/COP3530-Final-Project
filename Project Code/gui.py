from tkinter import *
from data import *
from tkinter.messagebox import showinfo
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from numpy import *


# https://www.tutorialspoint.com/python/tk_pack.htm
# For making tkinter GUI

GATOR_BLUE = "#003087"
GATOR_ORANGE = '#FA4616'

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
        self. stat = self.statistic.get()
        
        time = self.data.sample(self.stat, N = self.sample_size, sorting_alg = self.radio_variable.get())

        if self.var1.get() == 1:
            self.data.normalize_sample()
        
        self.alg_label.config(text="Sorting Time: %d ns" % time)
        
        self.updateGraph()
        self.updateStats()


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
        self.updateGraph()

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

    def update_sample_size(self, var_name, index, operation):
        """
        input: 
            @var_name: name of variable modified
            @index: index of variable if it is a list or an empty string
            @operation: the operation performed on the variable ("w": write, "r":read)
        output:
            prints new sample size
        purpose:
            track inputs to sample size entry box
        """
        if not self.sample.get() == "" and int(self.sample.get()) >= 2:
            new_size = int(self.sample.get())

            try:
                if new_size > len(self.data.df[self.stat]):
                    raise ValueError

                if self.sample_size != new_size:
                    self.sample_size = new_size

                    time = self.data.sample(self.stat, N = self.sample_size, sorting_alg = self.radio_variable.get())
                    
                    if self.var1.get() == 1:
                        self.data.normalize_sample()
                    
                    self.alg_label.config(text="Sorting Time: %d ns" % time)

                    self.updateGraph()
                    self.updateStats()
            
            except ValueError:
                self.popup_showinfo("Error! Sample size cannot be greater than population size or less than 0.")

            
    def updateStats(self):
        """
        input:
            @NaN
        output:
            displays statistics in the window
        purpose:
            reports results of the sampling to the user
        """
        mean, median, std_variation, max_val, min_val = self.data.report()
        
        self.n_label.config(text="N: " + str(self.sample_size))
        self.mean_label.config(text="Mean: " + str(round(mean,2)))
        self.median_label.config(text="Median: " + str(round(median,2)))
        self.deviation_label.config(text="Std Dev: " + str(round(std_variation,2)))
        self.max_val_label.config(text="Max: " + str(round(max_val,2)))
        self.min_val_label.config(text="Min: " + str(round(min_val,2)))

    def updateGraph(self):
        """
        input:
            @figure: the matplotlib graph of the data
        output:
            updates the graph
        purpose:
            allows user to see the sample distribution
        """       
        histogram_args = self.data.histogram()
        
        graph = self.graph_type.get()
        
        plot = self.chart.figure.gca()
        plot.clear()
        plot.set_facecolor("black")
        
        plot.spines['bottom'].set_color('white')
        plot.xaxis.label.set_color('white')
        plot.tick_params(axis='x', colors='white')

        plot.spines['left'].set_color('white')
        plot.xaxis.label.set_color('white')
        plot.tick_params(axis='y', colors='white')
        
        plot.set_title(self.stat)
        plot.title.set_color("white")

        if graph == "Box Plot":
            bp = plot.boxplot(self.data.rand_sample)
            
            for box in bp['boxes']:
                # change outline color
                box.set( color=GATOR_ORANGE, linewidth=2)

            for whisker in bp['whiskers']:
                whisker.set(color=GATOR_ORANGE, linewidth=2)
            
            for cap in bp['caps']:
                cap.set(color=GATOR_ORANGE, linewidth=2)

            ## change color and linewidth of the medians
            for median in bp['medians']:
                median.set(color=GATOR_ORANGE, linewidth=2)

            for flier in bp['fliers']:
                flier.set(marker='o', color=GATOR_BLUE, alpha=1)

        else:
            histogram_args = self.data.histogram()
            if(self.var3.get()):
                mean, median, std, max_val, min_val = self.data.report()
                x = np.linspace(min_val, max_val, 100)
                
                n = lambda t: self.sample_size * t
                z = norm.pdf(x,mean,std)
                y = np.array([n(zi) for zi in z])

                plot.plot(x, y, color=GATOR_BLUE)
                
            plot.hist(histogram_args[0], histogram_args[1], color=GATOR_ORANGE,  alpha = 0.9, label = self.stat)
        
        self.chart.draw()

    def normalize(self, var_name, index, operation):
        """
        input: 
            @var_name: name of variable modified
            @index: index of variable if it is a list or an empty string
            @operation: the operation performed on the variable ("w": write, "r":read)
        output:
            Change data points to Z-Scores, and update stats and graph
        purpose:
            Normalize data
        """
        if self.var1.get() == 1:
            self.data.normalize_sample()
            self.updateStats()
            self.updateGraph()
        
        if self.var1.get() == 0:
            self.data.denormalize_sample()
            self.updateStats()
            self.updateGraph()

    def __init__(self, path):
        self.root = Tk()
        self.data = Data(path)
        self.sample_size = 2

        statistics = self.data.statistics()

        time = self.data.sample(statistics[0], N = self.sample_size)
        
        self.root.tk_setPalette(
            background='black', 
            foreground="white",
            activeBackground=GATOR_BLUE, 
            activeForeground="white"
            )

        # Make Left Frame For Graph And Statistics
        self.left_frame = Frame(self.root)
        self.left_frame.pack(side = LEFT, padx = 10)

        # Make Right Frame For User Manipulation

        self.right_frame = Frame(self.root)
        self.right_frame.pack(side = LEFT, anchor= "nw", padx = 10)
        
        # Graph Label

        #self.graph_label = Label(self.left_frame, text = "Data", font = "Verdana 16 bold")
        #self.graph_label.pack(side = TOP)

        # Graph
        fig = plt.Figure(figsize=(5,4), dpi = 100)
        fig.patch.set_facecolor("black")
        plot = fig.gca()

        plot.set_facecolor("black")
        
        plot.spines['bottom'].set_color('white')
        plot.xaxis.label.set_color('white')
        plot.tick_params(axis='x', colors='white')

        plot.spines['left'].set_color('white')
        plot.xaxis.label.set_color('white')
        plot.tick_params(axis='y', colors='white')

        histogram_args = self.data.histogram()
        
        plot.set_title(statistics[0])
        plot.title.set_color("white")
        plot.hist(histogram_args[0], histogram_args[1], color=GATOR_ORANGE,  alpha = 0.9, label = statistics[0])
        self.chart = FigureCanvasTkAgg(fig,self.left_frame)
        self.chart.get_tk_widget().pack()

        # Results Labels
        self.results_frame = Frame(self.left_frame)

        self.results_label = Label(self.results_frame, text = "Statistics", font = "Verdana 10 underline")
        self.results_label.pack(side = TOP, anchor = "w")

        self.n_label = Label(self.results_frame, text = "N: ")
        self.n_label.pack(side = TOP, anchor = "w")

        self.mean_label = Label(self.results_frame, text = "Mean: ")
        self.mean_label.pack(side = TOP, anchor = "w")

        self.deviation_label = Label(self.results_frame, text = "Std Dev: ")
        self.deviation_label.pack(side = TOP, anchor = "w")

        self.median_label = Label(self.results_frame, text = "Median: ")
        self.median_label.pack(side = TOP, anchor = "w")

        self.max_val_label = Label(self.results_frame, text = "Max: ")
        self.max_val_label.pack(side = TOP, anchor = "w")

        self.min_val_label = Label(self.results_frame, text = "Min: ")
        self.min_val_label.pack(side = TOP, anchor = "w")

        self.results_frame.pack(side = TOP)
        # Choose algorithm
        alg_frame = Frame(self.right_frame)
        alg_frame.pack(side = TOP, anchor = "nw")

        self.radio_variable = StringVar()
        self.radio_variable.set("MergeSort")

        radiobutton1 = Radiobutton(
            alg_frame, 
            text="MergeSort", 
            variable=self.radio_variable, 
            selectcolor = "black",
            value="MergeSort"
            )
        radiobutton2 = Radiobutton(
            alg_frame, 
            text="QuickSort", 
            selectcolor = "black",
            variable=self.radio_variable, 
            value="QuickSort"
            )

        radiobutton1.pack(side = LEFT, anchor="nw")
        radiobutton2.pack(side = LEFT, anchor = "nw")

        alg_frame.pack(side = TOP, anchor = "nw")

        # Label for statistic drop down menu
        self.statistic_label = Label(self.right_frame, text = "Statistic:")
        self.statistic_label.pack(side = TOP, anchor = "nw")

        # Create option menu for statistic
        self.statistic = StringVar(self.root)
        self.statistic.set(statistics[0]) # default value
        self.statistic.trace("w", self.change_statistic) # track if statistic variable is written to

        self.stat = statistics[0]

        self.statistic_dropdown = OptionMenu(*(self.right_frame, self.statistic) + tuple(statistics))
        self.statistic_dropdown.pack(side = TOP, anchor = "w")

        # Label for sample size entry box
        self.sample_size_label = Label(self.right_frame, text = "Sample Size:")
        self.sample_size_label.pack(side = TOP, anchor = "nw")

        # Sample size entry box
        self.sample = StringVar(self.root)
        self.right_entry = Spinbox(
            self.right_frame, 
            textvariable = self.sample,
            from_ = 2, 
            to = 100000, 
            width = 6
        )
        self.sample.trace("w",self.update_sample_size)
        self.right_entry.pack(side = TOP, anchor = "nw")


         # Label for graph drop down menu
        self.graph_label = Label(self.right_frame, text = "Graph Type:")
        self.graph_label.pack(side = TOP, anchor = "nw")

        # Graph type label
        graph_statistics = ["Histogram", "Box Plot"]

        self.graph_type = StringVar(self.root)
        self.graph_type.set(graph_statistics[0]) # default value
        self.graph_type.trace("w", self.change_graph) # track if statistic variable is written to

        # Create option menu for statistic
        self.statistic_dropdown = OptionMenu(*(self.right_frame, self.graph_type) + tuple(graph_statistics))
        self.statistic_dropdown.pack(side = TOP, anchor = "nw")
        

        #creates the first check box with a variable called cb1 to store the 0 for unchecked or 1 for checked
        self.var1 = IntVar()
        checkBox_1 = Checkbutton(
            self.right_frame,
            text = "Normalize Data",
            selectcolor = "black",
            anchor = "w",
            variable = self.var1
        )
        checkBox_1.pack(side = TOP, anchor = "nw")
        self.var1.trace("w", self.normalize)
       
        #creates the third check box with a variable called cb3 to store the 0 for unchecked or 1 for checked
        self.var3 = IntVar()
        checkBox_3 = Checkbutton(   
            self.right_frame,
            selectcolor = "black",
            text = "Compare to Normal Distribution",
            variable = self.var3
        )
        checkBox_3.pack(side = TOP, anchor = "nw")

        #creates a label with a variable to display the run time for the first algorithm
        self.alg_label = Label( 
            self.right_frame,
            text = "Sorting Time: %d s" % time
        )
        self.alg_label.pack(side = TOP, anchor = "nw")

        self.root.mainloop()
