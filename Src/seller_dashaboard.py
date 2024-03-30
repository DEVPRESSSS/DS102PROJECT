                   
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
        self.master.minsize(1034, 600)



        def show_error():
             CTkMessagebox(title="Invalid Input", message="Please put value in Quantity textbox", icon="cancel")

        
#==============================================================================================================      

        def ask_question(price_product, current_name, result):
            msg = CTkMessagebox(title="Confirmation", message="Do you want to process this transaction?",
                                icon="question", option_1="No", option_2="Yes")
            response = msg.get()
            
            if response == "Yes":
                total = Decimal(result)
                new_content = f"{current_name}\t{price_product}\t{total}\n"
                
                existing_content = [line for line in preview_receipt.cget("text").splitlines()[3:] if line.strip() and not line.startswith("Grand Total:")]
                            
                updated_dynamic_content = '\n'.join(existing_content + [new_content])             
           
                grand_total = sum(Decimal(line.split('\t')[2]) for line in existing_content) + total
                
                updated_receipt_text = "===========BODENGHARDWARE============\n" \
                                    "================Receipt===============\n" \
                                    "ProductName\tPrice\tTotal\n" + \
                                    updated_dynamic_content
                
                updated_receipt_text += f"\nGrand Total:\t\t{grand_total}\n"
                
                preview_receipt.configure(text=updated_receipt_text)
            else:
                print("Click 'No' to cancel!")

#==============================================================================================================

        frame = CTkFrame(
            master=self.master,
            fg_color="#FFFFFF",
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
                            fg_color="#FFFFFF")
        tabview.place(relx=0.025,rely=0.01)

        tabview.add("tab 1") 
        tabview.rename("tab 1","Sell Products")
        tabview.add("tab 2")  
        tabview.rename("tab 2","Sales History")
        tabview.add("tab 3")
        tabview.rename("tab 3","View products")
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

        label_pic= CTkLabel(master=tabview.tab("Sell Products"),
                              text="Product Picture:",
                              font=("Tahoma",10,"bold"),
                              text_color="#125B50")
        label_pic.place(relx=0.532, rely=0.04)

        Image_frame= CTkFrame(master=tabview.tab("Sell Products"),
                              height=90,
                              width=90,
                              border_color="#125B50",
                              border_width=1,
                              fg_color="#FFFFFF")
        
        Image_frame.place(relx=0.53, rely=0.09)



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
                              fg_color="#125B50",
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
            current_name=pname.get()
            qtys = qty.get()

            try:
               
                qtys_decimal = Decimal(qtys)
            except:
               
                show_error()
                return
            if qtys is not None:

              result= price_product * qtys_decimal
              ask_question( price_product, current_name,result)
              
            else:
                show_error()
           
#==============================================================================================================      

        qty = CTkEntry(master=tabview.tab("Sell Products"),
                            border_color="#125B50",
                            border_width=1,
                            width=200
                        )
        qty.place(relx=0.01, rely=0.2)
       
        sell= CTkButton(master=tabview.tab("Sell Products"),
                       width=120,
                       text="Sell",
                       cursor="hand2",
                       fg_color="#125B50",
                       command=qty_count )
        sell.place(relx=0.01, rely=0.29)

        clear_btn= CTkButton(master=tabview.tab("Sell Products"),
                       width=120,
                       text="Clear",
                       cursor="hand2",
                       fg_color="#FF6363" )
        clear_btn.place(relx=0.17, rely=0.29)
#==============================================================================================================      

         #REFRESH BUTTON 
        def refresh():
            # table.delete_rows(list(range(1, len(table_data))))

            query = "SELECT * FROM products"
            my_db.execute(query)
            data = my_db.fetchall()

            table_data.clear()  
            table_data.extend([custom_headers] + data)
            table.update_values(table_data)
#==============================================================================================================
            

            
            

        refresh_btn= CTkButton(master=tabview.tab("Sell Products"),
                       width=120,
                       text="Refresh",
                       cursor="hand2",
                       fg_color="#125B50",
                       command=refresh)
                       
        refresh_btn.place(relx=0.33, rely=0.29)

        def combobox_callback(choice):
            print("combobox dropdown clicked:", choice)

        combobox_var = StringVar(value="option 2")
        combobox = CTkComboBox(master=tabview.tab("Sell Products"), values=["option 1", "option 2"],
                               
                                            command=combobox_callback, width=90, variable=combobox_var)
        combobox_var.set("option 2")

        combobox.place(relx=0.49, rely=0.29)


        filter_btn= CTkButton(master=tabview.tab("Sell Products"),
                              width=70,
                              text="Filter",
                              fg_color="#FF6363",
                              text_color="#FFFFFF")
        filter_btn.place(relx=0.59, rely=0.29)
        
        separate_label= CTkLabel(master=tabview.tab("Sell Products"),
                              text="Product Table Preview",
                              
                              text_color="#FFFFFF",
                              fg_color="#125B50",
                              width=612,
                              height=25,
                              corner_radius=5
                              )
                              
        separate_label.place(relx=0.01, rely=0.38)
       
        #TABLE CLICK FUNCTIONALITY>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

        global highlighted_row
        highlighted_row = None
        def users(cell):
                global highlighted_row

                if cell["row"]==0:
                     return 
                if highlighted_row is not None:
                    table.edit_row(highlighted_row, fg_color=table.fg_color if highlighted_row % 2 == 0 else table.fg_color2)
                if cell["row"] != highlighted_row:
                    table.edit_row(cell["row"], fg_color=table.hover_color)
                    highlighted_row = cell["row"]
                    price_index = custom_headers.index("Price")
                    global price_product
                    price_product = table_data[cell["row"] + 1][price_index] 
                    
                    if cell["row"] + 1 < len(table_data):
                        
                        product_name = table_data[cell["row"] + 1][1]
                        pname.delete(0, 'end')
                        pname.insert(0, product_name)
                else:
                    highlighted_row = None
        global custom_headers
        custom_headers = ["ProductID", "ProductName", "Description", "Category", "Price","Current Stock"]

       
        query = "SELECT * FROM products"
        my_db.execute(query)
        data =  my_db.fetchall()

        table_data= [custom_headers]+ data
      
       
        table_frame = CTkScrollableFrame(tabview.tab("Sell Products"), width=590,height=250,fg_color="#FFFFFF",
                                         border_color="#125B50",border_width=0.5)

        table = CTkTable(master=table_frame, row=0, column=6,
                         colors=["#F8F8F8", "#EAEAEA"],
                         values= table_data,
                         header_color=("#E5C287"),
                         font=("Tahoma",10,"bold"),
                         width=10,
                         height=20,
                         padx=0.5,
                         justify="left",
                         command=users,
                         
                         )

       
        table.pack()

        table_frame.place(relx=0.01, rely=0.45)
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>


        label_receipt= CTkLabel(master=tabview.tab("Sell Products"),
                              text="RECEIPT PREVIEW",
                              font=("Tahoma",10,"bold"),
                              text_color="#125B50")
        label_receipt.place(relx=0.78, rely=0.04)

        receipt_frame= CTkFrame(master= tabview.tab("Sell Products"),
                                height=300,
                                width=300,
                                border_width=1,
                                border_color="#125B50",
                                fg_color="#FFFFFF")
        receipt_frame.place(relx=0.672, rely=0.09)
        preview_receipt= CTkLabel(master= receipt_frame,
                              text="",
                              font=("Tahoma",10,"bold"),
                              text_color="#125B50")
        preview_receipt.place(relx=0.025, rely=0.02)

       


def main():
    root = CTk()
    root.title("Seller Dashboard")  
    app =  Seller_dash_App(root)
    root.mainloop()
    


if __name__ == "__main__":
    main()
