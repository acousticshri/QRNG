import scipy.special as ss

def test(input):

    ones = input.count('1')  # number of ones

    zeroes = input.count('0')  # number of zeros

    n = ones + zeroes

    M8 = [0.0882, 0.2092, 0.2483, 0.1933, 0.1208, 0.0675, 0.0727]

    # Length of blocks
    M = 10^4 # It should be 10^4
                
    K = 5

    N = 16
            
    # Table of frequencies
    v = [0,0,0,0,0,0,0] # Not sure about this

    for i in range(N): # over each block
        #find the longest run
        block = input[i*M:((i+1)*M)] # Block i
        
        run = 0
        longest = 0
        for j in range(M): # Count the bits.
            if block[j] == '1':
                run += 1
                if run > longest:
                    longest = run
            else:
                run = 0

        if longest <= 1:    v[0] += 1
        elif longest == 2:  v[1] += 1
        elif longest == 3:  v[2] += 1
        else:               v[3] += 1
    
    # Compute Chi-Sq
    chi_sq = 0.0
    for i in range(K+1):
        p_i = M8[i]
        upper = (v[i] - N*p_i)**2
        lower = N*p_i
        chi_sq += upper/lower
    # p-value
    p = float(ss.gammaincc(K/2.0, chi_sq/2.0))
    
    success = (p>=0.01)

    return [p, success]

