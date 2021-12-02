import numpy as np

a = [1,1,2,2]
b = [1,2]

print([a[i] for i in range(len(a)) if a[i] not in b[i:]])


def removeFromList(original, removables):
    #return [i for i in original if i not in removables]
    #a helper function that sorts an arrayLike and then searches for a val, if found returns the index, otherwise returns None
    def sort_n_search(arrayLike, val):
        sortedArrayLike = np.sort(arrayLike)
        insertionIndex = np.searchsorted(sortedArrayLike, val)
        if insertionIndex >= len(sortedArrayLike) or sortedArrayLike[insertionIndex] != val:
            return None
        else:
            return insertionIndex

    removables = removables.copy() #we don't want to alter the original object so we get a copy
    original = np.sort(original)  #sort the original list
    returnMe = [] #where we will accumulate values not in removables

    #for each value, i, in original, add only so many instances to returnMe as do not exist in removables - i.e. removeFromList([1,1], [1]) returns [1] - kind of like a set difference, but with duplicates
    j = 0
    for i in range(len(original)):
        if sort_n_search(removables[j:], original[i]) == None:
            returnMe.append(original[i])
        else: j+=1
    return np.asarray(returnMe)

print(removeFromList(a,b))
