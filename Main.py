import matplotlib.pyplot as plt
import numpy as np
np.random.seed(666)  # for reproducibility

from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation, Flatten
from keras.layers import Convolution2D, MaxPooling2D
from keras.utils import np_utils

import DataLoad
#import Features

X, Y, annotation = DataLoad.fload(FileNames='RowData/*.dat', WinSize=10, fs=360)
print('Input data has been completely parsed and loaded!')
plt.plot(X[100,:])
plt.show()
plt.plot(X[101,:])
plt.show()
plt.plot(X[102,:])
plt.show()

print('X.shape: ', X.shape)

print('Y.shape: ', Y.shape)
print('Ok segments:', Y[Y==1].shape[0], 'from', Y.shape[0])

#print(annotation.symbol[:100])

#annotation.sample
#annotation.symbol
				
# Implement follow: (X_train, y_train), (X_test, y_test)
#instruction here: https://elitedatascience.com/keras-tutorial-deep-learning-in-python
#Task 2: arythmia detection in publications