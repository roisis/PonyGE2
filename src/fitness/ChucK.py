import numpy as np
import random


class ChucK():
    """Random Fitness funtction for Chuck GE"""
    maximise = True
    default_fitness = np.NaN
    def __call__(self, cand):
        return random.randint(0,100)