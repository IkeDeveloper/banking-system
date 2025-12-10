import tkinter as tk
from tkinter import ttk

root = tk.Tk()
root.title("Dropdown Example")

options = ["Savings", "Current", "Business", "Student"]
selected = tk.StringVar()

dropdown = ttk.Combobox(root, textvariable=selected)
dropdown['values'] = options
dropdown.current(0)  # Set default
dropdown.pack(pady=10)

def show_selection():
    print("Selected:", selected.get())

btn = tk.Button(root, text="Submit", command=show_selection)
btn.pack()

root.mainloop()

