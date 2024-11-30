import math
import time
import numpy as np

# Helper Functions: MAX function to find the maximum of two values
def MAX(a, b):
    return a if a > b else b

# Function for weak design (example, placeholder for actual functionality)
def wd(m, t, t_req, S):
    for i in range(m):
        S[i] = np.random.randint(0, t_req, t_req)

# Function for block weak design (example, placeholder for actual functionality)
def bwd(m, t, t_req, S):
    for i in range(m):
        S[i] = np.random.randint(0, t_req, t_req)

# Function for one-bit extractor (example, placeholder for actual functionality)
def one_bit_ext(b, source, n, eps, poly_irr):
    # Placeholder function logic
    return np.random.choice([True, False])

def main():
    # Initialize variables
    r = 0
    eps = 0
    alpha = 0
    t_req = 0
    t = 0
    d = 0
    n = 0
    m = 0
    l = 0
    db = 0
    r1 = 0
    S = []
    x = 0

    # File names
    word1 = input("Enter the file name of the SOURCE (with .txt extension): ")
    word2 = input("Enter the file name of the SEED (with .txt extension): ")

    # Opening files
    try:
        with open(word1, 'r') as file1, open(word2, 'r') as file2, open("polinomi_irriducibili.txt", 'r') as file3:
            # Ask for alpha
            while True:
                alpha = float(input("Enter the min-entropy per bit of source (double): "))
                if 0 < alpha <= 1:
                    break
                print("Error: the min-entropy per bit of source must be a number between 0 and 1 (inclusive).")

            # Ask for epsilon
            while True:
                eps = float(input("Enter the desired error (double): "))
                if 0 < eps <= 1:
                    break
                print("Error: the desired error must be a number between 0 and 1 (inclusive).")

            # Weak design selection
            while True:
                x = int(input("Enter the weak design type (0 for standard, 1 for block): "))
                if x in [0, 1]:
                    break
                print("Error: enter 0 or 1.")

            r = 2 * math.e if x == 0 else 1

            # Getting the size of the source file
            file1.seek(0, 2)
            n = file1.tell()
            file1.seek(0, 0)

            k = alpha * n
            m = math.floor((k - 4 * math.log2(1 / eps) - 6) / r)
            t_req = 2 * math.ceil(math.log2(n) + 2 * math.log2(2 / eps))
            t = 2 ** math.ceil(math.log2(t_req))
            d = t ** 2
            r1 = 2 * math.e
            l = MAX(1, math.ceil((math.log2(m - r1) - math.log2(t_req - r1)) / (math.log2(r1) - math.log2(r1 - 1))))
            db = d * (l + 1)

            if m < 1:
                print("Error: the random output string length is < 1. Change your parameters.")
                return

            # Reading source and seed
            source = np.array([int(bit) for bit in file1.read().strip()], dtype=bool)
            seed = np.array([int(bit) for bit in file2.read().strip()], dtype=bool)
            if x == 0 and len(seed) < d:
                print(f"Error: seed's bit length is smaller than expected ({d} bits).")
                return
            elif x == 1 and len(seed) < db:
                print(f"Error: seed's bit length is smaller than expected ({db} bits).")
                return

            # Reading irreducible polynomials
            poly_irr = np.array([[int(bit) for bit in line.strip()] for line in file3.readlines()], dtype=bool)

            S = np.zeros((m, t_req), dtype=int)
            if x == 0:
                wd(m, t, t_req, S)
            else:
                bwd(m, t, t_req, S)

            rho = np.zeros(m, dtype=bool)
            start_time = time.time()

            for i in range(m):
                b = seed[S[i]]
                rho[i] = one_bit_ext(b, source, n, eps, poly_irr)

            # Writing results to files
            output_filename = f"random_output_string_{'WD' if x == 0 else 'BWD'}_{word1}"
            with open(output_filename, 'w') as output_file:
                output_file.write(''.join(map(str, rho.astype(int))))

            other_data_filename = f"other_data_{'WD' if x == 0 else 'BWD'}_{word1}"
            with open(other_data_filename, 'w') as other_data_file:
                other_data_file.write(f"The source length is: {n}\n")
                other_data_file.write(f"The random output string length is: {m}\n")
                other_data_file.write(f"The seed length required is: {d if x == 0 else db}\n")
                other_data_file.write(f"Execution time for the extraction is {time.time() - start_time:.3f} seconds.\n")

            print(f"The random output string length is: {m}")
            print(f"The random output string is: {''.join(map(str, rho.astype(int)))}")
            print(f"Execution time: {time.time() - start_time:.3f} seconds")

    except FileNotFoundError as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    main()
