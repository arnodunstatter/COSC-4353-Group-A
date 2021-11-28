import pandas as pd
import numpy as np
from IPython.display import display
from numpy.random import randint

d = {'col1': [1, 2], 'col2': [3, 4]}
df = pd.DataFrame(data=d)
display(df)
print(len(df.index))
