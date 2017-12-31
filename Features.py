# -*- coding: utf-8 -*-
"""
Created on Wed Oct 25 21:45:40 2017
@author: max
"""
import numpy as np
import math
from scipy import signal
import scipy
import matplotlib.pyplot as plt


def normalization(data):
	"""
	Normalize 2D array. Mean = 0; Variance = 1;
	:param data: 2D floats data array.
	:type data: numpy.ndarray

	:return: The normalized 2D floats array.
   	:rtype: numpy.ndarray
	"""
	mean = np.mean(data)
	var = 0
	
	for i in range(len(data)):
	    for j in range(len(data.transpose())):
						data[i,j] = data[i,j] - mean
	var = sum(sum(data ** 2)) 
	var =  math.sqrt(var / data.size)
	
	data = data / var
	
	return data

def betaindex(data, DiscFreq, f1=30, f2=47, f3=11, f4=21):
	""" Calculating Beta index of a list of signals:
	default for EEG formula: log (E(30-47) / E(11-21))
	:param data: 2D floats data array.
	:type data: numpy.ndarray

	:return: one column vector with Beta index 
   	:rtype: numpy.ndarray """
	BetaIndex = np.empty(len(data))
	MagicCoef = int(len(data[1,:]) / DiscFreq)
	
	for i in range(len(data)):
		f, PowDen = signal.periodogram(data[i,:], DiscFreq)
		BetaIndex[i] = math.log(
			np.sum(PowDen[int(f1*MagicCoef) : int(f2*MagicCoef)]) / 
			np.sum(PowDen[int(f3*MagicCoef) : int(f4*MagicCoef)]))
	
	return BetaIndex

def snr(data):
	""" Calculation Signal to noise ratio 
	(the mean divided by the standard deviation)
	
	:param data: 2D floats data array.
	:type data: numpy.ndarray
	:return: one column vector with SNR 
   	:rtype: numpy.ndarray """
				
	SNR = scipy.stats.signaltonoise(data, axis=1)
	MeanSNR = np.mean(SNR)
	SNR[SNR > MeanSNR] = MeanSNR
	return SNR
	
def sigenergy(data, DiscFreq, FullSig = False, f1 = 30, f2 = 47):
	""" Calculating energy of a signal in noticed band (f1-f2):
	FULLSIG = True: calculation of the total energy of a signal
	
	:param data: 2D floats data array.
	:type data: numpy.ndarray

	:return: one column vector with Beta index 
   	:rtype: numpy.ndarray """
				
	energy = np.empty(len(data))
	DominantFreq = np.empty(len(data))
	
	MagicCoef = len(data[1,:]) / DiscFreq
	
	if FullSig == True:
		for i in range(len(data)):
			f, energy[i] = signal.periodogram(data[i,:], DiscFreq)
			DominantFreq[i] = np.argmax(energy) / MagicCoef
	else:
		for i in range(len(data)):
			f, PowDen = signal.periodogram(data[i,:], DiscFreq)
			energy[i] = np.sum(PowDen[int(f1*MagicCoef) : int(f2*MagicCoef)])
	
	return energy
