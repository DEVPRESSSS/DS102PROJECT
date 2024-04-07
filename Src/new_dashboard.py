                   
from customtkinter import CTk, CTkFrame, CTkButton, CTkImage, CTkLabel, CTkTabview, CTkEntry,CTkScrollableFrame
import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import tkinter
import customtkinter
from PIL import Image,ImageTk
from CTkTable import *
import mysql.connector
from mysql.connector import Error
from tkinter import messagebox,ttk
from tkinter import filedialog
import io





my_connection= mysql.connector.connect(


    host="localhost",
    user="root",
    password="",
    database="hardware_db"
  
)
my_db= my_connection.cursor()



class DashboardApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.setup_dashboard()
        self.geometry("1100x600")
        self.minsize(1100, 600)
        
      
    def setup_dashboard(self):
        


        frame = CTkFrame(
            master=self.master,
            fg_color="#FFFFFF",
            width=1100,
            height=600,
            
        )
        frame.pack(expand=True, fill="both")
        tabview =CTkTabview(master=frame,
                            width=1100,
                            height=600,
                            segmented_button_selected_color="#401F71",
                            fg_color="#FFFFFF",
                            text_color="#FFFFFF"
                            )
        tabview.pack(expand=True, fill="both")

        tabview.add("tab 1") 
        tabview.rename("tab 1","Products")
        tabview.add("tab 2")  
        tabview.rename("tab 2","Sellers")
        tabview.add("tab 3")
        tabview.rename("tab 3","Purchase")
        tabview.add("tab 4")
        tabview.rename("tab 4","Product Category")
        tabview.add("tab 5")
        tabview.rename("tab 5","View Chart")
        tabview.add("tab 6")
        tabview.rename("tab 6","Manage profile")
        tabview.set("Products")

#<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<PRODUCT PHASE>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
       
        frame= CTkFrame(master=tabview.tab("Products"),
                    
                fg_color="#FFFFFF", 
                border_color="#FFCC70",
                width=1000,
                height=600,
                corner_radius=20,
                border_width=0
                )
        frame.place(relx=0.5, rely=0.5,anchor=tkinter.CENTER)

        
        reports= CTkFrame(master=frame,
                            height=250,
                            width=968,
                            fg_color="#EEEEEE", 
                            
                            )
        reports.place(relx=0.01,rely=0.048)
        
        label_for_pname= CTkLabel(
                        master=reports,
                        font=("Tahoma",12,"bold"),
                        text_color="#222831",
                        text="Product name:"

                        )
        label_for_pname.place(relx=0.05,rely=0.04)

        #Validations for entriess>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

        def on_validate(char, entry_value):
        
            return not char.isdigit() and len(entry_value) < 50 or char == ""

        #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

        product_name= CTkEntry(
                        master=reports,
                        border_width=2,
                        width=200,
                        validate="key", 
                        validatecommand=(reports.register(on_validate), "%S", "%P"),
                        font=("Tahoma", 12)
                        )
        product_name.place(relx=0.05, rely=0.18)


        description_label= CTkLabel(
                        master=reports,
                        font=("Tahoma",12,"bold"),
                        text_color="#222831",              
                        text="Description:"

                        )
        description_label.place(relx=0.05,rely=0.45)


        #Validations for entriess>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        def on_validate(char, entry_value):
            return char.isdigit() and len(entry_value) < 11 or char == ""
        #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>


        description= CTkEntry(
                        master=reports,
                        border_width=2,
                        width=200,
                        font=("Tahoma", 12),
                        )
        description.place(relx=0.05, rely=0.6)


        #It will clear the buttons everytime i call the function>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        def clear_btn():
            product_name.delete(0,'end')
            description.delete(0,'end')
            price.delete(0,'end')
            qty.delete(0,'end')
#===================================================================================================================

        def insert_image(product_id, selected_file_path):

            try:
                with open(selected_file_path, 'rb') as file:
                    image_blob = file.read()

                query = "INSERT INTO productpicture (ProductID, productPicture) VALUES (%s, %s)"
                values = (product_id, image_blob)
                my_db.execute(query, values)
                my_connection.commit()

            except Error as e:
                messagebox.showerror("Error", f"Failed to insert picture: {e}")
 #===================================================================================================================       
        def create_record():
            
            pname = product_name.get()
            pdescription = description.get()
            category = combobox.get()
            pprice = price.get()
            pqty = qty.get()

            if not all([pname, pdescription, category, pprice, pqty ]):
                messagebox.showerror("Error", "All fields are required!")
                return
            
           
            

            query = "INSERT INTO products (ProductName, Description, Category, Price, QuantityOnHand) VALUES ( %s, %s, %s, %s, %s)"
            values = (pname, pdescription, category, pprice, pqty )

            try:
                my_db.execute(query, values)
                my_connection.commit()
                
                messagebox.showinfo("Success", "Record created successfully!")
                product_id = my_db.lastrowid
               
                insert_image(product_id, file_path_image)
                print(file_path_image)
                refresh()
        
                
                clear_btn()
                
               
            except mysql.connector.Error as err:
                messagebox.showerror("Error", "Failed to create record:Email is already exist")
#===================================================================================================================
        add= CTkButton(
                        master=reports,
                        text="Add",
                        width=94,
                        font=("Tahoma",12,"bold"),
                        cursor="hand2",
                        command=create_record
                        )
        add.place(relx=0.05, rely=0.79)
#===================================================================================================================
        def refresh():
            query = "SELECT `ProductID`, `ProductName`, `Description`, `Category`, `Price`, `QuantityOnHand`, `Current_stock` FROM `products`"
            my_db.execute(query)
            data = my_db.fetchall()

            table_data.clear()  
            table_data.extend([custom_headers] + data)
            table.update_values(table_data)
#===================================================================================================================
       


        update= CTkButton(
                        master=reports,
                        text="Update",
                        width=94,
                        font=("Tahoma",12,"bold"),
                        cursor="hand2",
                        
                        )
        update.place(relx=0.16, rely=0.79)



        label_for_cat= CTkLabel(
                        master=reports,
                        font=("Tahoma",12,"bold"),
                        text_color="#222831",
                        text="Category:"

                        )
        label_for_cat.place(relx=0.37,rely=0.04)

        #COMBOBOX PHASE

        def populate_combobox():
            query = "SELECT CategoryName FROM category"

            try:
                my_db.execute(query)
                categories_list = my_db.fetchall()
                return [category[0] for category in categories_list]       
                
            except mysql.connector.Error as err:
                messagebox.showerror("Error", "Error in loading product count", err)



        def combobox_callback(choice):
            print(choice)

        cat= populate_combobox()
        combobox = customtkinter.CTkComboBox(master=reports, 
                                            values=cat,
                                            width=198,
                                            command=combobox_callback
                                            )
        combobox.set("Choose category")
        combobox.place(relx=0.37, rely=0.17 )



        #<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

        label_for_price= CTkLabel(
                        master=reports,
                        font=("Tahoma",12,"bold"),
                        text_color="#222831",
                        text="Price:"

                        )
        label_for_price.place(relx=0.37,rely=0.45)



        price= CTkEntry(
                        master=reports,
                        width=200,
                        font=("Tahoma", 12)
                        )
        price.place(relx=0.37, rely=0.6)

#<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<,IMAGE CHOOSE>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

        def choose_file():
            global file_path_image
            selected_file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg;*.png")])
            if selected_file_path:
                display_image(selected_file_path)
                file_path_image= selected_file_path
               
           
       
        def display_image(file_path):
            label_width = image_label.winfo_width()
            label_height = image_label.winfo_height()

            img = Image.open(file_path)
            img = img.resize((label_width, label_height)) 
            img = CTkImage(img, size=(label_width, label_height))  
            image_label.configure(image=img)
            image_label.image =  img
            
 #<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
       

        image_label = CTkLabel(
            master=reports,
            height=90,
            width=90,
            text="",
            fg_color="#FFFFFF",
            
            )
        image_label.place(relx=0.70, rely=0.29)

        file= CTkButton(
                        master=reports,
                        text="Choose File",
                        width=94,
                        font=("Tahoma",12,"bold"),
                        cursor="hand2",
                        command=choose_file
                        )
        file.place(relx=0.7, rely=0.64)


        clear= CTkButton(
                        master=reports,
                        text="Clear",
                        width=94,
                        font=("Tahoma",12,"bold"),
                        cursor="hand2",
                        command=clear_btn
                        )
        clear.place(relx=0.37, rely=0.79)


        #IT will delete the specific record>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        def delete_record():
            try:
            
                if pID is not None:
                
                    confirmation = messagebox.askyesno("Confirmation", "Are you sure you want to delete this record?")

                    if confirmation:
                    
                        query = "DELETE FROM products WHERE ProductID= %s"
                        values = (pID,)
                        my_db.execute(query, values)
                        my_connection.commit()
                        messagebox.showinfo("Success", "Record deleted successfully!")
                        table.delete_row(pID)
                        clear_btn()
                        refresh()
                
                else:
                    messagebox.showerror("Error", "Failed to delete the record")

            except mysql.connector.Error as err:
                messagebox.showerror("Error", f"Failed to update the record: {err}")
        delete= CTkButton(
                        master=reports,
                        text="Delete",
                        width=94,
                        font=("Tahoma",12,"bold"),
                        cursor="hand2",
                        command=delete_record
                       
                        )
        delete.place(relx=0.478, rely=0.79)


        search= CTkEntry(
                        master=reports,
                        width=150,
                        placeholder_text="Search here....",
                        font=("Tahoma", 12)
                )

        search.place(relx=0.68, rely=0.79)

#<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<SEARCH SELLERS>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
       

        search_btn= CTkButton(
                        master=reports,
                        text="Search",
                        width=80,
                        hover_color="#87A922",
                        font=("Tahoma",12,"bold"),
                        cursor="hand2",
                     
                        
            
                        )
        search_btn.place(relx=0.84, rely=0.79)
        qty_label= CTkLabel(
                        master=reports,
                        font=("Tahoma",12,"bold"),
                        text_color="#222831",
                        text="Quantity:"

                        )
        qty_label.place(relx=0.68,rely=0.04)
        qty= CTkEntry(
                        master=reports,
                        width=200,
                        font=("Tahoma", 12)
                        )
        qty.place(relx=0.68, rely=0.18)
#=====================================================================================================================
        global highlighted_row
        highlighted_row = None
      
        def users(cell):
            global highlighted_row, pID
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
                description_index = custom_headers.index("Description")
                category_index = custom_headers.index("Category")
                price_index = custom_headers.index("Price")
                old_stock = custom_headers.index("QuantityOnHand")


                if cell["row"] < len(table_data):
                    
                    pID=  table_data[cell["row"]][product_id_index]
                    
                    product_names = table_data[cell["row"]][product_name_index]
                    descriptions= table_data[cell["row"]][description_index]
                    categories= table_data[cell["row"]][category_index]
                    price_product = table_data[cell["row"]][price_index]
                    product_stock = table_data[cell["row"]][ old_stock]

                    product_name.delete(0,'end')
                    product_name.insert(0,product_names)
                    description.delete(0,'end')
                    description.insert(0,descriptions)
                    combobox.set(categories)
                    price.delete(0,'end')
                    price.insert(0,price_product)
                    qty.delete(0,'end')
                    qty.insert(0,product_stock)

                    product_picture = get_product_picture(pID)
                    if product_picture is not None:
                       display_images(product_picture)
                  
                else:
                    highlighted_row = None
            else:
                highlighted_row = None

        

        global custom_headers
        custom_headers = ["ProductID", "ProductName", "Description", "Category", "Price","Old_Stock","Current_Stock"]

       
        query = "SELECT `ProductID`, `ProductName`, `Description`, `Category`, `Price`, `QuantityOnHand`, `Current_stock` FROM `products`"
        my_db.execute(query)
        data =  my_db.fetchall()

        table_data= [custom_headers]+ data
       
       
        table_frame = CTkScrollableFrame(master=frame, width=930,height=250,fg_color="#FFFFFF",
                                         border_color="#125B50")
        table_frame.place(relx=0.01, rely=0.5)
        
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

        def get_product_picture(product_id):
            

            try:
                query = "SELECT `productPicture` FROM `productpicture` WHERE `productID`= %s"
                values = (product_id,)
                my_db.execute(query, values)
                data = my_db.fetchone()
                return data[0] if data else None
            except Exception as e:
                print("Error retrieving product picture:", e)
                return None
                    
            
        def display_images(product_picture):
                if product_picture: 
                    try:
                        pil_image = Image.open(io.BytesIO(product_picture))

                        label_width = image_label.winfo_width()
                        label_height = image_label.winfo_height()
                        pil_image = pil_image.resize((label_width, label_height))

                        ctk_image = CTkImage(pil_image, size=(label_width, label_height))

                        image_label.configure(image=ctk_image)
                        image_label.image = ctk_image
                    except Exception as e:
                        print("Error displaying image:", e)
                else:
                    print("No image found for product.")
                

      
            
#<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<END OF PRODUCT PHASE>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>






















#<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<SELLER PHASE>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        frame2= CTkFrame(master=tabview.tab("Sellers"),
                    
                fg_color="#FFFFFF", 
                border_color="#FFCC70",
                width=1100,
                height=600,
                corner_radius=20,
                border_width=0
                )
        frame2.pack(expand=True,fill="both")

      
      
        reports1= CTkFrame(master=frame2,
                            height=155,
                            width=720,
                            border_width=0,
                            # border_color="#9391E6",
                            fg_color="#FFFFFF"
                            )
        reports1.place(relx=0.25,rely=0.048)
        label_for_name= CTkLabel(
                        master=reports1,
                        font=("Tahoma",10,"bold"),
                        text_color="#1B770C",
                        text="Fullname:"

                        )
        label_for_name.place(relx=0.05,rely=0.04)

        #Validations for entriess>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

        def on_validate(char, entry_value):
        
            return not char.isdigit() and len(entry_value) < 50 or char == ""


        def on_limit(char, entry_value):
            return len(entry_value) < 60 and char.isalnum() or char == ""


        #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

        full_name= CTkEntry(
                        master=reports1,
                        border_color="#1B770C",
                        border_width=1,
                        width=200,
                        validate="key", 
                        validatecommand=(reports.register(on_validate), "%S", "%P"),
                        font=("Tahoma", 10)
                        )
        full_name.place(relx=0.05, rely=0.18)


        label_for_contact= CTkLabel(
                        master=reports1,
                        font=("Tahoma",10,"bold"),
                        text_color="#1B770C",
                        text="Contact:"

                        )
        label_for_contact.place(relx=0.05,rely=0.45)


        #Validations for entriess>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        def on_validate(char, entry_value):
            return char.isdigit() and len(entry_value) < 11 or char == ""
        #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>


        contact= CTkEntry(
                        master=reports1,
                        border_color="#1B770C",
                        border_width=1,
                        width=200,
                        font=("Tahoma", 10),
                        validate="key",
                        validatecommand=(frame.register(on_validate), "%S", "%P"),
                        )
        contact.place(relx=0.05, rely=0.6)


        #It will clear the buttons everytime i call the function>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        def clear_btn():
            full_name.delete(0,'end')
            contact.delete(0,'end')
            address.delete(0,'end')
            email.delete(0,'end')
            password1.delete(0,'end')

        #INSERT FUNCTION TO DATABASE>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

        def create_record():
            name1 = full_name.get()
            contacts1 = contact.get()
            addresss1 = address.get()
            emails1 = email.get()
            passwords1 = password1.get()

            if not all([name1, contacts1, addresss1, emails1,passwords1]):
                messagebox.showerror("Error", "All fields are required!")
                return

            query = "INSERT INTO sellers_tbl (fullname, contact, address, email, password) VALUES ( %s, %s, %s, %s, %s)"
            values = (name1, contacts1, addresss1, emails1, passwords1)

            try:
                my_db.execute(query, values)
                my_connection.commit()
                messagebox.showinfo("Success", "Record created successfully!")
             
                clear_btn()
                

            except mysql.connector.Error as err:
                messagebox.showerror("Error", "Failed to create record:Email is already exist")

        add= CTkButton(
                        master=reports1,
                        text="Add",
                        border_color="#1B770C",
                        border_width=1,
                        fg_color="#1B770C",
                        width=94,
                        hover_color="#87A922",
                        font=("Tahoma",10,"bold"),
                        cursor="hand2",
                        command=create_record
                        )
        add.place(relx=0.05, rely=0.79)

        #Update the selected row>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

        


        update= CTkButton(
                        master=reports1,
                        text="Update",
                        border_color="#4D606E",
                        border_width=1,
                        fg_color="#4D606E",
                        width=94,
                        hover_color="#3FBAC2",
                        font=("Tahoma",10,"bold"),
                        cursor="hand2",
                  
                        )
        update.place(relx=0.2, rely=0.79)



        label_for_address= CTkLabel(
                        master=reports1,
                        font=("Tahoma",10,"bold"),
                        text_color="#1B770C",
                        text="Address:"

                        )
        label_for_address.place(relx=0.37,rely=0.04)
        address= CTkEntry(
                        master=reports1,
                        border_color="#1B770C",
                        border_width=1,
                        width=200,
                        font=("Tahoma", 10),
                        validate="key", 
                        validatecommand=(reports.register(on_limit), "%S", "%P"),
                        )
        address.place(relx=0.37, rely=0.18)


        label_for_email= CTkLabel(
                        master=reports1,
                        font=("Tahoma",10,"bold"),
                        text_color="#1B770C",
                        text="Email:"

                        )
        label_for_email.place(relx=0.37,rely=0.45)



        email= CTkEntry(
                        master=reports1,
                        border_color="#1B770C",
                        border_width=1,
                        width=200,
                        font=("Tahoma", 10)
                        )
        email.place(relx=0.37, rely=0.6)
        clear= CTkButton(
                        master=reports1,
                        text="Clear",
                        border_color="#D37676",
                        border_width=1,
                        fg_color="#D37676",
                        width=94,
                        hover_color="#EBC49F",
                        font=("Tahoma",10,"bold"),
                        cursor="hand2",
                        command=clear_btn
                        )
        clear.place(relx=0.37, rely=0.79)


        #IT will delete the specific record>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>


        
        #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>..

        delete= CTkButton(
                        master=reports1,
                        text="Delete",
                        border_color="#BF3131",
                        border_width=1,
                        fg_color="#BF3131",
                        width=94,
                        hover_color="#EBC49F",
                        font=("Tahoma",10,"bold"),
                        cursor="hand2",
                       
                        )
        delete.place(relx=0.52, rely=0.79)


        search= CTkEntry(
                        master=reports1,
                        border_color="#1B770C",
                        border_width=1,
                        width=150,
                        placeholder_text="Search here....",
                        font=("Tahoma", 10)
                )

        search.place(relx=0.68, rely=0.79)


       
        search_btn= CTkButton(
                        master=reports1,
                        text="Search",
                        border_color="#1B770C",
                        border_width=1,
                        fg_color="#1B770C",
                        width=60,
                        hover_color="#87A922",
                        font=("Tahoma",10,"bold"),
                        cursor="hand2",
                        
            
                        )
        search_btn.place(relx=0.89, rely=0.79)
        password_label= CTkLabel(
                        master=reports1,
                        font=("Tahoma",10,"bold"),
                        text_color="#1B770C",
                        text="Password:"

                        )
        password_label.place(relx=0.68,rely=0.04)
       

        password1= CTkEntry(
                        master=reports1,
                        border_color="#1B770C",
                        border_width=1,
                        show="*",
                        width=200,
                        font=("Tahoma", 10)
                        )
        password1.place(relx=0.68, rely=0.18)

        def checkbox_events():
            global password1
            
            if check_var1.get() == "on":
                password1.configure(show="")
            else:
                password1.configure(show="*")
          


        check_var1 = customtkinter.StringVar(value="off")
        checkbox1 = customtkinter.CTkCheckBox(master=reports1, text="show password", command=checkbox_events,
                                            variable=check_var1, onvalue="on", offvalue="off",checkbox_height=15, checkbox_width=15)

        checkbox1.place(x=561, y=65)

        refreshs=CTkButton(master=frame2,
                        
                        text="Refresh",
                        border_color="#1B770C",
                        border_width=1,
                        fg_color="#1B770C",
                        width=60,
                        hover_color="#87A922",
                        font=("Tahoma",10,"bold"),
                        cursor="hand2",
                      
                        )

        refreshs.place(relx=0.88,rely=0.33)


       
        #Table creation>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        
        styles = ttk.Style()
        font_size = 12
        header_color = "lightblue"
        styles.configure("Treeview.Heading", font=("Tahoma", font_size),background=header_color)
        styles.configure("Treeview", font=("Tahoma", 12))
        tree1 = ttk.Treeview(frame2, style="Treeview")

        tree1["columns"] = ("seller_id","fullname", "contact", "address", "email", "password")
        tree1.bind("<Configure>", lambda event: tree1.column("#0", width=0))  


        tree1.column("#0", width=0)  
        tree1.column("seller_id", anchor="center", width=100) 
        tree1.column("fullname", anchor="center", width=200)
        tree1.column("contact", anchor="center", width=120)
        tree1.column("address", anchor="center", width=150)
        tree1.column("email", anchor="center", width=200)
        tree1.column("password", anchor="center", width=200)




        tree1.heading("#0", text="", anchor="center")  
        tree1.heading("seller_id", text="Seller ID", anchor="center")
        tree1.heading("fullname", text="Fullname", anchor="center")
        tree1.heading("contact", text="Contact", anchor="center")
        tree1.heading("address", text="Address", anchor="center")
        tree1.heading("email", text="Email", anchor="center")
        tree1.heading("password", text="Password", anchor="center")




        querys = "SELECT * FROM sellers_tbl"
        my_db.execute(querys)
        datas = my_db.fetchall()



        for row in datas:
            tree1.insert("", "end", text="", values=row)



        tree1.place(relx=0.29,rely=0.4)
        #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>


        #Refresh Table>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        def update_tables():
        
            query = "SELECT * FROM sellers_tbl"
            my_db.execute(query)
            data = my_db.fetchall()

        
            for item in tree1.get_children():
                tree1.delete(item)

            #
            for row in data:
                tree1.insert("", "end", values=row)
        update_tables()

        #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>



        #Get the selected row>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        seller_ids = None
        def on_row_select(event):
            selected_items = tree1.selection()
            if selected_items:
                selected_item = selected_items[0]  
                id = tree1.item(selected_item, "values") 
            
                if id is not None:
                    clear_btn()
                    global seller_ids
                    seller_ids = id[0]
                    full_name.insert(0, id[1] if len(id) > 1 else "")
                    contact.insert(0, id[2] if len(id) > 2 else "")
                    address.insert(0, id[3] if len(id) > 3 else "")
                    email.insert(0, id[4] if len(id) > 4 else "")
                    password1.insert(0, id[5] if len(id) > 5 else "")
                    
                else:
                    messagebox.showerror("Error", "Selected row has no data")

        tree1.bind("<<TreeviewSelect>>", on_row_select)
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
       


def main():
 
    app= DashboardApp()
    app.mainloop()
    

if __name__ == "__main__":
    main()
