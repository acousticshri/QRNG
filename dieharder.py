import subprocess


def convert_bit_string_file_to_binary(input_file, output_file):
    """
    Converts a file containing bit strings ('0's and '1's) to a binary file.

    Parameters:
    input_file (str): Path to the input file containing bit strings (text file).
    output_file (str): Path to the output binary file.
    """
    with open(input_file, 'r') as infile, open(output_file, 'wb') as outfile:
        for line in infile:
            # Remove any extra spaces or newlines
            bit_string = line.strip()

            # Convert bit string to an integer and then to bytes
            byte_array = int(bit_string, 2).to_bytes((len(bit_string) + 7) // 8, byteorder='big')

            # Write the byte array to the binary file
            outfile.write(byte_array)


def run_dieharder_on_binary_file(binary_file):
    """
    Runs the Dieharder test suite on a binary file containing random bits.

    Parameters:
    binary_file (str): Path to the binary file containing random bits.

    Returns:
    str: Output from the Dieharder test suite.
    """
    try:
        # Run the dieharder test suite on the binary file
        result = subprocess.run(['dieharder', '-a', '-g', '202', '-f', binary_file],
                                capture_output=True, text=True)

        # Check if the subprocess ran successfully
        if result.returncode == 0:
            return result.stdout
        else:
            return f"Error running Dieharder: {result.stderr}"

    except Exception as e:
        return f"An error occurred: {str(e)}"


# Example usage
input_bit_string_file = 'C:/Users/Rajat/Desktop/Project/Python Project/data to test/Quantis_QRNG.txt'  # Path to the file containing bit strings
output_binary_file = 'C:/Users/Rajat/Desktop/Project/Python Project/data to test/random_bits.bin'  # Path to the binary file to be created

# Convert the bit string file to binary
convert_bit_string_file_to_binary(input_bit_string_file, output_binary_file)

# Run Dieharder on the resulting binary file
output = run_dieharder_on_binary_file(output_binary_file)
print(output)

