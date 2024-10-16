import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
import pandas as pd
import numpy as np
import scipy.stats as stats
import math
import sys
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import threading
import time

# Increase the limit for integer string conversion
sys.set_int_max_str_digits(10025000)  # Adjust the value to your needs

# Importing the NIST test functions
sys.path.append('Python Project')
from nist_test_framework import process_bit_sequence


def dieharder_test(numbers):
    p_value = 0.5  # Example placeholder value
    return p_value


def kolmogorov_smirnov_test(numbers):
    d_statistic, p_value = stats.kstest(numbers, 'uniform')
    return d_statistic, p_value


def entropy_test(numbers):
    bits = ''.join(f'{int(num):b}' for num in numbers)
    n = len(bits)
    p_1 = bits.count('1') / n
    p_0 = 1 - p_1
    if p_0 > 0 and p_1 > 0:
        entropy = - (p_0 * math.log2(p_0) + p_1 * math.log2(p_1))
    else:
        entropy = 0
    return entropy


def autocorrelation_test(numbers, lag=1):
    bits = ''.join(f'{int(num):b}' for num in numbers)
    n = len(bits)
    auto_corr = sum(int(bits[i]) == int(bits[(i + lag) % n]) for i in range(n))
    p_value = (auto_corr - (n / 2)) / math.sqrt(n / 4)
    return auto_corr, p_value


# Define the GUI application class
class QRNG_GUI(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Quantum Random Number Generator GUI")
        self.geometry("1024x768")

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
                        random_numbers = data.iloc[:, 0].values
                    elif file_path.endswith('.txt') or file_path.endswith('.dat') or file_path.endswith('.pi'):
                        with open(file_path, 'r') as file:
                            random_numbers = list(map(int, file.read().split()))
                    else:
                        messagebox.showerror("Error", "Unsupported file format!")
                        return

                    self.random_numbers_list.append(random_numbers)
                    self.filename.set(', '.join([file_path.split("/")[-1] for file_path in file_paths])) # Show the file name
                    self.file_names.append(file_path.split("/")[-1])  # Just store the file name, not the full path

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
                bits = ''.join(f'{int(num):b}' for num in numbers)
                preview_text = f"File: {file_name}\n{bits[:100]}\n{'-' * 65}\n"

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

                elif test_name == "Kolmogorov-Smirnov Test":
                    d_statistic, p_value = kolmogorov_smirnov_test(random_numbers)
                    result = f"Kolmogorov-Smirnov Test for {file_name}:\nD-Statistic: {d_statistic:.4f}\nP-Value: {p_value:.4f}\n"
                    self.result_text.insert(tk.END, result)

                    # Store p-value in all_test_results
                    all_test_results[file_name] = {test_name: p_value}

                    self.result_text.insert(tk.END, "\n" + "=" * 65 + "\n")
                # Update progress based on the number of files processed
                progress_value = ((i + 1) / num_files) * 100
                self.progress['value'] = progress_value
                self.update_idletasks()  # Update the progress bar visually

            messagebox.showinfo("Tests Complete", "Randomness testing completed!")

        except Exception as e:
            messagebox.showerror("Error", f"Error during test execution: {str(e)}")
        finally:
            self.progress.stop()  # Stop the buffering circle after test execution completes

        # Once all tests are completed, plot the results
        self.plot_results(all_test_results)

    # Create the testing tab
    def create_testing_tab(self):
        tk.Label(self.testing_tab, text="Select a randomness test:").pack(pady=10)
        self.selected_test = tk.StringVar()
        tests = ["NIST Test", "DIE-Hard Test", "Kolmogorov-Smirnov Test", "Shannon Entropy Test",
                 "Autocorrelation Test"]
        self.selected_test.set(tests[0])
        tk.OptionMenu(self.testing_tab, self.selected_test, *tests).pack(pady=5)

        tk.Button(self.testing_tab, text="Run Test", command=self.run_test).pack(pady=10)

        # Add the progress bar here
        self.progress.pack(pady=10)  # Pack the progress bar with padding

        self.result_text = tk.Text(self.testing_tab, height=30, width=90)
        self.result_text.pack(pady=10)

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


# Run the application
if __name__ == "__main__":
    app = QRNG_GUI()
    app.mainloop()
