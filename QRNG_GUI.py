import math
import sys
import threading
import time
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk

import matplotlib.pyplot as plt
import pandas as pd
import scipy.stats as stats
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from Von_Neumann_Extraction_Method import process_bits

# Increase the limit for integer string conversion
sys.set_int_max_str_digits(15025000)  # Adjust the value to your needs

# Importing the NIST test functions
sys.path.append('Python Project')
from nist_test_framework import process_bit_sequence


import subprocess

def run_dieharder_test(self, file_path):
    """
    Runs the dieharder.py script on the provided file and returns the output.
    """
    try:
        result = subprocess.run(
            ['python', 'dieharder.py', file_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        if result.returncode != 0:
            raise Exception(f"Error: {result.stderr.strip()}")
        return result.stdout
    except Exception as e:
        return f"Error running DieHarder test: {str(e)}"




# Importing the Shannon entropy function from the specified file
import sys
sys.path.append(r"C:\Users\Rajat\Desktop\Project\Python Project")
import entropy_2  # Assuming entropy.py contains the Shannon entropy function

from entropy_2 import shannon

def shannon_entropy(numbers):
    bit_sequence = ''.join(f'{int(num):b}' for num in numbers)
    entropy_value = shannon(bit_sequence)
    n = len(bit_sequence)
    print(f"Entropy for this sequence: {entropy_value}")
    p_value = entropy_2.calculate_p_value_from_entropy(entropy_value, n)
    return p_value, entropy_value





# Define the GUI application class
# Run the application
class QRNG_GUI(tk.Tk):
    def run_dieharder_test(self, file_path):
        """
        Runs the dieharder.py script on the provided file and returns the output.
        """
        try:
            result = subprocess.run(
                ['python', 'dieharder.py', file_path],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            if result.returncode != 0:
                raise Exception(f"Error: {result.stderr.strip()}")
            return result.stdout
        except Exception as e:
            return f"Error running DieHarder test: {str(e)}"
    def __init__(self):
        super().__init__()
        self.file_add = []  # Initialize the file_add list to store file paths
        self.title("Quantum Random Number Generator GUI")
        self.geometry("1024x768")
        self.style = ttk.Style(self)
        self.style.theme_use("clam")

        # Variables
        self.random_numbers_list = []
        self.file_names = []  # List to store file names for reference
        self.filename = tk.StringVar()

        # Progress indicator for loading/previews/tests
        self.progress = ttk.Progressbar(self, orient=tk.HORIZONTAL, length=300, mode='indeterminate')

        # Tabs
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(expand=1, fill="both")

        # File Input Tab
        self.file_input_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.file_input_tab, text="File Input")

        self.create_file_input_tab()

        # Randomness Testing Tab
        self.testing_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.testing_tab, text="Randomness Testing")

        self.create_testing_tab()

        # Extraction Tab
        self.extraction_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.extraction_tab, text="Extraction")
        self.create_extraction_tab()  # New extraction tab

        # Settings Tab
        self.settings_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.settings_tab, text="Settings")

        self.create_settings_tab()

        # Help/Documentation Tab
        self.help_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.help_tab, text="Help")

        self.create_help_tab()

    # Create the file input tab
    def create_file_input_tab(self):
        tk.Label(self.file_input_tab, text="Upload your files with quantum random numbers:").pack(pady=10)
        tk.Entry(self.file_input_tab, textvariable=self.filename, width=50).pack(pady=5)

        tk.Button(self.file_input_tab, text="Browse", command=self.load_files).pack(pady=5)
        tk.Button(self.file_input_tab, text="Preview", command=self.run_preview).pack(pady=5)

        # Add the progress bar here
        self.progress.config(mode='indeterminate')  # Set indeterminate mode
        self.progress.pack(pady=10)  # Pack the progress bar with padding

        self.preview_text = tk.Text(self.file_input_tab, height=30, width=90)
        self.preview_text.pack(pady=10)

    # Load and preview the file
    def load_files(self):
        file_paths = filedialog.askopenfilenames(title="Open Files",
                                                 filetypes=[("Text Files", ".txt"), ("CSV Files", ".csv"),
                                                            ("DAT Files", ".dat"), ("PI Files", ".pi"),
                                                            ("All Files", ".*")])
        if file_paths:
            self.clear_previous_results()
            self.random_numbers_list = []  # List to store random numbers from all files
            self.file_names = []  # List to store file names for reference

            try:
                for file_path in file_paths:
                    if file_path.endswith('.csv'):
                        data = pd.read_csv(file_path)
                        # Assuming numbers are integers in the first column
                        random_numbers = data.iloc[:, 0].astype(str).str.strip().tolist()
                    elif file_path.endswith('.txt') or file_path.endswith('.dat') or file_path.endswith('.pi'):
                        with open(file_path, 'r') as file:
                            # Read the file as a single string and remove whitespace
                            content = file.read().replace('\n', '').replace(' ', '').strip()
                            # Check if the content is already binary
                            if all(c in '01' for c in content):
                                random_numbers = list(content)  # Keep the binary data as-is
                            else:
                                # Treat as space-separated integers
                                random_numbers = list(map(int, content.split()))
                    else:
                        messagebox.showerror("Error", "Unsupported file format!")
                        return

                    self.random_numbers_list.append(random_numbers)
                    self.filename.set(', '.join([file_path.split("/")[-1] for file_path in file_paths])) # Show the file name
                    self.file_names.append(file_path.split("/")[-1])  # Just store the file name, not the full path
                    self.file_add.append(file_path)  # Store the full file path

                messagebox.showinfo("Files Loaded", "Files loaded successfully!")

            except Exception as e:
                messagebox.showerror("Error", f"Could not load files: {str(e)}")

    def clear_previous_results(self):
        """Clear the preview and result text widgets."""
        self.preview_text.delete(1.0, tk.END)
        if hasattr(self, 'result_text'):
            self.result_text.delete(1.0, tk.END)

    # Run the preview with progress bar
    def run_preview(self):
        if not self.random_numbers_list:
            messagebox.showerror("Error", "No files loaded! Please load files first.")
            return

        self.progress.start(10)  # Start the buffering circle
        threading.Thread(target=self.preview_file).start()

    def preview_file(self):
        try:
            num_files = len(self.random_numbers_list)
            if num_files == 0:
                messagebox.showerror("Error", "No data to preview! Please load files first.")
                return

            time.sleep(1)  # Simulating some processing delay

            # Progress calculation: loop through files and update progress
            for i, numbers in enumerate(self.random_numbers_list):
                file_name = self.file_names[i]

                # Convert numbers to bits and show first 100 bits
                bits = ''.join(str(num) for num in numbers)  # Use str(num) if already binary

                preview_text = f"File: {file_name}\n{bits[:1000]}\n{'-' * 65}\n"
                print(len(bits))
                # Insert into the preview text area
                self.preview_text.insert(tk.END, preview_text)

                # Update progress (proportional to number of files processed)
                progress_value = ((i + 1) / num_files) * 100  # Calculate the percentage
                self.progress['value'] = progress_value
                self.update_idletasks()  # Update the GUI with the progress

            messagebox.showinfo("Preview Complete", "File preview completed!")
        except Exception as e:
            messagebox.showerror("Error", f"Could not preview files: {str(e)}")
        finally:
            self.progress.stop()  # Stop the buffering circle after preview completes

    # Run the selected test with progress bar
    def run_test(self):
        if not self.random_numbers_list:
            messagebox.showerror("Error", "No files loaded! Please load files first.")
            return

        self.progress.start(10)  # Start the buffering circle
        threading.Thread(target=self.execute_test).start()

    def execute_test(self):
        global all_test_results
        try:
            num_files = len(self.random_numbers_list)
            if num_files == 0:
                messagebox.showerror("Error", "No files to test! Please load files first.")
                return

            # Clear previous results
            self.result_text.delete(1.0, tk.END)

            all_test_results = {}  # Dictionary to store results for each file

            # Loop through each file and run the selected test
            for i, random_numbers in enumerate(self.random_numbers_list):
                file_name = self.file_names[i]
                test_name = self.selected_test.get()

                if test_name == "NIST Test":
                    binary_string = ''.join(f'{int(num):b}' for num in random_numbers)
                    test_results = process_bit_sequence(binary_string)

                    self.result_text.insert(tk.END, f"Results for {file_name}:\n")
                    header_format = f"{'Test Name':<40}{'P-Value':<15}{'Result':<10}\n"
                    self.result_text.insert(tk.END, header_format)
                    self.result_text.insert(tk.END, "-" * 65 + "\n")

                    p_values = {}
                    for test_name, test_result in test_results.items():
                        p_value, success = test_result
                        result_status = 'Success' if success else 'Failure'
                        row_format = f"{test_name:<40}{p_value:<15.4f}{result_status:<10}\n"
                        self.result_text.insert(tk.END, row_format)
                        p_values[test_name] = p_value  # Store p-values with test names as keys

                    all_test_results[file_name] = p_values  # Store results for the file

                elif test_name == "DieHarder Test":
                    file_path = self.file_add[i]  # Get the full file path
                    result = self.run_dieharder_test(file_path)
                    self.result_text.insert(tk.END, f"Results for {file_name}:\n{result}\n")


                elif test_name == "Shannon Entropy Test":
                    # Calculate Shannon entropy and p-value
                    p_value, entropy_value = shannon_entropy(random_numbers)
                    bit_sequence_length = len(
                        ''.join(f'{int(num):b}' for num in random_numbers))  # Calculate bit sequence length
                    # Format the result string to include length, entropy value, and p-value
                    result = (
                        f"Shannon Entropy Test for {file_name}:\n"
                        f"Length of Bit Sequence: {bit_sequence_length}\n"
                        f"Entropy Value: {entropy_value:.8f}\n"
                        f"P-Value: {p_value:.8f}\n"
                    )
                    # Insert the result into the GUI's result text widget
                    self.result_text.insert(tk.END, result)
                    # Store results in all_test_results
                    all_test_results[file_name] = {
                        "Entropy Value": entropy_value,
                        "P-Value": p_value,
                        "Bit Sequence Length": bit_sequence_length
                    }

                self.result_text.insert(tk.END, "\n" + "=" * 65 + "\n")
                # Update progress based on the number of files processed
                progress_value = ((i + 1) / num_files) * 100
                self.progress['value'] = progress_value
                self.update_idletasks()  # Update the progress bar visually

            messagebox.showinfo("Tests Complete", "Randomness testing completed!")
            # Plot results only if NIST Test suite was run
            if self.selected_test.get() == "NIST Test":
                self.plot_results(all_test_results)
        except Exception as e:
            messagebox.showerror("Error", f"Error during test execution: {str(e)}")
        finally:
            self.progress.stop()  # Stop the buffering circle after test execution completes

    def save_results(self):
        """
        Save test results in TXT, Excel, or PDF formats.
        """
        if not hasattr(self, 'result_text') or not self.result_text.get(1.0, tk.END).strip():
            messagebox.showerror("Error", "No results to save! Please run a test first.")
            return

        # Prompt user to choose the save format
        save_formats = [("Text Files", "*.txt"), ("Excel Files", "*.xlsx"), ("PDF Files", "*.pdf")]
        save_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=save_formats)

        if not save_path:
            return

        try:
            file_extension = save_path.split('.')[-1]
            results = self.result_text.get(1.0, tk.END).strip()

            if file_extension == "txt":
                with open(save_path, 'w') as txt_file:
                    txt_file.write(results)
                messagebox.showinfo("Success", f"Results saved as TXT at {save_path}")

            else:
                messagebox.showerror("Error", "Unsupported file format selected!")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to save results: {str(e)}")

    # Create the testing tab
    def create_testing_tab(self):
        tk.Label(self.testing_tab, text="Select a randomness test:").pack(pady=10)
        self.selected_test = tk.StringVar()
        tests = ["NIST Test", "DieHarder Test", "Shannon Entropy Test"]
        self.selected_test.set(tests[0])
        tk.OptionMenu(self.testing_tab, self.selected_test, *tests).pack(pady=5)

        tk.Button(self.testing_tab, text="Run Test", command=self.run_test).pack(pady=10)

        # Add the progress bar here
        self.progress.pack(pady=10)  # Pack the progress bar with padding

        self.result_text = tk.Text(self.testing_tab, height=30, width=90)
        self.result_text.pack(pady=10)
        tk.Button(self.testing_tab, text="Save Results", command=self.save_results).pack(pady=10)

    # Create the settings tab
    def create_settings_tab(self):
        tk.Label(self.settings_tab, text="Settings coming soon!").pack(pady=20)

    # Create the help tab
    def create_help_tab(self):
        tk.Label(self.help_tab, text="Help and Documentation coming soon!").pack(pady=20)

    # Plot results in a new window
    def plot_results(self, test_results):
        plot_window = tk.Toplevel(self)
        plot_window.title("Test Results Comparison")

        # Increase figure size for better visibility
        fig, ax = plt.subplots(figsize=(12, 8))  # Adjust the figure size

        # Prepare data for plotting
        if not test_results:
            messagebox.showwarning("No Data", "No test results available to plot.")
            return

        # Use the first file's results to get test names
        test_names = list(next(iter(test_results.values())).keys())  # Get test names from the first file's results

        for file_name, p_values in test_results.items():
            # Ensure p_values are extracted correctly
            p_values_list = [p_values[test] for test in test_names]  # Extract p-values for all tests

            ax.plot(test_names, p_values_list, marker='o', label=file_name)

            # Annotate each point with its corresponding p-value
            #for x, p in enumerate(p_values_list):
            #    ax.annotate(f'{p:.4f}', (x, p), textcoords="offset points", xytext=(0, 10), ha='center')

        ax.set_xlabel('NIST Tests', fontsize=14)
        ax.set_ylabel('P-Values', fontsize=14)
        ax.set_title('Randomness Test Results Comparison', fontsize=16)

        # Set x-ticks to test names and rotate labels
        ax.set_xticks(range(len(test_names)))  # Set x-ticks to the number of tests
        ax.set_xticklabels(test_names, rotation=45, ha='right', fontsize=12)  # Adjust font size and rotation

        ax.legend()

        # Use tight layout with padding to ensure everything fits
        plt.tight_layout(pad=3.0)

        canvas = FigureCanvasTkAgg(fig, master=plot_window)
        canvas.draw()

        # Create a frame for buttons at the bottom of the window
        button_frame = tk.Frame(plot_window)
        button_frame.pack(side=tk.BOTTOM, pady=10)  # Pack at the bottom with padding

        # Save Plot Button
        save_button = tk.Button(button_frame, text="Save Plot", command=lambda: self.save_plot(fig))
        save_button.pack(side=tk.LEFT, padx=5)  # Pack button to the left with padding

        # Close Button
        close_button = tk.Button(button_frame, text="Close", command=plot_window.destroy)
        close_button.pack(side=tk.LEFT, padx=5)  # Pack button to the left with padding

        # Add canvas to the window
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)  # Ensure the canvas fills the window

    # Save plot as an image
    def save_plot(self, fig):
        save_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG Files", "*.png"),
                                                                                     ("JPEG Files", "*.jpg"),
                                                                                     ("All Files", ".*")])
        if save_path:
            fig.savefig(save_path)
            messagebox.showinfo("Success", f"Plot saved to {save_path}")


# Create the extraction tab
    def create_extraction_tab(self):
        tk.Label(self.extraction_tab, text="Select an extraction method:").pack(pady=10)
        self.selected_extraction = tk.StringVar()
        extractions = ["Von Neumann Extraction", "Trevison Extraction"]  # Add more extraction methods if needed
        self.selected_extraction.set(extractions[0])
        tk.OptionMenu(self.extraction_tab, self.selected_extraction, *extractions).pack(pady=5)

        tk.Button(self.extraction_tab, text="Run Extraction", command=self.run_extraction).pack(pady=10)
        self.progress.pack(pady=10)


        self.extraction_result_text = tk.Text(self.extraction_tab, height=30, width=90)
        self.extraction_result_text.pack(pady=10)

        # Add a button to save the output
        tk.Button(self.extraction_tab, text="Save Output", command=self.save_output).pack(pady=5)

        # Add a label to display input and output lengths
        self.length_label = tk.Label(self.extraction_tab, text="")
        self.length_label.pack(pady=5)


    # Implement the extraction methods
    def run_extraction(self):
        if not self.random_numbers_list:
            messagebox.showerror("Error", "No files loaded! Please load files first.")
            return

        extraction_method = self.selected_extraction.get()
        self.progress.start(10)  # Start the buffering circle
        threading.Thread(target=self.execute_extraction, args=(extraction_method,)).start()

    def execute_extraction(self, extraction_method):
        try:
            self.extraction_result_text.delete(1.0, tk.END)  # Clear previous results
            result_text = f"Extraction Method: {extraction_method}\n\n"

            self.extracted_output = ""  # Initialize the full output to be saved

            for i, random_numbers in enumerate(self.random_numbers_list):
                file_name = self.file_names[i]
                result_text += f"Results for {file_name}:\n"

                # Calculate the input length
                input_length = len(random_numbers)

                # Extract data based on the selected method
                if extraction_method == "Von Neumann Extraction":
                    extracted_data = self.von_neumann_extraction(random_numbers)
                elif extraction_method == "Trevison Extraction":
                    extracted_data = self.trevison_extraction(random_numbers)
                else:
                    extracted_data = "No data extracted. Invalid method."

                # Calculate the output length
                output_length = len(extracted_data)

                # Add input/output lengths to the result
                result_text += f"Input Length: {input_length} bits | Output Length: {output_length} bits\n"

                # Add the extracted data preview
                result_text += f"{extracted_data[:1000]}...\n\n"  # Truncate for display

                # Store the full extracted data for saving
                self.extracted_output += f"File: {file_name}\nInput Length: {input_length} bits | Output Length: {output_length} bits\n"
                self.extracted_output += f"{extracted_data}\n\n"

            # Update the text widget with the result
            self.extraction_result_text.insert(tk.END, result_text)

            messagebox.showinfo("Extraction Complete", "Extraction process completed!")

        except Exception as e:
            messagebox.showerror("Error", f"Error during extraction: {str(e)}")
        finally:
            self.progress.stop()  # Stop the buffering circle after extraction completes

    # Add a method to save the output
    def save_output(self):
        if not hasattr(self, 'extracted_output') or not self.extracted_output:
            messagebox.showerror("Error", "No output to save! Run extraction first.")
            return

        file_path = filedialog.asksaveasfilename(
            title="Save Output",
            defaultextension=".txt",
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
        )
        if file_path:
            try:
                with open(file_path, "w") as file:
                    file.write(self.extracted_output)
                messagebox.showinfo("Save Complete", "Output saved successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Error saving file: {str(e)}")

    # Example implementations of extraction methods (placeholders)
    sys.path.append('Python Project')

    def von_neumann_extraction(self, numbers):
        # Convert numbers to a uniform bit sequence (zero-padded 8-bit binary)
        bit_sequence = ''.join(f'{int(num):b}' for num in numbers)

        # Call process_bits with this bit sequence
        result = process_bits(bit_sequence)

        # Return the full extracted result
        return result

    def trevison_extraction(self, numbers):
        # Placeholder logic for Trevison Extraction
        extracted_bits = [num % 2 for num in numbers]
        return "Extracted Bits: " + ''.join(map(str, extracted_bits[:100])) + "\n\n"  # Show first 100 bits

    # Other tabs, file loading, and preview functions go here (unchanged)...


if __name__ == "__main__":
    app = QRNG_GUI()
    app.mainloop()
