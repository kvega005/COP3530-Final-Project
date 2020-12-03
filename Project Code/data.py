from matplotlib import pyplot as plt 

import pandas as pd
import numpy as np
import random
import time

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

    def sample(self, statistic, N, mergeSort = False):
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

        start = time.perf_counter()

        if mergeSort:
            # the mergesort implementation is actually timsort
            self.rand_sample = np.sort(self.rand_sample,kind = 'mergesort') 
        else:
            self.rand_sample = np.sort(self.rand_sample, kind = 'quicksort')

        end = time.perf_counter()

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
        
        data_range = self.rand_sample[-1] - self.rand_sample[0]
        hist_bins = int(data_range/5)

        plt.hist(self.rand_sample, bins = hist_bins ,alpha = 0.5, label = "H")
        plt.legend(loc='upper right')
        return plt

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

        std_variation = np.nanvar(self.rand_sample)

        max_val = self.rand_sample[-1]
        min_val = self.rand_sample[0]

        return mean, median, std_variation, max_val, min_val

    def print_columns(self):
        print(self.df.keys())
        print(len(self.df["H"]))
        
x = Data("C:\Kevin\Code\COP3530-Final-Project\Project Code\Data\Batting.csv")
print(x.sample("SO", 10000))
x.histogram()

for i in x.report():
    print(i, end = " ")