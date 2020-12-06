from matplotlib import pyplot as plt 

import pandas as pd
import numpy as np
import random
import time
import math

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

    def statistics(self):
        """
        input:
            NaN
        output:
            Returns list of statistics available in the csv file
        Purpose:
            Get a list of categories that can be used in the data analysis
        """
        return self.df.keys()

    def sample(self, statistic, N, sorting_alg = "MergeSort"):
        """
        input:
            @statistic: statistic to be sampled
            @N: sample size
        output:
            Sets sample class variable, returns time it took to sort the sample
        purpose:
            Make random sample from Data, and time the sorting algorithm used
        """
        self.sample_size = N
        self.rand_sample = np.array(self.df[statistic].sample(N))

        start = time.perf_counter_ns()

        if sorting_alg == "MergeSort":
            # the mergesort implementation is actually timsort
            self.rand_sample = np.sort(self.rand_sample,kind = 'mergesort') 
        else:
            self.rand_sample = np.sort(self.rand_sample, kind = 'quicksort')

        end = time.perf_counter_ns()

        return end - start

    def histogram(self):
        """
        input:
        output:
            Popoup window
        purpose:
            Creates histogram with data in member veriable, rand_sample
        """

        plt.style.use('seaborn-deep')
        
        if len(self.rand_sample) != 1:
            data_range = self.rand_sample[-1] - self.rand_sample[0]
            hist_bins = int(data_range/5)
        else:
            hist_bins = 5

        return self.rand_sample, hist_bins 

    def report(self):
        """
        input:
        output:
            @returns a list containing 5 values:
                mean, median, std_variation, max, and min.
        purpose:
            Calculate statistics for random sample of data.
        """
        mean = np.nanmean(self.rand_sample)
        median = np.nanmedian(self.rand_sample)

        # std_var = sqrt(variance)
        std_variation = math.sqrt(np.nanvar(self.rand_sample))

        max_val = self.rand_sample[-1]
        min_val = self.rand_sample[0]

        return mean, median, std_variation, max_val, min_val

    def print_columns(self):
        print(self.df.keys())
        print(len(self.df["H"]))

    def zScore(self):
        """
        input:
            @takes in the data from the loaded csv file
        output:
            @returns a list containing 5 values:
                returns a z score and places it on to the screen using the check box command option
        purpose:
            Calculate statistics(z score(normalize data)) for random sample of data.
        """
        mean = np.nanmean(self.rand_sample)
        std_variation = math.sqrt(np.nanvar(self.rand_sample))
        for i in self.data[statistics]:
            normalize = (i-mean)/std_variation

        

        return z

"""
x = Data("C:\Kevin\Code\COP3530-Final-Project\Project Code\Data\Batting.csv")
print(x.sample("SO", 10000))
x.histogram()

for i in x.report():
    print(i, end = " ")
"""