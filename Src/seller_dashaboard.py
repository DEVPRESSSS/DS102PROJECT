                   
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

        search_btn= CTkButton(master=tabview.tab("Sell Products"),
                              width=70,
                              text="Search",
                              cursor="hand2",
                              fg_color="#125B50"
                             
                              )
        
        search_btn.place(relx=0.226, rely=0.09)

        label_qty= CTkLabel(master=tabview.tab("Sell Products"),
                              text="Quantity:",
                              font=("Tahoma",10,"bold"),
                              text_color="#125B50")
        label_qty.place(relx=0.01, rely=0.15)

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
                       fg_color="#125B50" )
        sell.place(relx=0.01, rely=0.29)

        clear_btn= CTkButton(master=tabview.tab("Sell Products"),
                       width=120,
                       text="Clear",
                       cursor="hand2",
                       fg_color="#FF6363" )
        clear_btn.place(relx=0.17, rely=0.29)

        refresh_btn= CTkButton(master=tabview.tab("Sell Products"),
                       width=120,
                       text="Refresh",
                       cursor="hand2",
                       fg_color="#125B50" )
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
                        #  header_color=("#FAF5E4"),
                         header_color=("#E5C287"),
                         font=("Tahoma",10,"bold"),
                         width=10,
                         height=20,
                         padx=0.5,
                         justify="left"
                         
                         )
        
      
        row_selector = CTkTableRowSelector(table)
        
        table.pack()
        table_frame.place(relx=0.01, rely=0.45) 

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
    

       


def main():
    root = CTk()
    root.title("Seller Dashboard")  
    app =  Seller_dash_App(root)
    root.mainloop()
    


if __name__ == "__main__":
    main()
