import numpy as np
import wfdb
import glob
import Normalize

def nload(Patients=(1,10), Winsize=120, Fs=360, Norm=True):
	"""
	Function read a WFDB record from 'http://physionet.org/physiobank/database/mitdb'
		
	Input Arguments:
		PATIENTS (tuple) - pointer to the directory and files;
		WINSIZE (int) - size of the chunks of input signal in sec;
		FS (int) - frequency in Hz;
		NORM (binary) - normalize input signal or not;
		
	Output Arguments:
		X - Array of the input data for further analysis
		Y - Keys (labels) for classification
	Example:
	X, Y = DataLoad.fload(FileNames='RowData/*.dat', Winsize=10)
	"""
	#Filenames in db: 100-124, 200-234	
	namelist = np.concatenate((np.arange(100,110), np.arange(111,120)))
	namelist = np.concatenate((namelist, np.arange(121,125)))
	namelist = np.concatenate((namelist, np.arange(200,204)))
	namelist = np.concatenate((namelist, np.arange(205,206)))
	namelist = np.concatenate((namelist, np.arange(207,211)))
	namelist = np.concatenate((namelist, np.arange(212,216)))
	namelist = np.concatenate((namelist, np.arange(217,218)))
	namelist = np.concatenate((namelist, np.arange(219,224)))
	namelist = np.concatenate((namelist, np.arange(228,229)))
	namelist = np.concatenate((namelist, np.arange(230,235)))
	
	SigSize = Winsize * Fs
	
	X = np.array(np.zeros([SigSize])) 
	Y = np.array(np.zeros([1]))	
	
	IsNormal = 1
	FirstAnn = 0
	
	for item in np.arange(Patients[0]-1, Patients[1]):
		# here we read files from web
		fname = str(namelist[item])
		
		
		
		print('reading: ' + fname + '.dat')
		sig, fields = wfdb.srdsamp(fname, pbdir='mitdb', channels=[0])
		annotation = wfdb.rdann(fname, 'atr', pbdir='mitdb')
		
		# here we stack pieces of a readed signal
		SigStart = 0	
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
			
			if IsNormal >= 1:
				Y = np.vstack([Y, 1])
			else:
				Y = np.vstack([Y, 0])
				
			#Y = np.vstack([Y, lambda x: 1 if IsNormal >= 0 else 0])
				
			IsNormal = 1
			SigStart += SigSize
			
	if Norm == True:
		X = Normalize.normalize(X)
	print('\n')
	return X[1:,:], Y[1:,:]	
	
def fload(FileNames, WinSize, Fs, AllowMistakes=0, Norm=True):
	"""
	Function for reading .atr and .dat files from the local disc
	
	Input Arguments:
		FILENAMES (str) - pointer to the directory and files;
		WINSIZE (int) - size of the chunks of input signal in sec;
		FS (int) - frequency in Hz;
		ALLOWMISTAKES (int) - how much mistakes we are ready to ignore;
		NORM (binary) - normalize input signal or not;
		
	Output Arguments:
		X - Array of the input data for further analysis
		Y - Keys (labels) for classification
		annotation
	Example:
	X, Y = DataLoad.fload( FileNames='TrainData/*.dat', 
					  WinSize=winsize, 
					  Fs=freq,
					  AllowMistakes=allowmistakes,
					  Norm=True))
	"""
	#Some necessary settings 
	SigSize = WinSize * Fs	
	X = np.array(np.zeros([SigSize])) 
	Y = np.array(np.zeros([1]))
	IsNormal = 1
	FirstAnn = 0
	print('\n\t\t', FileNames)
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
	
	if Norm == True:
		X = Normalize.normalize(X)
	
	return X[1:,:], Y[1:,:], annotation
