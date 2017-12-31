import numpy as np
np.random.seed(666)  # for reproducibility

import glob
import wfdb

def fload(FileNames, WinSize, fs, AllowMistakes=1):
	"""
	Function for reading .atr and .dat files from the physiobank databases
	
	Input Arguments:
		FILENAMES - pointer to the directory and files
		WINSIZE - size of the chunks of input signal in sec.
		
	Output Arguments:
		X - Array of the input data for further analysis
		Y - Keys (labels) for classification
	Example:
	X, Y = DataLoad.fload(FileNames='RowData/*.dat', Winsize=10)
	"""
	#Some necessary settings 
	SigSize = WinSize * fs	#For frequency of a signal f=360Hz
	X = np.array(np.zeros([SigSize])) 
	Y = np.array(np.zeros([1]))
	IsNormal = 1
	FirstAnn = 0
	
	#Here we one-by-one computing all the files
	for filename in glob.glob(FileNames):
		SigStart = 0		
		recname = filename.split(".")
		print(filename)
		
		#reading annotation and data from file
		sig, fields = wfdb.srdsamp(recname[0], channels = [0])
		annotation = wfdb.rdann(recname[0], 'atr')
		
		#Cuting and stacking into the X array all the short picies
		Iterrations = np.arange(int(sig.size/SigSize))
		for Item in Iterrations-1:
			
			#Chunk to append to X vector			
			NextChunk = sig[SigStart: SigStart+SigSize]
			NextChunk = NextChunk.T[0]
			
			#Appending chunk to X
			X = np.vstack([X, NextChunk])
			
			
			#Finding samples for Y vector
			LastAnn = np.max(np.where(annotation.sample < SigStart+SigSize)[0])
			if SigStart is not 0:
				FirstAnn = np.max(np.where(annotation.sample < SigStart)[0])
				
			#Checking - is our annotation symbols are ok
			for item in annotation.symbol[FirstAnn:LastAnn]:
				if item not in "~+.N/|fQ?()ptu^'`sT*D=@":
					IsNormal -= 1
			# If annotation symbols are ok - stack to Y 'one'
			
			if IsNormal >= 1 - AllowMistakes:
				Y = np.vstack([Y, 1])
			else:
				Y = np.vstack([Y, 0])
				
			#Y = np.vstack([Y, lambda x: 1 if IsNormal >= 0 else 0])
				
			IsNormal = 1
			SigStart += SigSize
	
	#print(annotation.symbol[:100])
	#annotation.sample
	#annotation.symbol
	return X[1:,:], Y[1:,:], annotation

def Shuffle(X, Y, Percent=30):
	"""
	Function for shuffling data  .atr and .dat files from the physiobank databases
	
	Input Arguments:
		X - input dataset
		Y - keys(classes) for input dataset
		Percent - How much persent of input data gonna be in test set
		
	Output Arguments:
		X_train - data for training 
		X_test - data for testing
		Y_train - keys(classes) for training
		Y_test - keys(classes) for testing
		
	Example:
	X_train, X_test, Y_train, Y_test = DataLoad.Shuffle(X, Y, Percent=30)
	"""
	n_all = X.shape[0]
	n_test = int(n_all * (Percent/100))
	
	X_s = np.arange(n_all)
	np.random.shuffle(X_s)
	
	X_tr = X_s[n_test:]
	X_te = X_s[:n_test]
	
	X_train = X[X_tr,:]
	X_test = X[X_te,:]
	
	Y_train = Y[X_tr,:]
	Y_test = Y[X_te,:]
	
	return X_train, X_test, Y_train, Y_test 