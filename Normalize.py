import numpy as np

def normalize(data):
	""" 
	Normalize 2D array. Variance = 1;
	:input: 2D floats data array.
	:return: The normalized 2D floats array.
   	:return type: numpy.ndarray """
	
	Min = np.min(data)
	Max = np.max(data)
	
	for i in range(len(data)):
		for j in range(len(data.transpose())):
			data[i,j] = (data[i,j] - Min) / (Max - Min)
	return data