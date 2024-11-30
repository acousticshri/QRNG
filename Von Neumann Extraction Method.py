with open("C:/Users/Rajat/Desktop/Project/Python Project/data to test/Entangled_Photon.txt", 'r') as file:
    bits = file.read().replace('\n', '')  # Read the entire file and remove newline characters

# Convert the concatenated bits to a list of characters
bit_list = bits

# Print the result
print(len(bit_list))

output_file_path = 'data_single_row.txt'                #  making a new file to put all the extracted random numbers in separate file
with open(output_file_path, 'w') as output_file:
    output_file.write(bit_list)
    file = open("C:/Users/Rajat/Desktop/Project/Python Project/data to test/Entangled_Photon.txt", "r")  # Read the input file
    content = file.read()
    length = len(content)

    if length % 2 == 0:  # check if the length of the bits if even
        length = length
    else:
        length = length - 1

    output = []

    for i in range(0, int(length / 2)):  # Comparison of two consecutive bits
        bit_1 = content[2 * i]
        bit_2 = content[2 * i + 1]

        if bit_1 != bit_2:
            output.append(bit_1)

    result = result = ''.join(output)

    output_file_path = 'Von_Neumann_Extracted_data.txt'  # making a new file to put all the extracted random numbers in separate file
    with open(output_file_path, 'w') as output_file:
        output_file.write(result)

    file = open(output_file_path, "r")  # viewing the extracted random number
    content = file.read()
    print(len(content))