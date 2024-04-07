import tkinter as tk
from tkinter import ttk
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os
import subprocess

def print_treeview_to_pdf(treeview, filename):
    # Create a PDF canvas
    c = canvas.Canvas(filename, pagesize=letter)

    # Set up the PDF layout
    x_offset = 50
    y_offset = 750
    line_height = 20

    # Get column names
    columns = treeview['columns']

    # Write header row to PDF
    for i, column in enumerate(columns):
        c.drawString(x_offset + i * 100, y_offset, column)
    y_offset -= line_height  # Move to the next line after the header

    # Iterate over each item in the treeview
    for item in treeview.get_children():
        # Get item values as a tuple
        item_values = treeview.item(item, 'values')
        # Write the row values to the PDF
        for i, value in enumerate(item_values):
            c.drawString(x_offset + i * 100, y_offset, str(value))
        y_offset -= line_height  # Move to the next line for the next row

    # Save PDF
    c.save()

# Create a Tkinter window
root = tk.Tk()
root.title("TreeView to PDF")

# Create a TreeView
treeview = ttk.Treeview(root, columns=('Name', 'Age'))
treeview.heading('#0', text='ID')
treeview.heading('#1', text='Name')
treeview.heading('#2', text='Age')

# Insert sample data into TreeView
data = [
    ("1", "Alice", "25"),
    ("2", "Bob", "30"),
    ("3", "Charlie", "35"),
    ("4", "David", "40"),
    ("5", "Emma", "45")
]

for item in data:
    treeview.insert('', 'end', text=item[0], values=(item[1], item[2]))



def on_print_button_click():
    
   
    print_treeview_to_pdf(treeview, "treeview.pdf")  # Create the PDF first
    try:
        subprocess.run(["start", "treeview.pdf"], shell=True)  # Open the PDF after it's saved
    except Exception as e:
        print("Error opening PDF:", e)

# Print the TreeView data to PDF
print_button = tk.Button(root, text="Print to PDF", command=on_print_button_click)
print_button.pack()

# Pack the TreeView widget
treeview.pack()

# Run the Tkinter event loop
root.mainloop()
