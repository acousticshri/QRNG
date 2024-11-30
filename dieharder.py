import subprocess
import argparse


def run_dieharder(input_file):
    """
    Runs the Dieharder command using WSL with the given input file.

    Args:
        input_file (str): Path to the input file.

    Returns:
        str: Output of the Dieharder test or error message.
    """
    # Dieharder command
    command = f'wsl dieharder -a -f "{input_file}"'

    try:
        # Run the command using subprocess
        result = subprocess.run(command, shell=True, text=True, capture_output=True)

        if result.returncode == 0:
            return result.stdout  # Command succeeded, return output
        else:
            return f"Error:\n{result.stderr}"  # Command failed, return error message
    except Exception as e:
        return f"Exception occurred: {str(e)}"


if __name__ == "__main__":
    # Create an argument parser for the script
    parser = argparse.ArgumentParser(description="Run Dieharder tests via WSL.")
    parser.add_argument("input_file", help="Path to the input file for Dieharder.")

    # Parse arguments
    args = parser.parse_args()
    input_file = args.input_file

    # Run the Dieharder test
    print("Running Dieharder test...")
    output = run_dieharder(input_file)
    print("Dieharder Test Output:")
    print(output)
