# -*- coding: utf-8 -*-
"""
Created on Thu Dec 22, 2022

@author: Numan Oezguen
"""

import os
import numpy as np
import pandas as pd
import pylab
from scipy.optimize import curve_fit

def sigmoid(x, A ,x0, k, b):
    y = A / (1 + np.exp(-k*(x-x0))) + b
    return (y)

def predict_PH(y, A, x0, k, b):
    return(x0 - np.log((A/(y-b))-1)/k)


file_name = input("Please provide the data file name (1st column = pH, 2nd column = adsorbtion ratio): ")

data = pd.read_csv(file_name, sep='\t')
xt = data.iloc[:,0].values
yt = data.iloc[:,1].values

p0 = [max(yt), np.median(xt),1,min(yt)]   #initial guess for A, x0, k, b
popt, pcov2 = curve_fit(sigmoid, xt, yt,p0, method='lm')
print('Sigmoidal function:\n\t y =  A / (1 + exp(-k*(x-x0))) + b')
print("\tA=%6.4f\tx0=%6.4f\tk=%6.4f\tb=%6.4f"%(popt[0],popt[1],popt[2],popt[3]))

x = np.linspace(min(xt), max(xt), 100)
y = sigmoid(x, *popt)

pylab.ylim(min(yt)*0.95, max(yt)*1.05)
pylab.plot(xt, yt, 'o', label='pH calibrator')
pylab.plot(x,y, label='Sigmoidal fit')
pylab.legend(loc='upper left')
pylab.xlabel('Media pH')
pylab.ylabel('Abs (590nm / Abs 520nm)')
pylab.savefig('sigmoidal_fit.png', dpi=600)
pylab.show()

#===================================================================================================
print("\n======= pH predictions based on fit =======")
abfrage = 'y'
while not( (abfrage=='n')  | (abfrage=='N') ):
    yp = input("Please provide the Absortion Ratio (range between %.3f and %.3f): "%(min(y),max(y)))
    pH = predict_PH(float(yp),popt[0],popt[1],popt[2],popt[3])
    print("Corresponding pH=%.1f"%pH)

    abfrage = input("Another absorption ratio (n/N to exit)")

