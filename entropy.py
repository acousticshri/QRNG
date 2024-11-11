import math
from collections import Counter


def shannon(bit_sequence):
    """
    Calculate the Shannon entropy for a sequence of bits (0 and 1).
    """
    freq_count = Counter(bit_sequence)
    total_bits = len(bit_sequence)

    # Calculate entropy
    entropy = 0
    for bit in freq_count:
        probability = freq_count[bit] / total_bits
        entropy -= probability * math.log2(probability)

    return entropy


def compute_p_value(entropy, max_entropy=1.0):
    """
    Compute the p-value based on the entropy of the bit sequence.
    """
    deviation = abs(entropy - max_entropy)
    p_value = 1 - deviation
    return max(0, min(1, p_value))


def calculate_p_value_from_sequence(bit_sequence, chunk_size=1000):
    """
    Calculate the p-value for randomness from a bit sequence.
    Returns only the p-value.
    """
    try:
        # Ensure the sequence only contains valid bits
        if not all(bit in '01' for bit in bit_sequence):
            raise ValueError("Bit sequence contains invalid characters. Only '0' and '1' are allowed.")

        # Divide the sequence into chunks for analysis
        num_chunks = len(bit_sequence) // chunk_size
        entropies = []

        for i in range(num_chunks):
            chunk = bit_sequence[i * chunk_size: (i + 1) * chunk_size]
            entropies.append(shannon(chunk))

        # Calculate average entropy across all chunks
        avg_entropy = sum(entropies) / len(entropies)

        # Calculate and return p-value for randomness
        p_value = compute_p_value(avg_entropy)
        return p_value

    except ValueError as ve:
        print(ve)
        return None


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


# Keep the main function for standalone execution
if __name__ == "__main__":
    # Input file name
    filename = input("Enter the filename or path of the bit sequence file: ")
    bit_sequence = read_bit_sequence_from_file(filename)

    if bit_sequence:
        p_value = calculate_p_value_from_sequence(bit_sequence)
        if p_value is not None:
            print(f"P-value for randomness: {p_value:.4f}")
    else:
        print("Could not process the file.")
