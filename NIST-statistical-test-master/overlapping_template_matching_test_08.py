import os
import math
import scipy.special as ss


def lgamma(x):
    return math.log(ss.gamma(x))


def Pr(u, eta):
    if u == 0:
        p = math.exp(-eta)
    else:
        sum_prob = 0.0
        for l in range(1, u + 1):
            sum_prob += math.exp(-eta - u * math.log(2) + l * math.log(eta)
                                 - lgamma(l + 1) + lgamma(u) - lgamma(l) - lgamma(u - l + 1))
        p = sum_prob
    return p


def test(input_bits, blen=6):
    ones = input_bits.count('1')  # Number of ones
    zeroes = input_bits.count('0')  # Number of zeros
    n = ones + zeroes

    m = 10  # Template length
    N = 968  # Number of blocks as specified in SP800-22rev1a
    K = 5  # Number of degrees of freedom
    M = 1032  # Length of each block as specified in SP800-22rev1a

    # Check if the input bit length is sufficient
    if len(input_bits) < (M * N):
        print(f"Error: Input bit sequence too short! Length provided: {len(input_bits)}, required: {M * N}")
        return [0] * 12

    blocks = []
    for i in range(N):
        block = [int(bit) for bit in input_bits[i * M:(i + 1) * M]]
        blocks.append(block)

    # Template B as a list of 1s of length `m`
    B = [1] * m

    # Count the distribution of matches of the template across blocks: Vj
    v = [0] * (K + 1)
    for block in blocks:
        count = 0
        for position in range(M - m + 1):
            if block[position:position + m] == B:
                count += 1
        if count >= K:
            v[K] += 1
        else:
            v[count] += 1

    # Chi-square calculation
    pi = [0.364091, 0.185659, 0.139381, 0.100571, 0.0704323, 0.139865]  # From STS
    piqty = [int(x * N) for x in pi]

    lambd = (M - m + 1.0) / (2.0 ** m)
    eta = lambd / 2.0
    sum_prob = 0.0
    for i in range(K):  # Compute Probabilities
        pi[i] = Pr(i, eta)
        sum_prob += pi[i]

    pi[K] = 1 - sum_prob

    chisq = 0.0
    for i in range(K + 1):
        if N * pi[i] > 0:
            chisq += ((v[i] - (N * pi[i])) ** 2) / (N * pi[i])

    p = float(ss.gammaincc(5.0 / 2.0, chisq / 2.0))  # Compute p-value

    success = (p >= 0.01)
    return [p, success]