import random
import numpy as np
import pandas as pd
from scipy.signal import hilbert
import joblib

def inrush_classifier(df):
    """
    Classify whether inrush is present in `signals`
    """
    covars = covariables(df)
    model = joblib.load('classifier.pkl')
    return model.predict(covars)[0]

def covariables (df):
    signals = df.Channel.unique()
    s1 = df[df.Channel == signals[0]].Value
    s2 = df[df.Channel == signals[1]].Value
    s3 = df[df.Channel == signals[2]].Value
    
    medians,ma_stds = [],[]

    analytic_signal1 = hilbert(s1)
    analytic_signal2 = hilbert(s2)
    analytic_signal3 = hilbert(s3)

    amplitude1 = np.abs(analytic_signal1)
    amplitude2 = np.abs(analytic_signal2)
    amplitude3 = np.abs(analytic_signal3)

    amp_nor1 = amplitude1/np.max(amplitude1)
    amp_nor2 = amplitude2/np.max(amplitude2)
    amp_nor3 = amplitude3/np.max(amplitude3)

    medians.append(np.median(amp_nor1))
    medians.append(np.median(amp_nor2))
    medians.append(np.median(amp_nor3))
    # Moving Average
    mov_avg1 = np.convolve(s1, np.ones(50)/50, mode='valid')
    mov_avg1 = mov_avg1/np.max(mov_avg1)
    mov_avg2 = np.convolve(s2, np.ones(50)/50, mode='valid')
    mov_avg2 = mov_avg1/np.max(mov_avg2)
    mov_avg3 = np.convolve(s3, np.ones(50)/50, mode='valid')
    mov_avg3 = mov_avg1/np.max(mov_avg3)

    ma_stds.append(np.std(mov_avg1))
    ma_stds.append(np.std(mov_avg2))
    ma_stds.append(np.std(mov_avg2))
    max_median = max(medians)
    ma_min_std = min(ma_stds)

    return pd.DataFrame({'max_median': [max_median], 'ma_min_std': [ma_min_std]})