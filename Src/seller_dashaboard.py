                   
from customtkinter import*
import tkinter as tk
from PIL import Image
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import subprocess
import mysql.connector
from tkinter import messagebox,ttk
from CTkTable import *
from CTkTableRowSelector import *
from CTkMessagebox import*
from decimal import Decimal, InvalidOperation
from pdf2image import convert_from_bytes
from PyPDF2 import PdfWriter, PdfReader
import io
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader







my_connection= mysql.connector.connect(


    host="localhost",
    user="root",
    password="",
    database="hardware_db"
  
)
my_db= my_connection.cursor()

class Seller_dash_App:
    def __init__(self, master):
       
        self.master = master
        self.setup_seller_dashboard()
      
   
    def setup_seller_dashboard(self):
        self.master.geometry("1034x600")
        self.master.minsize(1034,600)
#==============================================================================================================      
        def show_error(message=None):
             CTkMessagebox(title="Invalid Input", message="Please put value in Quantity textbox or Product Name", icon="cancel")
#==============================================================================================================
        def show_error_in():
             CTkMessagebox(title="Invalid Input", message="Invalid productname", icon="cancel")
#============================================================================================================== 

#==============================================================================================================
        def show_quantity():
             CTkMessagebox(title="Invalid Input", message="Invalid Quantity", icon="cancel")
#============================================================================================================== 
        def on_validate(char, entry_value):
            return char.isdigit() and len(entry_value) < 4 or char == ""     
#============================================================================================================== 

        def update_stock(product_name, quantity):

           
            try:
                # Subtract the specified quantity from the QuantityOnHand for the specified product
                query = "UPDATE products SET Current_Stock = Current_Stock- %s WHERE ProductName = %s"
                values = (quantity, product_name)
                my_db.execute(query, values)
                my_connection.commit()
                refresh()
            except mysql.connector.Error as err:
                print(f"Failed to update stock: {err}")





#==============================================================================================================      


        
#==============================================================================================================      
     
          
        def print_treeview_to_pdf(treeview, filename,logo_path):
                c = canvas.Canvas(filename, pagesize=letter)
                page_width, page_height = letter
                x_offset = (page_width - 100) / 2  
                y_offset = page_height - 100 - 50  
                line_height = 20
                left_margin = 80
                line_margin = 5
                line_length = page_width - 3 * left_margin + 20
                logo = ImageReader(logo_path)
                c.drawImage(logo, x_offset, y_offset, width=80, height=80) 
                y_offset -= 80 

               
                columns = treeview['columns']

                for i, column in enumerate(columns):
                    header_x_offset = left_margin + i * 120 
                    c.drawString(header_x_offset, y_offset, column)
                y_offset -= line_height              




              
                for item in treeview.get_children():
                    item_values = treeview.item(item, 'values')
                    for i, value in enumerate(item_values):
                        c.drawString(left_margin + i * 120, y_offset, str(value))  
                    y_offset -= line_height 

                separator_y_offset = y_offset + line_margin
                c.line(left_margin, separator_y_offset, left_margin + line_length, separator_y_offset)

                # Adjust y_offset for the next row
                y_offset -= line_margin
              
                c.save()


       
#==============================================================================================================      

 
        def ask_question(current_name, quantity, price_product, subtotal):
            msg = CTkMessagebox(title="Confirmation", message="Do you want to process this transaction?",
                                icon="question", option_1="No", option_2="Yes")
            response = msg.get()

            if response == "Yes":
                    pname.delete(0,'end')
                    qty.delete(0,'end')
                    new_row = [current_name, quantity, price_product, subtotal]
                    treeview.insert('', 'end', values=new_row)
                    total = 0
                    for item in treeview.get_children():
                        subtotal = float(treeview.item(item, 'values')[3])  
                        total += subtotal
                        gtotal.delete(0,'end')
                        gtotal.insert(0, total)

                
            else:
                print("Click 'No' to cancel!")


        def on_print_button_click():
            if treeview.get_children():  
                msg = CTkMessagebox(title="Confirmation", message="Do you want to print this transaction?",
                                    icon="question", option_1="No", option_2="Yes")
                response = msg.get()
                if response == "Yes":
                    logo_path = r"D:\\DS102PROJECT\\Icon\\logos.png" 
                    print_treeview_to_pdf(treeview, "treeview.pdf",logo_path) 
                    try:
                        subprocess.run(["start", "treeview.pdf"], shell=True) 
                        treeview.delete(*treeview.get_children()) 
                    except Exception as e:
                        print("Error opening PDF:", e)
            else:
                empty_msg = CTkMessagebox(title="You cant print the data", message="The Treeview is empty.", icon="info")
               
#==============================================================================================================


        frame = CTkFrame(
            master=self.master,
            fg_color="#F6F5F5",
            width=1000,
            height=580,
            corner_radius=20
           
        )
        frame.pack(expand=True, fill="both")

      
        tabview =CTkTabview(master=frame,
                            width=1020,
                            height=550,
                            fg_color = ("#F6F5F5", "#EEEEEE"))
        tabview.pack()
        tabview.add("tab 1") 
        tabview.add("tab 2") 
        tabview.add("tab 3") 
        tabview.add("tab 4") 
        tabview.add("tab 5") 
        tabview.rename("tab 1","Dashboard")
        tabview.rename("tab 2","Sell Products")
        tabview.rename("tab 3","My Sales")
        tabview.rename("tab 4", "Product Reports") 
        tabview.rename("tab 5", "Manage Profile") 

        tabview.set("Dashboard")


        label_pname= CTkLabel(master=tabview.tab("Sell Products"),
                              text="PRODUCT NAME:",
                              font=("Tahoma",10,"bold"),
                              text_color="#222831")
        label_pname.place(relx=0.01, rely=0.04)

        pname = CTkEntry(master=tabview.tab("Sell Products"),
                            border_color="#125B50",
                            border_width=1,
                            width=200
                        )
        pname.place(relx=0.01, rely=0.09)




#==============================================================================================================      
        #Search functionality on products
        def search_product():
            search=pname.get().strip()
            
            if search:
               
               query = "SELECT `ProductID`, `ProductName`, `Category`, `Price`, `QuantityOnHand`, `Current_stock` FROM `products` WHERE ProductName LIKE %s OR Price LIKE %s"
               value= ("%" + search + "%","%" + search + "%")
            else:
                query = "SELECT `ProductID`, `ProductName`, `Category`, `Price`, `QuantityOnHand`, `Current_stock` FROM `products`"
                value = ()
            my_db.execute(query, value)
            data = my_db.fetchall()
            
            
            table_data.clear()
            table_data.extend([custom_headers] + data)         
            table.configure(values=table_data)
#==============================================================================================================      
        
        search_btn= CTkButton(master=tabview.tab("Sell Products"),
                              width=70,
                              text="Search",
                              cursor="hand2",
                              command=search_product
                             
                              )
        
        search_btn.place(relx=0.226, rely=0.09)


        
        label_qty= CTkLabel(master=tabview.tab("Sell Products"),
                              text="QUANTITY:",
                              font=("Tahoma",10,"bold"),
                              text_color="#222831")
        label_qty.place(relx=0.01, rely=0.15)

#==============================================================================================================      
        

        def qty_count():
            product_name=pname.get()
            global quantity
            quantity = qty.get()

            if not quantity:
                show_error("Quantity is empty")
                return

            try:
                quantity = int(quantity)
            except ValueError:
                show_error("Invalid quantity")
                return
            

            query = "SELECT ProductName FROM products WHERE ProductName= %s"
            my_db.execute(query, (product_name,))

            data =  my_db.fetchall()
            if data:
           
                if quantity <= 0:     
                    show_error()
                    return  
                if not quantity:

                    print("qty is empty")

                elif price_product==0:
                    show_error("Price of the product is not defined due to the invalid productname")
                elif quantity > stock:
                   
                    show_quantity()
                else:
                    subtotal = Decimal(price_product) * int(quantity)
                    ask_question(product_name, quantity,price_product, subtotal)
            else:
                show_error_in()
                return
            
            
           
           
#==============================================================================================================  
     
        
        
#==============================================================================================================  


        qty = CTkEntry(master=tabview.tab("Sell Products"),
                            border_color="#125B50",
                            border_width=1,
                            width=200,
                            validate="key", 
                            validatecommand=(tabview.tab("Sell Products").register(on_validate), "%S", "%P"),
                        )
        qty.place(relx=0.01, rely=0.2)
       
        sell= CTkButton(master=tabview.tab("Sell Products"),
                       width=100,
                       text="Sell",
                       cursor="hand2",
                     
                       command=qty_count )
        sell.place(relx=0.01, rely=0.29)



#==============================================================================================================      
        #Clear textboxes
        def clear():
            pname.delete(0,'end')
            qty.delete(0, 'end')
  
        clear_btn= CTkButton(master=tabview.tab("Sell Products"),
                       width=100,
                       text="Clear",
                       cursor="hand2",
                       command=clear
                       )
        clear_btn.place(relx=0.13, rely=0.29)
#==============================================================================================================      

        #REFRESH BUTTON 
        def refresh():
            query = "SELECT `ProductID`, `ProductName`, `Category`, `Price`, `QuantityOnHand`, `Current_stock` FROM `products`"
            my_db.execute(query)
            data = my_db.fetchall()

            table_data.clear()  
            table_data.extend([custom_headers] + data)
            table.update_values(table_data)
        
        refresh_btn= CTkButton(master=tabview.tab("Sell Products"),
                       width=100,
                       text="Refresh",
                       cursor="hand2",
                       command=refresh)
                       
        refresh_btn.place(relx=0.25, rely=0.29)
#==============================================================================================================
        
        separate_label= CTkLabel(master=tabview.tab("Sell Products"),
                              text="PRODUCT LIST",
                              font=("Tahoma",10,"bold"),
                              text_color="#222831",
                              fg_color="transparent",
                              width=612,
                              height=25,
                              corner_radius=5
                              )
                              
        separate_label.place(relx=0.01, rely=0.38)
       
#==============================================================================================================
        global highlighted_row
        highlighted_row = None
      
        def users(cell):
            global highlighted_row
            global price_product

            if cell["row"] == 0 or cell["row"] >= len(table_data):
                return

            if highlighted_row is not None:
                table.edit_row(highlighted_row, fg_color=table.fg_color if highlighted_row % 2 == 0 else table.fg_color2)

            if cell["row"] != highlighted_row:
                table.edit_row(cell["row"], fg_color=table.hover_color)
                highlighted_row = cell["row"]
                product_id_index = custom_headers.index("ProductID")
                product_name_index = custom_headers.index("ProductName")
                price_index = custom_headers.index("Price")
                current_stock = custom_headers.index("Current_Stock")


                if cell["row"] < len(table_data):
                    price_product = table_data[cell["row"]][price_index]
                    product_name = table_data[cell["row"]][product_name_index]
                    global stock
                    stock = table_data[cell["row"]][current_stock]
                  
                    pname.delete(0, 'end')
                    pname.insert(0, product_name)
                else:
                    highlighted_row = None
            else:
                highlighted_row = None

       

        global custom_headers
        custom_headers = ["ProductID", "ProductName", "Category", "Price","Old_Stock","Current_Stock"]

       
        query = "SELECT `ProductID`, `ProductName`, `Category`, `Price`, `QuantityOnHand`, `Current_stock` FROM `products`"
        my_db.execute(query)
        data =  my_db.fetchall()

        table_data= [custom_headers]+ data
#==============================================================================================================
     
       
        table_frame = CTkScrollableFrame(tabview.tab("Sell Products"), width=590,height=250,fg_color="#FFFFFF",
                                         border_color="#125B50",border_width=0.5)
        table_frame.place(relx=0.01, rely=0.45)
        
        table = CTkTable(master=table_frame,row=0, column=6,
                         colors=["#FFF7F1", "#EAEAEA"],
                         values= table_data,
                         header_color=("#E5C287"),
                         font=("Tahoma",12),
                         width=10,
                         height=20,
                         padx=0.5,
                         justify="left",
                         command=users
                         )                       
        table.pack(expand=True, fill="both")


        label_receipt= CTkLabel(master=tabview.tab("Sell Products"),
                              text="RECEIPT PREVIEW",
                              font=("Tahoma",10,"bold"))
        label_receipt.place(relx=0.78, rely=0.04)

#==============================================================================================================
        receipt_frame = CTkFrame(tabview.tab("Sell Products"), width=400,height=400,fg_color="#FFFFFF",
                                         border_color="#125B50",border_width=1)
        receipt_frame.place(relx=0.64, rely=0.09)
        global receipt_headers
        receipt_headers = ["ProductName", "Quantity", "Price","Total"]

       
        treeview = ttk.Treeview(master=receipt_frame,columns=receipt_headers, show="headings", height=28)

        for header in receipt_headers:
            treeview.heading(header, text=header)
        treeview.column("ProductName", width=150) 
        treeview.column("Quantity", width=150) 
        treeview.column("Price", width=120) 
        treeview.column("Total", width=100) 
        style = ttk.Style()
        style.configure("Treeview.Heading", font=("Tahoma", 12))
        style.configure("Treeview", font=("Tahoma", 12))         
        treeview.pack() 

    
#==============================================================================================================
        
        logout= CTkButton(master=tabview.tab("Sell Products"),
                       width=90,
                       text="Log Out",
                       cursor="hand2",
                      )
                       
        logout.place(relx=0.90, rely=0)

        print_btn= CTkButton(master=tabview.tab("Sell Products"),
                       width=120,
                       text="Print receipt",
                       cursor="hand2",
                       command=on_print_button_click
                       )
                       
        print_btn.place(relx=0.65, rely=0.89)

        gtotal_label=CTkLabel(master=tabview.tab("Sell Products"),
                        text="GRAND TOTAL:",
                        font=("Tahoma",10,"bold"),
                        text_color="#222831")
        gtotal_label.place(relx=0.82,rely=0.89)

        gtotal= CTkEntry(master=tabview.tab("Sell Products"),
                        width=80,
                        border_width=0,
                        placeholder_text="0",
                        
                        state="normal",
                        text_color="#222831",
                        )
        gtotal.place(relx=0.90,rely=0.89)

       

        
    


def main():
    root = CTk()
    root.title("Seller Dashboard")  
    app =  Seller_dash_App(root)
    root.mainloop()


if __name__ == "__main__":
    main()
