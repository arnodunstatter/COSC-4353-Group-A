import pandas as pd
import numpy as np
from IPython.display import display
from numpy.random import randint
import algorithms

def sort_n_search(arrayLike, val):
    sortedArrayLike = np.sort(arrayLike)
    insertionIndex = np.searchsorted(sortedArrayLike, val)
    if insertionIndex >= len(sortedArrayLike) or sortedArrayLike[insertionIndex] != val:
        return None
    else:
        return insertionIndex

def removeFromList(original, removables):
    removables = removables.copy()
    original = np.sort(original)
    returnMe = []
    for i in original:
        if sort_n_search(removables, i) == None:
            returnMe.append(i)
        else:
            del removables[sort_n_search(removables, i)]
    return np.asarray(returnMe)

destWeights =[1,1]
weights = [1]

newDestWeights = removeFromList(destWeights, weights)
print("newDestWeights: ", newDestWeights)
print("weights after pass to removeFromList: ", weights)
