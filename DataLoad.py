import numpy as np
import glob
import wfdb

#import matplotlib.pyplot as plt
#import math


#import scipy.stats
#import scipy.signal

def fload(FileNames, WinSize):
	"""Input Arguments:
		FILENAMES - pointer to the directory and files
	Output Arguments:
	
	Example:
	X, Y = DataLoad.fload(FileNames='RowData/*.dat', Winsize=10)
	"""
	#Some necessary settings 
	SigSize = WinSize * 360	
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
				if item not in "~+N/fQ?()ptu'sT*D=@":
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

	return X[1:,:], Y[1:,:]
	
	
#	
#def sshow(S):
#	"""Displaying first 3 EEG signals with index A1-LE.
#	Displaying only if [Signal] is not an empty array"""
#	m = 1.2 #multiplyer for plot y limits
#	#print(S.shape)
#	plt.figure(1)
#	
#	if S.any():
#		Sig_length = len(S.transpose())
#		
#		ax1 = plt.subplot(3, 1, 1)
#		ax1.plot(range(Sig_length), S[0,:])
#		ax1.set_ylim([np.min(S[0:2,:])*m, np.max(S[0:2,:])*m])
#		ax1.set_title('First three EEG signals (A1-LE)')
#		ax1.xaxis.set_visible(False)
#		
#		ax2 = plt.subplot(3, 1, 2)
#		ax2.plot(range(Sig_length), S[1,:])
#		ax2.set_ylim([np.min(S[0:2,:])*m, np.max(S[0:2,:])*m])
#		ax2.xaxis.set_visible(False)
#		
#		ax3 = plt.subplot(313)
#		ax3.plot(range(Sig_length), S[2,:])
#		ax3.set_ylim([np.min(S[0:2,:])*m, np.max(S[0:2,:])*m])
#		plt.show
#		
#	else:
#		print('\n Nothing to show. Array is empty :( \n')
#
#def cuton(S, WinSize = 100):
#	#WinSize = int(WinSize)
#	Pices = int(math.ceil(len(S.transpose()) / WinSize) - 1)
#	
##	print(Pices)
##	print(WinSize)
##	print(len(S))
#	CutSig = np.empty((len(S), Pices, WinSize))
#	
#	for i in range(len(S)):
#		for j in range(Pices):
#			CutSig[i,j,:] = np.array(S[i, j*WinSize:(j+1)*WinSize])
#	
#	return CutSig
#						
#def cutshow(Sig, N = 1):
#	
#	S_merge = np.concatenate((Sig[N,0,:], Sig[N,1,:], Sig[N,2,:]))
#	Ymin = np.min(S_merge) * 1.1
#	Ymax = np.max(S_merge) + np.abs(np.max(S_merge) * 0.1)
#
#	plt.figure(2)
#
#	ax1 = plt.subplot(2, 3, 1)
#	ax1.plot(range(len(Sig[N,0,:])), Sig[N,0,:])
#	ax1.set_ylim([Ymin, Ymax])
#	ax1.xaxis.set_visible(False)
#	
#	ax2 = plt.subplot(2, 3, 2)
#	ax2.plot(range(len(Sig[N,1,:])), Sig[N,1,:])
#	ax2.set_ylim([Ymin, Ymax])
#	ax2.xaxis.set_visible(False)
#	ax2.yaxis.set_visible(False)
#	
#	ax3 = plt.subplot(2, 3, 3)
#	ax3.plot(range(len(Sig[N,2,:])), Sig[N,2,:])
#	ax3.set_ylim([Ymin, Ymax])
#	ax3.xaxis.set_visible(False)
#	ax3.yaxis.set_visible(False)
#
#	
#	ax4 = plt.subplot(2, 1, 2) #here - connected signal
#	ax4.plot(range(len(S_merge.transpose())), S_merge)
#	ax4.set_ylim([Ymin, Ymax])
#	ax4.set_xlim([0, len(S_merge.transpose())])
#	ax4.xaxis.set_visible(True)
#	
#	plt.show