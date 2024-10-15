import os
import sys
import matplotlib.pyplot as plt
from tabulate import tabulate

# Import individual tests
sys.path.append('C:/Users/Rajat/Desktop/Project/Python Project/NIST-statistical-test-master/')
from monobit_test_01 import test as monobit_test
from frequency_within_block_test_02 import test as frequency_block_test
from runs_test_03 import test as runs_test
from longest_run_ones_in_a_block_test_04 import test as longest_ones_run_test
from binary_matrix_rank_test_05 import test as binary_matrix_rank_test
from dft_test_06 import test as dft_test
from non_overlapping_template_matching_test_07 import test as non_overlapping_test
from overlapping_template_matching_test_08 import test as overlapping_test
from maurers_universal_test_09 import test as maurers_test
from linear_complexity_test_10 import test as linear_complexity_test
from serial_test_11 import test as serial_test
from approximate_entropy_test_12 import test as app_entropy_test
from cumulative_sums_test_13 import test as cumulative_sums_test
from random_excursion_test_14 import test as random_excursion_test
from random_excursion_variant_test_15 import test as random_excursion_variant_test


def read_bits_from_file(filename):
    """Reads a file containing a sequence of bits and returns it as a string."""
    with open(filename, 'r') as file:
        data = file.read().strip()
    if not all(bit in '01' for bit in data):
        raise ValueError("Input file contains invalid characters. Only '0' and '1' are allowed.")
    return data


def run_nist_tests(bit_sequence):
    """Runs all the NIST tests on the given bit sequence and returns only p-values."""
    results = {}
    results['Monobit Test'] = monobit_test(bit_sequence)
    results['Frequency within Block Test'] = frequency_block_test(bit_sequence)
    results['Runs Test'] = runs_test(bit_sequence)
    results['Longest Run of Ones in a Block'] = longest_ones_run_test(bit_sequence)
    results['Binary Matrix Rank Test'] = binary_matrix_rank_test(bit_sequence)
    results['DFT Test'] = dft_test(bit_sequence)
    results['Non Overlapping Template Matching Test'] = non_overlapping_test(bit_sequence)
    results['Overlapping Template Matching Test'] = overlapping_test(bit_sequence)
    results['Maurers Universal Test'] = maurers_test(bit_sequence)
    results['Linear Complexity Test'] = linear_complexity_test(bit_sequence)
    results['Serial Test'] = serial_test(bit_sequence)
    results['Approximate Entropy Test'] = app_entropy_test(bit_sequence)
    results['Cumulative Sums Test'] = cumulative_sums_test(bit_sequence)
    results['Random Excursion Test'] = random_excursion_test(bit_sequence)
    results['Random Excursion Variant Test'] = random_excursion_variant_test(bit_sequence)

    return results


def plot_results(test_results):
    """Plots the p-values of the NIST tests with their corresponding test names and prints a table."""
    test_names = list(test_results.keys())
    p_values = list(test_results.values())

    # Tabulate the results
    table_data = [(name, p_value) for name, p_value in zip(test_names, p_values)]
    headers = ["Test Name", "P-Value"]

    # Print the table
    print(tabulate(table_data, headers=headers, tablefmt="grid"))

    # Plot the p-values
    plt.figure(figsize=(10, 6))
    plt.barh(test_names, p_values, color='blue')
    plt.xlabel('P-Value')
    plt.title('NIST Statistical Test P-Values')
    plt.show()


def process_file(input_file):
    """Processes a file and returns the results of the NIST tests."""
    print(f"Debug: input_file type is {type(input_file)}")

    if not isinstance(input_file, str):
        raise TypeError("The input file path should be a string.")

    if not os.path.exists(input_file):
        raise FileNotFoundError(f"File '{input_file}' not found.")

    try:
        bit_sequence = read_bits_from_file(input_file)
    except ValueError as e:
        raise ValueError(f"Error reading bits from file: {e}")

    return run_nist_tests(bit_sequence)


def process_bit_sequence(bit_sequence):
    """Processes a bit sequence directly and returns the results of the NIST tests."""
    if not isinstance(bit_sequence, str):
        raise TypeError("The bit sequence should be a string.")

    return run_nist_tests(bit_sequence)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python nist_test_framework.py <input_file>")
        sys.exit(1)

    input_file = sys.argv[1]

    try:
        # Process the file and get the results
        test_results = process_file(input_file)

        # Plot the results and print a table
        plot_results(test_results)

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
