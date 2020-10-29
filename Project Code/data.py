from matplotlib import pyplot as plt 

import pandas as pd
import numpy as np
import random

# https://pandas.pydata.org/pandas-docs/stable/user_guide/10min.html
# For creating data frame

class Data:
    def __init__(self, path):
        self.df = pd.read_csv(path)
        # Get rid of non numeric data and rows with missing entries
        self.df = self.df._get_numeric_data()
        # Gets rid of rows with empty values
        self.df = self.df.dropna(axis= 'index')

        self.sample_size = 0
        self.rand_sample = []

    def sample(self, statistic, N):
        """
        input:
            @N: sample size
            @N: statistic to be sampled
        output:
            Sets sample class variable
        purpose:
            Make random sample from Data
        """
        self.sample_size = N
        self.rand_sample = np.array(self.df[statistic].sample(N))
        self.rand_sample = np.sort(self.rand_sample,kind = 'mergesort') # the mergesort implementation is actually timsort

    def histogram(self):
        plt.style.use('seaborn-deep')
        
        data_range = self.rand_sample[-1] - self.rand_sample[0]
        hist_bins = int(data_range/5)

        plt.hist(self.rand_sample, bins = hist_bins ,alpha = 0.5, label = "H")
        plt.hist(self.df["H"], bins = hist_bins, alpha = 0.5, label= "Population")
        plt.legend(loc='upper right')
        plt.show()
    
    def print_columns(self):
        print(self.df.keys())
        print(len(self.df["H"]))
        
x = Data("C:\Kevin\Code\COP3530-Final-Project\Project Code\Data\Batting.csv")
x.sample("SO", 10000)
x.histogram()
x.print_columns()