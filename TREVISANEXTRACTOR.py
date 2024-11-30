import time
import numpy as np
from random import choices
import galois
from bitarray import bitarray

"""
Function Definitions
"""


def GFpow(x, y):  # Perform power operation using multiplication
    if y == 0:
        return x ** y
    else:
        a = x
        for i in range(y - 1):
            x = x * a
        return x


def inttobit(x):  # Convert an integer to binary (big-endian)
    if x > 0:
        return [x // 2 ** k % 2 for k in range(int(np.floor(np.log2(x)) + 1))]
    if x == 0:
        return [0]


def bittoint(x):  # Convert binary to an integer
    a = 0
    for i in range(len(x)):
        a = a + x[i] * 2 ** i
    return a


def WDcomputeS(i, m, t, t_req):
    GFt = galois.GF(t)  # Define the finite field GF(t)
    alf = []
    S = []
    c = int(np.ceil(np.log2(m) / np.log2(t_req) - 1))
    mask = (1 << int(np.log2(t))) - 1  # Create a bitwise mask

    # Decompose 'i' into coefficients in the finite field
    for j in range(c + 1):
        coefficient = (i & (mask << (j * int(np.log2(t))))) >> (j * int(np.log2(t)))
        alf.insert(0, GFt(coefficient))  # Convert to GF(t)

    # Compute the weak design set S_i
    for a in range(t_req):
        b = GFt(0)  # Initialize b as a Galois field element
        Sa = 0  # Standard integer for XOR operations
        a_GF = GFt(a)  # Convert `a` to GF(t)

        for j in range(c + 1):
            b += alf[-j - 1] * GFpow(a_GF, j)  # Perform Galois field addition and multiplication

        # Convert Galois field element back to integer for XOR operation
        b_int = int(b)
        Sa ^= b_int  # XOR operation with `b_int`
        Sa ^= (a << int(np.log2(t)))  # XOR operation with `a << log2(t)`
        S.append(Sa)  # Append the result to the set S

    return S



def OneBitExt(sottoseed, source, error):
    source_bitarray = bitarray(source)
    sottoseed_bitarray = bitarray(sottoseed)
    c = []
    r = 0
    n = len(source)
    l = int(np.ceil(np.log2(n) + 2 * np.log2(2 / error)))
    GF2l = galois.GF(2 ** l)  # Finite field GF(2^l)
    s = int(np.ceil(n / l))
    source = source + [0] * (s * l - n)

    for i in range(s):
        c.append(source[i * l:(i + 1) * l])

    alf = sottoseed[0:l]  # Take the first half of the seed

    for i in range(s):
        c[i] = GF2l(c[i])

    alf = GF2l(alf)

    for i in range(1, s + 1):
        r = r + c[i - 1] * GFpow(alf, (i - 1))

    r = r.integer  # Convert finite field element to integer
    b = 0  # Hadamard step: calculate parity

    for j in range(l):
        b = b ^ (sottoseed[j + l] & ((r >> j) & 1))

    return b


"""
Parameters and Constants Definition
"""
start_time = time.time()

r = 2 * np.e
n = int(input("Enter the length of the input string: "))
alpha = float(input("Enter the min-entropy of the input string: "))
eps = float(input("Enter the error per bit for the final construction: "))

k = alpha * n
m = int(np.floor((k - 4 * np.log2(1 / eps) - 6) / r))

t_req = int(2 * np.ceil(np.log2(n) + 2 * np.log2(2 / eps)))
t = int(2 ** (np.ceil(np.log2(t_req))))  # Round up to the nearest power of 2
d = t ** 2

"""
Source and Seed Input
"""
q = input("Enter the file name of the SOURCE (with .txt extension): ")
with open(q, "r") as f1:
    a = f1.read()

w = input("Enter the file name of the SEED (with .txt extension): ")
with open(w, "r") as f2:
    b = f2.read()

seed = []
source = []

for i in range(d):
    seed.append(int(b[i], 2))

for i in range(n):
    source.append(int(a[i], 2))

"""
Trevisan's Extractor Algorithm
"""

rho = [0] * m

for i in range(m):
    print(i / m * 100)
    S = WDcomputeS(i, m, t, t_req)
    b = [0] * t_req

    for j in range(t_req):
        b[j] = seed[S[j]]

    rho[i] = OneBitExt(b, source, eps)

print()
print("The output random string is:", rho)
print()
print("--- The program took %s minutes to run ---" % ((time.time() - start_time) / 60))
print()
