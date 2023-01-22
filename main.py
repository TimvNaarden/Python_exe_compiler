import os
import subprocess
import re
from tkinter import *
from tkinter import filedialog
import shutil
import shlex

def get_imports(file):
    """
    Given the file path, the function extracts all the imported modules by looking for the 'import' and 'from import' statements.
    """
    with open(file, 'r') as f:
        lines = f.readlines()
    imports = []
    for line in lines:
        match = re.search(r'^import\s+(\w+)', line)
        if match:
            imports.append(match.group(1))
        match = re.search(r'^from\s+(\w+)\s+import', line)
        if match:
            imports.append(match.group(1))
    return imports

def select_file():
    filepath = filedialog.askopenfilename()
    file_label.config(text=filepath)

def select_folder():
    output_folder = filedialog.askdirectory()
    output_folder_label.config(text=output_folder)

def select_data():
    data_paths = filedialog.askopenfilenames()
    data_label.config(text='\n'.join(data_paths))

def convert_to_exe():
    file = file_label.cget("text").strip('"')
    data_paths = data_label.cget("text").strip('"').split("\n")
    output_folder = output_folder_label.cget("text").strip('"')
    if os.path.isfile(file):
        modules = get_imports(file)
        hidden_imports = ["--hidden-import=" + module for module in modules]
        build_folder = os.path.join(output_folder, 'build') # create the build folder path
        data_args = []
        if data_label.cget("text") != "No data file selected":
            for data_path in data_paths:
                data_args += ['--add-data', data_path]
        subprocess.call(["pyinstaller", "--onefile", "--distpath=" + output_folder, "--workpath=" + build_folder, "--specpath=" + build_folder, *hidden_imports, *data_args, file])
        success_label.config(text="File converted to EXE!")

        shutil.rmtree(build_folder) # delete the build folder
    else:
        success_label.config(text="Invalid file path or file not found.")


def select_data():
    data_paths = filedialog.askopenfilenames()
    data_label.config(text='\n'.join(data_paths))


root = Tk()
root.title("Python to EXE Converter")
root.geometry("300x200")

file_button = Button(root, text="Select File", command=select_file)
file_button.pack()

file_label = Label(root, text="No file selected")
file_label.pack()

data_button = Button(root, text="Select Data File", command=select_data)
data_button.pack()

data_label = Label(root, text="No data file selected")
data_label.pack()

output_folder_button = Button(root, text="Select Output Folder", command=select_folder)
output_folder_button.pack()

output_folder_label = Label(root, text="No output folder selected")
output_folder_label.pack()

convert_button = Button(root, text="Convert to EXE", command=convert_to_exe)
convert_button.pack()



success_label = Label(root, text="")
success_label.pack()

root.mainloop()
