                   
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
from decimal import Decimal
from pdf2image import convert_from_bytes
from PyPDF2 import PdfWriter, PdfReader
import io
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Image, Paragraph, Spacer
from reportlab.lib.units import inch







my_connection= mysql.connector.connect(


    host="localhost",
    user="root",
    password="",
    database="hardware_db"
  
)
my_db= my_connection.cursor()

class Seller_dash_App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("1034x600")
        self.minsize(1034, 600)
        self.setup_seller_dashboard()
        self.center_window()
    def back_to_login(self):
            self.withdraw()
            subprocess.Popen(["python", r"D:\\DS102PROJECT\\Src\\Login.py"])
    def center_window(self):
        # Get the width and height of the window
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        window_width = 1034  # Width of the window
        window_height = 600  # Height of the window

        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2

        # Set the window position
        self.geometry("+{}+{}".format(x, y))
    def setup_seller_dashboard(self):
        

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
 

        def ask_question(current_name, price_product, subtotal, quantity):
            msg = CTkMessagebox(title="Confirmation", message="Do you want to process this transaction?",
                                icon="question", option_1="No", option_2="Yes")
            response = msg.get()

            if response == "Yes":
                total = Decimal(subtotal)
                # Define column widths
                column_widths = [20, 10, 5, 10]  # Adjust as needed

                # Format the content for each column
                formatted_content = [
                    f"{current_name[:column_widths[0]]:<{column_widths[0]}}",
                    f"{price_product:^{column_widths[1]}}",
                    f"{quantity:^{column_widths[2]}}",
                    f"{total:^{column_widths[3]}}",
                ]

                new_content = '\t'.join(formatted_content) + '\n'

                existing_content = [line for line in preview_receipt.cget("text").splitlines()[3:] if
                                    line.strip() and not line.startswith("Grand Total:")]

                updated_dynamic_content = '\n'.join(existing_content + [new_content])

                grand_total = sum(Decimal(line.split('\t')[2]) for line in existing_content) + total

                # Format the receipt text
                updated_receipt_text = "===========BODENGHARDWARE============\n" \
                                    "================Receipt===============\n" \
                                    "ProductName\tPrice\tQty\tTotal\n" + \
                                    updated_dynamic_content

                updated_receipt_text += f"\nGrand Total:\t\t{grand_total}\n"

                preview_receipt.configure(text=updated_receipt_text)

                update_stock(current_name, quantity)
                clear()
            else:
                print("Click 'No' to cancel!")


#==============================================================================================================


        frame = CTkFrame(
            master=self.master,
            fg_color="#F4F5F6",
            border_color="#1B770C",
            border_width=1,
            width=1000,
            height=580,
            corner_radius=20
           
        )
        frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

      
        tabview =CTkTabview(master=frame,
                            width=950,
                            height=550,
                            fg_color="#F4F5F6")
        tabview.place(relx=0.025,rely=0.01)

        tabview.add("tab 1") 
        tabview.add("tab 2") 

        tabview.rename("tab 1","Sell Products")
        tabview.rename("tab 2","Sales reports")

        tabview.set("Sell Products")


        label_pname= CTkLabel(master=tabview.tab("Sell Products"),
                              text="Product Name:",
                              font=("Tahoma",10,"bold"),
                              text_color="#125B50")
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
               
               query= "SELECT * FROM products where ProductName LIKE %s OR Price LIKE %s"
               value= ("%" + search + "%","%" + search + "%")
            else:
                query = "SELECT * FROM sellers_tbl"
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
                              text="Quantity:",
                              font=("Tahoma",10,"bold"),
                              text_color="#125B50")
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
                    print(stock)
                    show_quantity()
                else:
                    subtotal = Decimal(price_product) * int(quantity)
                    ask_question(product_name, price_product,  subtotal, quantity)
            else:
                show_error_in()
                return
            
            
           
           
#==============================================================================================================  
        def create_pdf_receipt():
           
            # pdf= FPDF("P","mm","A4")
            # w=210
            # h=33
            # pdf.set_font("Arial","B",12)
            # pdf.add_page()
            # pdf.cell(60,7,"ProductName", border=1)
            # pdf.cell(60,7,"ProductName", border=1)
            # pdf.cell(60,7,"ProductName", border=1)

            
            # pdf.output("Receipt.pdf")
            pass
        
        
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
                       width=120,
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
                       width=120,
                       text="Clear",
                       cursor="hand2",
                       command=clear
                       )
        clear_btn.place(relx=0.17, rely=0.29)
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
                       width=120,
                       text="Refresh",
                       cursor="hand2",
                       command=refresh)
                       
        refresh_btn.place(relx=0.33, rely=0.29)
#==============================================================================================================
        
        separate_label= CTkLabel(master=tabview.tab("Sell Products"),
                              text="Product Table Preview",
                              
                              text_color="#FFFFFF",
                              fg_color="#125B50",
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
                    print(stock)
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
                         colors=["#F8F8F8", "#EAEAEA"],
                         values= table_data,
                         header_color=("#E5C287"),
                         font=("Tahoma",10,"bold"),
                         width=10,
                         height=20,
                         padx=0.5,
                         justify="left",
                         command=users
                         )                       
        table.pack(expand=True, fill="both")


        label_receipt= CTkLabel(master=tabview.tab("Sell Products"),
                              text="RECEIPT PREVIEW",
                              font=("Tahoma",10,"bold"),
                              text_color="#125B50")
        label_receipt.place(relx=0.78, rely=0.04)

        receipt_frame= CTkFrame(master= tabview.tab("Sell Products"),
                                height=439,
                                width=300,
                                border_width=1,
                                border_color="#125B50",
                                fg_color="#FFFFFF")
        receipt_frame.place(relx=0.674, rely=0.09)
        preview_receipt= CTkLabel(master= receipt_frame,
                              text="",
                              font=("Tahoma",10,"bold"),
                              text_color="#125B50")
        preview_receipt.place(relx=0.025, rely=0.02)
        
        
        logout= CTkButton(master=tabview.tab("Sell Products"),
                       width=90,
                       text="Log Out",
                       cursor="hand2",
                       command=self.back_to_login)
                       
        logout.place(relx=0.90, rely=0)

        print_btn= CTkButton(master=tabview.tab("Sell Products"),
                       width=120,
                       text="Print receipt",
                       cursor="hand2",
                       command=create_pdf_receipt)
                       
        print_btn.place(relx=0.79, rely=0.91)
       
        # def export_to_pdf(self):
        #     file_path = filedialog.asksaveasfilename(defaultextension=".pdf")
        #     if file_path:
        #         doc = SimpleDocTemplate(file_path, pagesize=letter)

        #     # Add logo image
        #     logo_path = "C:/Users/russe/Downloads/433969516_942025734229990_8532999142125472888_n.png"  # Correct path to the logo image

        #     # Resize the logo image
        #     resized_logo_path = "resized_logo.png"
        #     self.resize_image(logo_path, resized_logo_path, width=1*inch, height=1*inch)

           
        #     cafe_info_text = [
        #         "HARDWARE POS",
        #         "S. DE OCAMPO ST BRYGY 143",
        #         "Sampaloc, Manila",
        #         "09078632798",
        #         "Date: " + datetime.now().strftime('%m-%d-%Y')  # Date now
        #     ]

        #     # Create a paragraph style
        #     cafe_info_style = ParagraphStyle('Title', fontSize=12, leading=14, alignment=1)

        #     # Create a Paragraph object
        #     cafe_info = Paragraph("<br />".join(cafe_info_text), cafe_info_style)

        #     # Extracting data from the treeview
        #     data = [[self.table.heading(col)["text"] for col in self.table["columns"][1:]]]  # Exclude the ID column
        #     data += [list(self.table.item(item, "values"))[1:] for item in self.table.get_children()]  # Exclude the ID column

        #     # Converting binary data to strings (if needed)
        #     data = [[str(cell, 'utf-8') if isinstance(cell, bytes) else cell for cell in row] for row in data]
        #     t = Table(data)
        #     t.setStyle(TableStyle([('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        #                            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        #                            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        #                            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        #                            ('GRID', (0, 0), (-1, -1), 1, colors.black)]))

        #     # Build content
        #     content = [Image(resized_logo_path), cafe_info, Spacer(1, 12), t]

        #     doc.build(content)
        #     messagebox.showinfo("Export to PDF", "PDF generated successfully!")
        #     subprocess.Popen([file_path], shell=True)


def main():
    # root = CTk()
    # root.title("Seller Dashboard")  
    app =  Seller_dash_App()
    app.mainloop()
    


if __name__ == "__main__":
    main()
