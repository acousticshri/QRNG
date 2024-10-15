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

    p = ss.gammaincc(5.0 / 2.0, chisq / 2.0)  # Compute p-value

    success = (p >= 0.01)
    return [p, success]


# Function to read bit sequences from a file
def read_bits_from_file(filepath):
    try:
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"File not found: {filepath}")

        with open(filepath, 'r') as file:
            content = file.read().strip()  # Read and remove leading/trailing whitespace
        # Ensure the content is composed of 0s and 1s
        bit_sequence = ''.join(filter(lambda x: x in '01', content))
        return bit_sequence
    except Exception as e:
        print(f"Error reading file {filepath}: {e}")
        return None


# Update the file paths as absolute paths
filepaths = [
    'C:/Users/Rajat/Desktop/Project/QRNG/data_clean.txt',
    'C:/Users/Rajat/Desktop/Project/QRNG/two.txt'
]

# Process each file and test the randomness
result = []
for filepath in filepaths:
    bit_sequence = read_bits_from_file(filepath)
    if bit_sequence:
        # Check the length of the bit sequence
        print(f"Testing file: {filepath}, Bit sequence length: {len(bit_sequence)}")
        result.append(test(bit_sequence))

print(result)
