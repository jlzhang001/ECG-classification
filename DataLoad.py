import numpy as np
import glob
import wfdb

def fload(FileNames, WinSize, fs):
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
				if item not in "~+N/|fQ?()ptu^'`sT*D=@":
					IsNormal -= 1
			# If annotation symbols are ok - stack to Y 'one'
			if IsNormal == 1:
				Y = np.vstack([Y, 1])
			else:
				Y = np.vstack([Y, 0])
			
			IsNormal = 1
			SigStart += SigSize

	#Y = annotation
	#annotation.sample
	#annotation.symbol
	return X[1:,:], Y[1:,:], annotation
