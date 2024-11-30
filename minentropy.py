import math
from collections import Counter


def calculate_min_entropy(bitstream):
    """
    Calculate the min-entropy of a given bitstream.

    Parameters:
    bitstream (str): Input bitstream as a string of 0s and 1s.

    Returns:
    float: Min-entropy value.
    """
    # Count the frequency of each bit pattern
    counts = Counter(bitstream)

    # Calculate the probabilities of each unique bit pattern
    total_bits = len(bitstream)
    probabilities = [count / total_bits for count in counts.values()]

    # Find the maximum probability
    max_prob = max(probabilities)

    # Calculate min-entropy
    min_entropy = -math.log2(max_prob)

    return min_entropy


if __name__ == "__main__":
    # Prompt the user to enter the file path
    file_path = input("Enter the path of the input file containing the bitstream: ")

    try:
        # Read the bitstream from the file
        with open(file_path, "r") as file:
            bitstream = file.read().strip()  # Remove any trailing whitespace

        # Validate the bitstream
        if not all(bit in "01" for bit in bitstream):
            print("Error: The file must contain a valid bitstream (only 0s and 1s).")
        else:
            # Calculate min-entropy
            min_entropy = calculate_min_entropy(bitstream)
            print(f"Min-Entropy of the bitstream: {min_entropy:.4f}")
    except FileNotFoundError:
        print("Error: The file was not found. Please check the path and try again.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
