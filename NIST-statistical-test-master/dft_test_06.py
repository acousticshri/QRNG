import numpy as np
import math

def test(input):
    ones = input.count('1')  # number of ones

    zeroes = input.count('0')  # number of zeros

    n = ones + zeroes

    T = math.sqrt(math.log(1.0/0.05)*n) # Compute upper threshold

    N0 = 0.95*n/2.0

    write_array = [0.0,0.0,0.0,0.0]

    ts = list()             # Convert to +1,-1
    for i in range(n):
        if input[i] == '1':
            ts.append(1)
        else:
            ts.append(-1)
    ts_np = np.array(ts)

    fs = np.fft.fft(ts_np)  # Compute DFT

    mags = abs(fs)[:int(n/2)]  #Compute magnitudes of first half of sequence


    N1 = 0.0   # Count the peaks above the upper theshold

    for mag in mags:
        if mag < T:
            N1 += 1.0
    d = (N1 - N0)/math.sqrt((n*0.95*0.05)/4)
    
    # Compute the P value
    p = float(math.erfc(abs(d)/math.sqrt(2)))

    success = (p>=0.01)

    return [p, success]