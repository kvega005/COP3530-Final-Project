from matplotlib import pyplot as plt 

import pandas as pd
import numpy as np
import random

# https://pandas.pydata.org/pandas-docs/stable/user_guide/10min.html
# For creating data frame

class Data:
    def __init__(self, path):
        self.df = pd.read_csv(path)
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
        self.rand_sample = np.array(self.df[statistic].sample(N))
        self.rand_sample = self.rand_sample[self.rand_sample != 0]

    def histogram(self):
        plt.hist(self.rand_sample, bins = sorted(self.rand_sample))
        plt.show()

x = Data("C:\Kevin\Code\COP3530-Final-Project\Project Code\Data\Batting.csv")
x.sample("AB", 1000)
x.histogram()