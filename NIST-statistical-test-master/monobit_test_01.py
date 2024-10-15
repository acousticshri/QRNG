import math

def test(input):
    ones = input.count('1')  # number of ones
    zeroes = input.count('0')  # number of zeros

    s = abs(ones - zeroes)
    n = ones + zeroes

    if n == 0:
        raise ValueError("Input contains no bits.")

    p = float(math.erfc(float(s) / (math.sqrt(float(n)) * math.sqrt(2.0))))  # p-value
    success = (p >= 0.01)  # success = true if p-value >= 0.01

    return [p, success]

# Function to read bits from a file and run the test
def run_test_from_file(file_path):
    try:
        with open(file_path, 'r') as file:
            bits = file.read().strip()  # Read the file contents and strip any extra whitespace

        # Call the test function with the file contents
        result = test(bits)
        print("Test Results:", result)

    except FileNotFoundError:
        print("Error: File not found.")
    except ValueError as ve:
        print(f"Error: {ve}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


