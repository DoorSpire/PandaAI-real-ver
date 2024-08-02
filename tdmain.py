import tkinter as tk
from tkinter import filedialog
import renderer

def choose_file_and_render():
    root = tk.Tk()
    root.withdraw()

    file_path = filedialog.askopenfilename(filetypes=[("Wavefront OBJ files", "*.obj")])
    if file_path:
        print("Selected file:", file_path)
        app = renderer.SoftwareRenderer(file_path)
        app.run()
    else:
        print("No file selected.")