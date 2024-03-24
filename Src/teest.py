import tkinter as tk

# Create the main window
root = tk.Tk()
root.title("Receipt")

# Create a Text widget for the receipt
receipt_text = tk.Text(root, width=60, height=20)
receipt_text.pack()

# Insert the receipt content into the Text widget
receipt_content = """
            
            Company Name
            Address Line 1
            Address Line 2
            City, State, Zip Code
            Phone Number
            Email Address
            Website URL

            Date: [Date and Time]
            Receipt Number: [Receipt Number]

-------------------------------------------------------
Description          Qty    Price   Subtotal
-------------------------------------------------------
Item 1               1      $10.00   $10.00
Item 2               2      $5.00    $10.00
Item 3               1      $8.00    $8.00
-------------------------------------------------------
Total: $28.00

Payment Method: Cash

Thank you for your purchase!
"""

receipt_text.insert(tk.END, receipt_content)

# Disable text editing
receipt_text.config(state=tk.DISABLED)

# Run the Tkinter event loop
root.mainloop()
