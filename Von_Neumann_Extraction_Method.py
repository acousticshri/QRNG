def extract_and_process_bits(bit_sequence):
    # Use the input bit sequence directly
    bit_list = bit_sequence.replace('\n', '')  # Remove newline characters if any

    # Print the length of the bit list
    print(f"Length of bit list: {len(bit_list)}")

    # Define the output data (no file output in this case)
    output = []

    # Ensure the length is even for pairing
    length = len(bit_list)
    if length % 2 != 0:
        length -= 1  # Make the length even for pairing

    # Comparison of two consecutive bits
    for i in range(0, int(length / 2)):
        bit_1 = bit_list[2 * i]
        bit_2 = bit_list[2 * i + 1]

        if bit_1 != bit_2:
            output.append(bit_1)

    # Join the output bits
    result = ''.join(output)

    # Print the preview (first 1000 bits) of the extracted data
    preview_length = min(1000, len(result))
    print(f"Preview of the first 1000 bits (or total length if shorter):\n{result[:preview_length]}")

    print(f"Length of extracted Von Neumann data: {len(result)}")

    # Return the processed Von Neumann data
    return result
