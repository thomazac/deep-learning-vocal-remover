import tkinter as tk
from tkinter import filedialog, messagebox, ttk, scrolledtext
from inference import main as separate_main
import threading
import sys
import os
import io

# Override the argparse in the original script
sys.argv = ['separator.py']

# Define the colors for the dark theme
dark_background_color = "#1C1C1E"
dark_foreground_color = "#F2F2F7"
dark_button_color = "#3A3A3C"
dark_entry_color = "#2C2C2E"
dark_text_color = "#FFFFFF"

class StdoutRedirector(io.StringIO):
    def __init__(self, text_widget):
        self.text_widget = text_widget

    def write(self, string):
        if not self.text_widget['state'] == 'normal':
            self.text_widget['state'] = 'normal'
        self.text_widget.insert(tk.END, string)
        self.text_widget.see(tk.END)
        self.text_widget['state'] = 'disabled'

    def flush(self):
        pass

def select_file(entry, filetypes=[("All files", "*.*")]):
    file_path = filedialog.askopenfilename(filetypes=filetypes)
    if file_path:
        entry.delete(0, tk.END)
        entry.insert(0, file_path)

def select_folder(entry):
    folder_path = filedialog.askdirectory()
    if folder_path:
        entry.delete(0, tk.END)
        entry.insert(0, folder_path)

def get_model_files():
    models_dir = 'models/'
    return [f for f in os.listdir(models_dir) if f.endswith('.pth')]

def separate():
    # Disable the button to prevent multiple clicks
    separate_button['state'] = 'disabled'

    # Redirect stdout and stderr
    old_stdout = sys.stdout
    old_stderr = sys.stderr
    sys.stdout = StdoutRedirector(console_text)
    sys.stderr = StdoutRedirector(console_text)

    # Using threading.Event to notify the main thread of completion
    completed_event = threading.Event()

    def run_separation():
        try:
            # Clear previous arguments and set the script name
            sys.argv = ['separator.py']

            # Construct the command-line arguments
            sys.argv.extend(['--pretrained_model', os.path.join('models', model_var.get())])
            sys.argv.extend(['--input', input_path.get()])
            sys.argv.extend(['--output_dir', output_dir.get()])
            sys.argv.extend(['--gpu', '0' if gpu_var.get() else '-1'])
            if processing_var.get() == 'postprocess':
                sys.argv.append('--postprocess')
            elif processing_var.get() == 'tta':
                sys.argv.append('--tta')

            # Run the main function from the separate script
            separate_main()
        except Exception as e:
            # Schedule the messagebox to be shown in the main thread
            root.after(0, messagebox.showerror, "Error", str(e))
        finally:
            # Notify the main thread that processing is completed
            completed_event.set()

    # Run the separation in a separate thread
    thread = threading.Thread(target=run_separation)
    thread.start()

    # Check for the completion of the thread in a non-blocking way
    def check_thread():
        if completed_event.is_set():
            # Restore stdout and stderr
            sys.stdout = old_stdout
            sys.stderr = old_stderr
            # Re-enable the button after completion or failure
            separate_button['state'] = 'normal'
            # Inform the user of success if no error was caught
            if not thread.is_alive():
                messagebox.showinfo("Success", "Separation completed!")
        else:
            # Check again after some delay
            root.after(100, check_thread)

    # Start checking for thread completion
    check_thread()

root = tk.Tk()
root.title("Vocal Separator")

# Apply dark theme colors
root.configure(bg=dark_background_color)

style = ttk.Style()
style.theme_use('clam')
style.configure('TLabel', background=dark_background_color, foreground=dark_text_color)
style.configure('TEntry', fieldbackground=dark_entry_color, foreground=dark_text_color)
style.configure('TButton', background=dark_button_color, foreground=dark_text_color)
style.configure('TRadiobutton', background=dark_background_color, foreground=dark_text_color)
style.configure('TCheckbutton', background=dark_background_color, foreground=dark_text_color)

# Input file
ttk.Label(root, text="Input File:").grid(row=0, column=0, sticky='e')
input_path = ttk.Entry(root, width=50)
input_path.grid(row=0, column=1)
ttk.Button(root, text="Browse", command=lambda: select_file(input_path, [("WAV files", "*.wav")])).grid(row=0, column=2)

# Output directory
ttk.Label(root, text="Output Directory:").grid(row=1, column=0, sticky='e')
output_dir = ttk.Entry(root, width=50)
output_dir.grid(row=1, column=1)
ttk.Button(root, text="Browse", command=lambda: select_folder(output_dir)).grid(row=1, column=2)

# Model selection
ttk.Label(root, text="Model:").grid(row=2, column=0, sticky='e')
model_var = tk.StringVar()
model_dropdown = ttk.Combobox(root, textvariable=model_var, values=get_model_files(), state="readonly")
model_dropdown.grid(row=2, column=1)
model_dropdown.set('Select a model')  # Default text

# GPU or CPU
gpu_var = tk.BooleanVar()
ttk.Checkbutton(root, text="Use GPU (cuda:0)", variable=gpu_var).grid(row=3, column=1, sticky='w')

# Processing options
processing_var = tk.StringVar(value="none")  # default value is none
processing_frame = ttk.LabelFrame(root, text="Processing Options", labelanchor='n')
processing_frame.grid(row=4, column=1, sticky='w', padx=10, pady=10)
ttk.Radiobutton(processing_frame, text="None", variable=processing_var, value="none").pack(anchor='w')
ttk.Radiobutton(processing_frame, text="Postprocess", variable=processing_var, value="postprocess").pack(anchor='w')
ttk.Radiobutton(processing_frame, text="Test-time Augmentation (TTA)", variable=processing_var, value="tta").pack(anchor='w')

# Separate button
separate_button = ttk.Button(root, text="Separate", command=separate)
separate_button.grid(row=5, column=1, pady=10)

# Console area
console_frame = ttk.LabelFrame(root, text="Console Output", labelanchor='n')
console_frame.grid(row=6, column=0, columnspan=3, sticky='nsew', padx=10, pady=10)
console_text = scrolledtext.ScrolledText(console_frame, height=10)
console_text.pack(fill='both', expand=True)
console_text['state'] = 'disabled'  # Prevent user from typing into the console

root.mainloop()
