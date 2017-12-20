import numpy as np
import matplotlib.pyplot as plt



import DataLoad
#import Features

X, Y = DataLoad.fload(FileNames='RowData/*.dat', WinSize=10)

plt.plot(X[100,:])
plt.show()
plt.plot(X[101,:])
plt.show()
plt.plot(X[102,:])
plt.show()


print('X.shape: ', X.shape)

print('Y.shape: ', Y.shape)

#Y.sample
#Y.symbol
#																	
##найти нейронки для тайм-сириес
#
#arythmia detection in - publications
