import math
from collections import Counter
from scipy.stats import entropy, norm
import numpy as np

def shannon(bit_sequence):
    """
    Calculate the Shannon entropy for a sequence of bits (0 and 1).
    """
    freq_count = Counter(bit_sequence)
    total_bits = len(bit_sequence)
    # Calculate probabilities for each unique bit
    pk = [freq_count[bit] / total_bits for bit in freq_count]

    # Calculate Shannon entropy
    observed_entropy = entropy(pk, base=2)
    return observed_entropy


def calculate_p_value_from_entropy(observed_entropy, n):
    """
    Calculate a p-value for randomness based on the observed Shannon entropy.
    This approach assumes a normal approximation around the expected entropy for a large n.
    """
    # Expected entropy for a random binary sequence
    H_expected = 1.0  # since log2(2) = 1 for a 50-50 random distribution

    # Standard deviation of entropy for binary sequences, approx sqrt(1 / (2 * n))
    std_dev = math.sqrt(1 / (2 * n))

    # Compute the z-score for observed entropy
    z_score = (observed_entropy - H_expected) / std_dev

    # Calculate p-value from the z-score (two-tailed)
    p_value = 2 * (1 - norm.cdf(abs(z_score)))

    return p_value


def read_bit_sequence_from_file(filename):
    """
    Read a bit sequence from a file and return it as a string.
    """
    try:
        # Read the bit sequence from file
        with open(filename, 'r') as file:
            bit_sequence = file.read().strip()

        # Ensure the sequence only contains valid bits
        if not all(bit in '01' for bit in bit_sequence):
            raise ValueError("File contains invalid characters. Only '0' and '1' are allowed.")

        return bit_sequence

    except FileNotFoundError:
        print("File not found. Please check the filename and try again.")
        return None
    except ValueError as ve:
        print(ve)
        return None


# Main function for standalone execution
if __name__ == "__main__":
    # Input file name
    filename = input("Enter the filename or path of the bit sequence file: ")
    bit_sequence = read_bit_sequence_from_file(filename)

    if bit_sequence:
        # Calculate Shannon entropy
        entropy_value = shannon(bit_sequence)
        print(f"Shannon Entropy: {entropy_value:.7f}")

        # Calculate p-value for randomness
        p_value = calculate_p_value_from_entropy(entropy_value, len(bit_sequence))
        print(f"P-value for randomness: {p_value:.7f}")
    else:
        print("Could not process the file.")
