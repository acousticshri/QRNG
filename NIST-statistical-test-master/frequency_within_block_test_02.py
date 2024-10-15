import math
import scipy.special as ss
from fractions import Fraction

def test(input):
    # Compute number of blocks M = block size. N=num of blocks
    # N = floor(n/M)
    # miniumum block size 20 bits, most blocks 100
    # fieldnames = ['number','chisq','p-value', 'success']
    ones = input.count('1')  # number of ones
    zeroes = input.count('0')  # number of zeros

    n = ones + zeroes
    M = int(0.01 * n)  # Ensure M is an integer
    N = int(math.floor(n / M))  # Calculate number of blocks

    if N > 99:
        N=99
        M = int(math.floor(n/N))

    if n < 100:
        # Too little data for test. Input of length at least 100 bits required
        return [0.0, 0.0, False]

    num_of_blocks = N

    block_size = M 

    proportions = list()

    for i in range(num_of_blocks):
        
        block = input[i*(block_size):((i+1)*(block_size))]
        
        ones = block.count('1')

        zeroes = block.count('0') 
        
        proportions.append(Fraction(ones,block_size))

    chisq = 0.0

    for prop in proportions:
        chisq += 4.0*block_size*((prop - Fraction(1,2))**2)
    
    p = float(ss.gammaincc((num_of_blocks/2.0),float(chisq)/2.0)) # p-value
    
    success = (p>= 0.01)

    return [p, success]
