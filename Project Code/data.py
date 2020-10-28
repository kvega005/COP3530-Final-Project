from matplotlib import pyplot as plt 

import pandas as pd
import numpy as np
import random

# https://pandas.pydata.org/pandas-docs/stable/user_guide/10min.html
# For creating data frame

class Data:
    def __init__(self, path):
        self.df = pd.DataFrame.from_csv(path)
        self.sample_size = 0
        self.sample = np.array()

    def sample(self, N, statistic):
        """
        input:
            @N: sample size
            @N: statistic to be sampled
        output:
            Sets sample class variable
        purpose:
            Make random sample from Data
        """

        self.sample = random.sample(self.df[statistic], N).sort()

    def histogram():
        plt.hist(self.sample, self.sample)

x = Data("Data/Batting.csv")
x.sample("AB", 100)
x.histogram()