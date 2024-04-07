                   
from customtkinter import CTk, CTkFrame, CTkButton, CTkImage, CTkLabel, CTkTabview
import tkinter as tk
from PIL import Image, ImageTk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import subprocess
import mysql.connector
from tkinter import messagebox,ttk
from customtkinter import*
import tkinter
import customtkinter
from PIL import Image
from CTkTable import *
import mysql.connector
from tkinter import messagebox,ttk
from tkinter import filedialog




my_connection= mysql.connector.connect(


    host="localhost",
    user="root",
    password="",
    database="hardware_db"
  
)
my_db= my_connection.cursor()



class Category_Windows(tk.Toplevel):
    def __init__(self, DashboardApp):
        super().__init__(DashboardApp)
        self.DashboardAp = DashboardApp
        self.title("Manage product")
        self.geometry("500x400")
        self.minsize(500,400)
        self.set_up_seller()
        self.center_window()
    def back_to_login(self):
        self.destroy()
        self.DashboardAp.deiconify()
    def center_window(self):
        # Get the width and height of the window
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        window_width = 500  # Width of the window
        window_height = 400  # Height of the window

        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2

        # Set the window position
        self.geometry("+{}+{}".format(x, y))
   
        self.starty = None
   
    def set_up_seller(self):
        frame= CTkFrame(master=self,
                    
                fg_color="#FFFFFF", 
                border_color="#FFCC70",
                width=1100,
                height=600,
                
                        )
        label_for_name= CTkLabel(
                        master=frame,
                        font=("Tahoma",10,"bold"),
                        text_color="#1B770C",
                        text="CategoryName:"

                        )
        label_for_name.place(relx=0.1,rely=0.15)

        #Validations for entriess>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

        def on_validate(char, entry_value):
        
            return not char.isdigit() and len(entry_value) < 50 or char == ""


        def on_limit(char, entry_value):
            return len(entry_value) < 60 and char.isalnum() or char == ""


        #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

        full_name= CTkEntry(
                        master=frame,
                        border_color="#1B770C",
                        border_width=1,
                        width=200,
                        validate="key", 
                        validatecommand=(frame.register(on_validate), "%S", "%P"),
                        font=("Tahoma", 10)
                        )
        full_name.place(relx=0.1, rely=0.25)



        #Validations for entriess>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        def on_validate(char, entry_value):
            return char.isdigit() and len(entry_value) < 11 or char == ""
        #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>


    


        #It will clear the buttons everytime i call the function>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        def clear_btn():
            full_name.delete(0,'end')
           

        #INSERT FUNCTION TO DATABASE>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

        def create_record():
            name = full_name.get()
            
           

            if not all([name]):
                messagebox.showerror("Error", "All fields are required!")
                return

            query ="INSERT INTO category (CategoryName) VALUES (%s)"
            values = (name,)

            try:
                my_db.execute(query, values)
                my_connection.commit()
                messagebox.showinfo("Success", "Record created successfully!")
               
                clear_btn()
                
                

            except mysql.connector.Error as err:
                messagebox.showerror("Error", "Category Name is already exist")
                
        add= CTkButton(
                        master=frame,
                        text="Add",
                       
                        width=200,
                        font=("Tahoma",10,"bold"),
                        cursor="hand2",
                        command=create_record
                        )
        add.place(relx=0.1, rely=0.40)

        def refresh():
            query = "SELECT * FROM category"
            my_db.execute(query)
            data = my_db.fetchall()

            table_data.clear()  
            table_data.extend([custom_headers] + data)
            table.update_values(table_data)

       
        back= CTkButton(
                        master=frame,
                        text="Back",
                        width=100,
                       
                        font=("Tahoma",10,"bold"),
                        cursor="hand2",
                        command=self.back_to_login
                        )
        back.place(relx=0.73, rely=0.1)

        def delete_record():
            try:
            
                if cat_id_index is not None:
                
                    confirmation = messagebox.askyesno("Confirmation", "Are you sure you want to delete this record?")

                    if confirmation:
                    
                        query = "DELETE FROM category WHERE CategoryID= %s"
                        values = (cat_id_index,)
                        my_db.execute(query, values)
                        my_connection.commit()
                        messagebox.showinfo("Success", "Record deleted successfully!")
                        
                        clear_btn()
                        
                else:
                    messagebox.showerror("Error", "Failed to delete the record")

            except mysql.connector.Error as err:
                messagebox.showerror("Error", f"Failed to update the record: {err}")

        delete= CTkButton(
                        master=frame,
                        text="Delete",
                        width=200,
                        font=("Tahoma",10,"bold"),
                        cursor="hand2",
                        command=delete_record
                        )
        delete.place(relx=0.54, rely=0.40)
        

        




        global highlighted_row
        highlighted_row = None
      
        def users(cell):
            global highlighted_row,cat_id_index
           

            if cell["row"] == 0 or cell["row"] >= len(table_data):
                return

            if highlighted_row is not None:
                table.edit_row(highlighted_row, fg_color=table.fg_color if highlighted_row % 2 == 0 else table.fg_color2)

            if cell["row"] != highlighted_row:
                table.edit_row(cell["row"], fg_color=table.hover_color)
                highlighted_row = cell["row"]
                
                cat_id_index = custom_headers.index("CategoryID")
                product_name_index = custom_headers.index("CategoryName")

                if cell["row"] < len(table_data):
                    cat_id_index = table_data[cell["row"]][cat_id_index]

                    product_name = table_data[cell["row"]][product_name_index]
                    full_name.insert(0,product_name)
                else:
                    highlighted_row = None
            else:
                highlighted_row = None

       

        global custom_headers
        custom_headers = ["CategoryID", "CategoryName"]

       
        query = "SELECT * FROM category"
        my_db.execute(query)
        data =  my_db.fetchall()

        table_data= [custom_headers]+ data
        table_frame = CTkScrollableFrame(master=frame, width=400,height=30,fg_color="#FFFFFF",
                                         border_color="#125B50",border_width=1)
        table_frame.place(relx=0.1, rely=0.5)
        
        table = CTkTable(master=table_frame,row=0, column=2,
                         colors=["#F8F8F8", "#EAEAEA"],
                         values= table_data,
                         header_color=("#E5C287"),
                         font=("Tahoma",10,"bold"),
                         width=40,
                         height=20,
                         padx=0.5,
                         
                         command=users
                         )                       
        # table.place(relx=0.01,rely=0.1)
        table.pack(expand=True, fill="both")
        frame.pack(expand=True,fill="both")

        
        









class Addseller_Windows(tk.Toplevel):
    def __init__(self, DashboardApp):
        super().__init__(DashboardApp)
        self.DashboardAp = DashboardApp
        self.title("Manage product")
        self.geometry("1100x600")
        self.minsize(1100,600)
        self.set_up_seller()
    def back_to_login(self):
        self.destroy()
        self.DashboardAp.deiconify()


    def set_up_seller(self):

        frame= CTkFrame(master=self,
                    
                fg_color="#FFFFFF", 
                border_color="#FFCC70",
                width=1100,
                height=600,
                
                        )
        frame.pack(expand=True, fill="both")
        

        reports= CTkFrame(master=frame,
                            height=155,
                            width=720,
                            border_width=0,
                            fg_color="#FFFFFF"
                            )
        reports.pack(expand=True,pady=30)

        label_title =CTkLabel(master=frame, text="Add Product", fg_color="transparent", font=("Tahoma",14,"bold"))
        label_title.place(relx=0.45, rely=0.0)

        label_for_name= CTkLabel(
                        master=reports,
                        font=("Tahoma",10,"bold"),
                       
                        text="Full name:"

                        )
        label_for_name.place(relx=0.05,rely=0.04)

        #Validations for entriess>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

        def on_validate(char, entry_value):
        
            return not char.isdigit() and len(entry_value) < 50 or char == ""


        def on_limit(char, entry_value):
            return len(entry_value) < 60 and char.isalnum() or char == ""


        #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

        full_name= CTkEntry(
                        master=reports,
                        border_color="#1B770C",
                        border_width=1,
                        width=200,
                        validate="key", 
                        validatecommand=(reports.register(on_validate), "%S", "%P"),
                        font=("Tahoma", 10)
                        )
        full_name.place(relx=0.05, rely=0.18)


        label_for_contact= CTkLabel(
                        master=reports,
                        font=("Tahoma",10,"bold"),
                       
                        text="Contact:"

                        )
        label_for_contact.place(relx=0.05,rely=0.45)


        #Validations for entriess>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        def on_validate(char, entry_value):
            return char.isdigit() and len(entry_value) < 11 or char == ""
        #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>


        contact= CTkEntry(
                        master=reports,
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
            password.delete(0,'end')

        #INSERT FUNCTION TO DATABASE>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        def validate_email(email):
            if email.endswith("@gmail.com"):
                    return True
            else:
                return False

            
            

        def create_record():
            name = full_name.get()
            contacts = contact.get()
            addresss = address.get()
            emails = email.get()
            if not validate_email(emails):
                messagebox.showerror("Error", "Email must end with @gmail.com")
                return  
            passwords = password.get()

            if len(contacts) <11:

                messagebox.showerror("Error", "Contact should be 11 digits")
                return
            

            if not all([name, contacts, addresss, emails,passwords]):
                messagebox.showerror("Error", "All fields are required!")
                return
            
            query = "INSERT INTO sellers_tbl (fullname, contact, address, email, password) VALUES ( %s, %s, %s, %s, %s)"
            values = (name, contacts, addresss, emails, passwords)

            try:
                my_db.execute(query, values)
                my_connection.commit()
                messagebox.showinfo("Success", "Record created successfully!")
                update_table()
                clear_btn()
                

            except mysql.connector.Error as err:
                messagebox.showerror("Error", "Failed to create record:Email is already exist")

        add= CTkButton(
                        master=frame,
                        text="Add",
                        width=94,
                        font=("Tahoma",10,"bold"),
                        cursor="hand2",
                        command=create_record
                        )
        add.place(relx=0.05, rely=0.35)

        #Update the selected row>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

        def update_data():
            name = full_name.get().strip()
            contacts = contact.get().strip()
            addresss = address.get().strip()
            emails = email.get().strip()
            passwords = password.get().strip()
        
        
        
            try:
                if seller_id is not None:
                    query = """
                    UPDATE sellers_tbl
                    SET fullname = %s, contact = %s, address = %s, email = %s, password = %s
                    WHERE seller_id = %s
                    """
                    values = (name, contacts, addresss, emails, passwords,seller_id)

                    my_db.execute(query, values)
                    my_connection.commit()
                    messagebox.showinfo("Success", "Record updated successfully!")
                    update_table()
                    clear_btn()
                else:
                    messagebox.showerror("Error", "Please select a row to update")

            except IndexError:
                messagebox.showerror("Error", "IndexError: Tuple index out of range")
            except mysql.connector.Error as err:
                messagebox.showerror("Error", f"Failed to update the record: {err}")


        update= CTkButton(
                        master=frame,
                        text="Update",
                        width=94,
                        font=("Tahoma",10,"bold"),
                        cursor="hand2",
                        command=update_data
                        )
        update.place(relx=0.2, rely=0.35)



        label_for_address= CTkLabel(
                        master=reports,
                        font=("Tahoma",10,"bold"),
                        text="Address:"

                        )
        label_for_address.place(relx=0.37,rely=0.04)
        address= CTkEntry(
                        master=reports,
                        border_color="#1B770C",
                        border_width=1,
                        width=200,
                        font=("Tahoma", 10),
                        validate="key", 
                        validatecommand=(reports.register(on_limit), "%S", "%P"),
                        )
        address.place(relx=0.37, rely=0.18)


        label_for_email= CTkLabel(
                        master=reports,
                        font=("Tahoma",10,"bold"),
                        text="Email:"

                        )
        label_for_email.place(relx=0.37,rely=0.45)

        def validate_email(email):
            if email.endswith("@gmail.com"):
                return True
            else:
                return False

        def on_validate_email(new_value, current_value):
            # Return True if the email is valid, otherwise False
            return validate_email(new_value)

        email= CTkEntry(
                        master=reports,
                        border_color="#1B770C",
                        border_width=1,
                        width=200,
                        font=("Tahoma", 10),
                        validate="key",
                        validatecommand=(frame.register(on_validate_email), "%S", "%P"),
                        )
        email.place(relx=0.37, rely=0.6)
        clear= CTkButton(
                        master=frame,
                        text="Clear",
                        width=94,
                        font=("Tahoma",10,"bold"),
                        cursor="hand2",
                        command=clear_btn
                        )
        clear.place(relx=0.355, rely=0.35)


        #IT will delete the specific record>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>


        def delete_record():
            try:
            
                if seller_id is not None:
                
                    confirmation = messagebox.askyesno("Confirmation", "Are you sure you want to delete this record?")

                    if confirmation:
                    
                        query = "DELETE FROM sellers_tbl WHERE seller_id = %s"
                        values = (seller_id,)
                        my_db.execute(query, values)
                        my_connection.commit()
                        messagebox.showinfo("Success", "Record deleted successfully!")
                        update_table()
                        clear_btn()
                
                else:
                    messagebox.showerror("Error", "Failed to delete the record")

            except mysql.connector.Error as err:
                messagebox.showerror("Error", f"Failed to update the record: {err}")

        #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>..

        delete= CTkButton(
                        master=frame,
                        text="Delete",
                        width=94,                        
                        font=("Tahoma",10,"bold"),
                        cursor="hand2",
                        command=delete_record
                        )
        delete.place(relx=0.52, rely=0.35)


        search= CTkEntry(
                        master=frame,
                        border_color="#1B770C",
                        border_width=1,
                        width=150,
                        placeholder_text="Search here....",
                        font=("Tahoma", 10)
                )

        search.place(relx=0.68, rely=0.35)


        def search_sellers():
            search_term = search.get().strip()
            
            if search_term:
                query = "SELECT * FROM sellers_tbl WHERE fullname LIKE %s OR email LIKE %s"
                values = ("%" + search_term + "%", "%" + search_term + "%")
            else:
                query = "SELECT * FROM sellers_tbl"
                values = ()

            my_db.execute(query, values)
            data = my_db.fetchall()
            
            
            for item in tree.get_children():
                tree.delete(item)

            for row in data:
                tree.insert("", "end", values=row)
        search_btn= CTkButton(
                        master=frame,
                        text="Search",
                        width=60,
                        font=("Tahoma",10,"bold"),
                        cursor="hand2",
                        command=search_sellers
                        
            
                        )
        search_btn.place(relx=0.82, rely=0.35)
        password_label= CTkLabel(
                        master=reports,
                        font=("Tahoma",10,"bold"),
                        text="Password:"

                        )
        password_label.place(relx=0.68,rely=0.04)

        password= CTkEntry(
                        master=reports,
                        border_color="#1B770C",
                        border_width=1,
                        show="*",
                        width=200,
                        font=("Tahoma", 10)
                        )
        password.place(relx=0.68, rely=0.18)

        def checkbox_event():
            
            
            if check_var.get() == "on":
                password.configure(show="")
            else:
                password.configure(show="*")
          


        check_var = customtkinter.StringVar(value="off")
        checkbox = customtkinter.CTkCheckBox(master=reports, text="show password", command=checkbox_event,
                                            variable=check_var, onvalue="on", offvalue="off",checkbox_height=15, checkbox_width=15)

        checkbox.place(x=561, y=65)

        refresh=CTkButton(master=frame,
                        
                        text="Refresh",
                        width=60,
                        font=("Tahoma",10,"bold"),
                        cursor="hand2",
                        command=search_sellers
                        )

        refresh.place(relx=0.88,rely=0.35)

        back=CTkButton(master=frame,
                        
                        text="Back",
                        width=60,
                        hover_color="#87A922",
                        font=("Tahoma",10,"bold"),
                        cursor="hand2",
                        command=self.back_to_login
                        )

        back.place(relx=0.88,rely=0.1)
        #Table creation>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        style = ttk.Style()
        font_size = 14
        header_color = "lightblue"
        style.configure("Treeview.Heading", font=("Tahoma", font_size),background=header_color)
        style.configure("Treeview", font=("Tahoma", 12))
        tree = ttk.Treeview(frame, style="Treeview")

        tree["columns"] = ("seller_id","fullname", "contact", "address", "email", "password")
        tree.bind("<Configure>", lambda event: tree.column("#0", width=0))  


        tree.column("#0", width=0)  
        tree.column("seller_id", anchor="center", width=100) 
        tree.column("fullname", anchor="center", width=200)
        tree.column("contact", anchor="center", width=120)
        tree.column("address", anchor="center", width=150)
        tree.column("email", anchor="center", width=200)
        tree.column("password", anchor="center", width=200)




        tree.heading("#0", text="", anchor="center")  
        tree.heading("seller_id", text="Seller ID", anchor="center")
        tree.heading("fullname", text="Fullname", anchor="center")
        tree.heading("contact", text="Contact", anchor="center")
        tree.heading("address", text="Address", anchor="center")
        tree.heading("email", text="Email", anchor="center")
        tree.heading("password", text="Password", anchor="center")




        query = "SELECT * FROM sellers_tbl"
        my_db.execute(query)
        data = my_db.fetchall()



        for row in data:
            tree.insert("", "end", text="", values=row)



        tree.pack(expand=True, pady=30)
        #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>


        #Refresh Table>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        def update_table():
        
            query = "SELECT * FROM sellers_tbl"
            my_db.execute(query)
            data = my_db.fetchall()

        
            for item in tree.get_children():
                tree.delete(item)

            #
            for row in data:
                tree.insert("", "end", values=row)
        update_table()

        #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>



        #Get the selected row>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        global seller_id
        seller_id = None
        def on_row_select(event):
            selected_items = tree.selection()
            if selected_items:
                selected_item = selected_items[0]  
                id = tree.item(selected_item, "values") 
            
                if id is not None:
                    clear_btn()
                    global seller_id
                    seller_id = id[0]
                    full_name.insert(0, id[1] if len(id) > 1 else "")
                    contact.insert(0, id[2] if len(id) > 2 else "")
                    address.insert(0, id[3] if len(id) > 3 else "")
                    email.insert(0, id[4] if len(id) > 4 else "")
                    password.insert(0, id[5] if len(id) > 5 else "")
                    
                else:
                    messagebox.showerror("Error", "Selected row has no data")

        tree.bind("<<TreeviewSelect>>", on_row_select)




class Product_Windows(tk.Toplevel):
    def __init__(self, DashboardApp):
        super().__init__(DashboardApp)
        self.DashboardAp = DashboardApp
        self.title("Manage product")
        self.geometry("1100x600")
        self.minsize(1100,600)
        self.set_up_product()
        self.center_window()


    def back_to_login(self):
        self.destroy()
        self.DashboardAp.deiconify()  

    def center_window(self):
        # Get the width and height of the window
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        window_width = 1100  # Width of the window
        window_height = 600  # Height of the window

        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2

        # Set the window position
        self.geometry("+{}+{}".format(x, y))
   
        self.starty = None
   
    def set_up_product(self):
            frame= CTkFrame(master=self,                        
                fg_color="#FFFFFF", 
                width=1100,
                height=600,
                
                )
            frame.pack(expand=True, fill="both")
           
            my_image = customtkinter.CTkImage(light_image=Image.open("D:\\POS\\Images\\coffee.png"),
                                  size=(100, 100))

            image_label = customtkinter.CTkLabel(master=frame, image=my_image, text="")
            image_label.place(relx=0.1,rely=0.1)
          
            reports= CTkFrame(master=frame,
                                height=250,
                                width=1000,
                                fg_color="#FFFFFF",
                                border_color="#1B770C",
                                border_width=1
                                )
            # reports.place(relx=0.05,rely=0.048)
            reports.pack(expand=True,pady=30)

            label_for_pname= CTkLabel(
                            master=reports,
                            font=("Tahoma",12,"bold"),
                            text_color="#1B770C",
                            text="Product name:"

                            )
            label_for_pname.place(relx=0.05,rely=0.04)

            label_title =CTkLabel(master=frame, text="Add Product", fg_color="transparent", font=("Tahoma",14,"bold"))
            label_title.place(relx=0.45, rely=0.0)

            #Validations for entriess>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

            def on_validate(char, entry_value):
            
                return not char.isdigit() and len(entry_value) < 50 or char == ""
        

            def on_limit(char, entry_value):
                    # Allow digits (0-9), a single dot, and empty string
                    if char == "":
                        return True  # Allow empty string for deletion
                    elif char.isdigit():
                        return True  # Allow digits
                    elif char == '.' and '.' not in entry_value:
                        return True  # Allow a single dot if not already present
                    else:
                        return False  # Disallow other characters



            #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

            product_name= CTkEntry(
                            master=reports,
                            border_color="#1B770C",
                            border_width=1,
                            width=200,
                            validate="key", 
                            validatecommand=(reports.register(on_validate), "%S", "%P"),
                            font=("Tahoma", 12)
                            )
            product_name.place(relx=0.05, rely=0.18)


            description_label= CTkLabel(
                            master=reports,
                            font=("Tahoma",12,"bold"),
                            text_color="#1B770C",
                            text="Description:"

                            )
            description_label.place(relx=0.05,rely=0.45)


            #Validations for entriess>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
            def on_validates(char, entry_value):
                return char.isdigit() and len(entry_value) <=3 or char == ""
            
            def on_validatesssss(char, entry_value):
        
                 return  char.isdigit() and len(entry_value) < 50 or char == ""
            
            def on_validatess(char, entry_value):
                if char.isdigit():
                     return True  # Allow digits

                if char == '.' and '.' not in entry_value and len(entry_value) < 7:
                    # Allow decimal point only once, within a limit of 6 characters
                    return True

                if char == '':  # Allow backspace to delete characters
                    return True

                return False  # Reject any other characters
            #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
            def validate_input(char, entry_value):
                    return len(entry_value) < 50 

                # Create a StringVar to track the entry value
            description_value = StringVar()


            description= CTkEntry(
                            master=reports,
                            border_color="#1B770C",
                            border_width=1,
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

            #INSERT FUNCTION TO DATABASE>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

            def create_record():
                pname = product_name.get()
                pdescription = description.get()
                category = combobox.get()
                pprice = price.get()
                pqty = qty.get()
                
              
                
                try:
                    price_value = float(pprice)
                    if price_value <= 0:
                        messagebox.showerror("Error", "Price must be a positive number.")
                        return
                except ValueError:
                    messagebox.showerror("Error", "Invalid price format. Please enter a number.")
                    return

                
                if not all([pname, pdescription, category, pprice, pqty ]):
                    messagebox.showerror("Error", "All fields are required!")
                    return
                
               

                query = "INSERT INTO products (ProductName, Description, Category, Price, QuantityOnHand, Current_Stock) VALUES ( %s, %s, %s, %s, %s, %s)"
                values = (pname, pdescription, category, pprice, pqty,pqty)

                try:
                    my_db.execute(query, values)
                    my_connection.commit()
                    messagebox.showinfo("Success", "Record created successfully!")
                    update_table()
                    clear_btn()
                    

                except mysql.connector.Error as err:
                    # messagebox.showerror("Error", "Failed to create record:Email is already exist")
                    print(err)

            add= CTkButton(
                            master=reports,
                            text="Add",
                            width=94,
                            hover_color="#87A922",
                            font=("Tahoma",12,"bold"),
                            cursor="hand2",
                            command=create_record
                            )
            add.place(relx=0.05, rely=0.79)

            

            def update_data():
                    pname = product_name.get()
                    pdescription = description.get().strip()
                    cat = combobox.get().strip()
                    pprice = price.get().strip()
                    pqty = qty.get().strip()

                    if not all([pname, pdescription, cat, pprice, pqty ]):
                        messagebox.showerror("Error", "All fields are required!")
                        return

                    try:
                        if seller_id is not None:
                            query_fetch = "SELECT ProductName, Description, Category, Price, QuantityOnHand FROM products WHERE ProductID = %s"
                            my_db.execute(query_fetch, (seller_id,))
                            existing_data = my_db.fetchone()

                            print(existing_data)
                            
                            if (pname, pdescription, cat, pprice, pqty) != existing_data:
                                query = """
                                UPDATE products
                                SET ProductName = %s, Description = %s, Category = %s, Price = %s, QuantityOnHand = %s
                                WHERE ProductID = %s
                                """
                                values = (pname, pdescription, cat,  pprice, pqty, seller_id)

                                my_db.execute(query, values)
                                my_connection.commit()

                                messagebox.showinfo("Success", "Record updated successfully!")
                                update_table()
                                clear_btn()
                            else:
                                messagebox.showinfo("No Changes", "No changes were made to the record.")
                        else:
                            messagebox.showerror("Error", "Please select a row to update")

                    except IndexError:
                        messagebox.showerror("Error", "IndexError: Tuple index out of range")
                    except mysql.connector.Error as err:
                        messagebox.showerror("Error", f"Failed to update the record: {err}")



            update= CTkButton(
                            master=reports,
                            text="Update",
                            width=94,
                            hover_color="#3FBAC2",
                            font=("Tahoma",12,"bold"),
                            cursor="hand2",
                            command=update_data
                            )
            update.place(relx=0.2, rely=0.79)



            label_for_cat= CTkLabel(
                            master=reports,
                            font=("Tahoma",12,"bold"),
                            text_color="#1B770C",
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
                                                state="readonly",
                                                command=combobox_callback
                                                )
            combobox.set("Choose category")
            combobox.place(relx=0.37, rely=0.17 )



            #<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

            label_for_price= CTkLabel(
                            master=reports,
                            font=("Tahoma",12,"bold"),
                            text_color="#1B770C",
                            text="Price:"

                            )
            label_for_price.place(relx=0.37,rely=0.45)

            def validate_price(price):
                if len(price) > 7:
                    return False  
                if not price:
                    return True  # Allow empty input
                try:
                    # Attempt to convert the input to a float
                    float_price = float(price)
                    # Ensure the price is non-negative
                    if float_price >= 0:
                        return True
                    else:
                        return False
                except ValueError:
                    # If the input cannot be converted to a float, it's invalid
                    return False



            price= CTkEntry(
                    master=reports,
                    border_color="#1B770C",
                    border_width=1,
                    width=200,
                    font=("Tahoma", 12),
                    validate="key",  
                    validatecommand=(reports.register(validate_price), "%P"))
            price.place(relx=0.37, rely=0.6)



            def choose_file():
                global file_path
                file_path = filedialog.askopenfilename(
                        filetypes=[("Image files", "*.jpg;*.jpeg;*.png;*.gif")]
                    )

                if file_path:
                    try:
                        with open(file_path, "rb") as f:
                           global image_data
                           image_data = f.read()
                        img = Image.open(file_path)
                        img.thumbnail((image_label.winfo_width(), image_label.winfo_height()))  # Resize based on label size
                        img_tk = CTkImage(img)
                        image_label.configure(image=img_tk)
                        image_label.image = img_tk  
                    except (FileNotFoundError, IOError) as err:
                        print(f"Error opening image: {err}")
                    
                
            

            image_frame= CTkFrame(master=reports,
                                
                            
                                border_color="#D37676",
                                border_width=1,
                                fg_color="#FFFFFF",
                                width=90,
                                height=90
                                
                                )
            image_frame.place(relx=0.74, rely=0.30)

            image_label = CTkLabel(
                master=image_frame,
                height=75,
                width=75,
                
                text="",
            

            
            
            )
            image_label.place(relx=0.02, rely=0.02)

            file= CTkButton(
                            master=reports,
                            text="Choose File",
                            border_color="#D37676",
                            border_width=1,
                            fg_color="#D37676",
                            width=94,
                            hover_color="#EBC49F",
                            font=("Tahoma",12,"bold"),
                            cursor="hand2",
                            command=choose_file
                            )
            file.place(relx=0.74, rely=0.678)


            clear= CTkButton(
                            master=reports,
                            text="Clear",
                            width=94,
                            hover_color="#EBC49F",
                            font=("Tahoma",12,"bold"),
                            cursor="hand2",
                            command=clear_btn
                            )
            clear.place(relx=0.37, rely=0.79)


            #IT will delete the specific record>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>


            def delete_record():
                try:
                
                    if seller_id is not None:
                    
                        confirmation = messagebox.askyesno("Confirmation", "Are you sure you want to delete this record?")

                        if confirmation:
                        
                            query = "DELETE FROM products WHERE ProductID = %s"
                            values = (seller_id,)
                            my_db.execute(query, values)
                            my_connection.commit()
                            messagebox.showinfo("Success", "Record deleted successfully!")
                            update_table()
                            clear_btn()
                    
                    else:
                        messagebox.showerror("Error", "Failed to delete the record")

                except mysql.connector.Error as err:
                    messagebox.showerror("Error", f"Failed to update the record: {err}")



            delete= CTkButton(
                            master=reports,
                            text="Delete",
                            width=94,
                            hover_color="#EBC49F",
                            font=("Tahoma",12,"bold"),
                            cursor="hand2",
                            command=delete_record
                            )
            delete.place(relx=0.52, rely=0.79)


            search= CTkEntry(
                            master=frame,
                            border_color="#1B770C",
                            border_width=1,
                            width=150,
                            placeholder_text="Search here....",
                            font=("Tahoma", 12)
                    )

            search.place(relx=0.68, rely=0.5)

            back= CTkButton(master=frame,
                            
                            
                            width=100,
                            
                            text="BACK TO DASHBOARD",
                            command=self.back_to_login
                            )
            back.place(relx=0.5, rely=0.5)


            def search_sellers():
                search_term = search.get().strip()
                if search_term:
                    query = "SELECT * FROM products WHERE ProductName LIKE %s OR Price LIKE %s OR Category LIKE %s"
                    values = ("%" + search_term + "%", "%" + search_term + "%", "%" + search_term + "%")
                else:
                    query = "SELECT * FROM products"
                    values = ()

                my_db.execute(query, values)
                data = my_db.fetchall()

                for item in tree.get_children():
                    tree.delete(item)

                for row in data:
                    tree.insert("", "end", values=row)

            search_btn= CTkButton(
                            master=frame,
                            text="Search",
                            border_color="#1B770C",
                            border_width=1,
                            width=100,
                            hover_color="#87A922",
                            font=("Tahoma",12,"bold"),
                            cursor="hand2",
                            command=search_sellers
                            
                
                            )
            search_btn.place(relx=0.82, rely=0.5)
            qty_label= CTkLabel(
                            master=reports,
                            font=("Tahoma",12,"bold"),
                            text_color="#1B770C",
                            text="Quantity:"

                            )
            qty_label.place(relx=0.68,rely=0.04)
            qty= CTkEntry(
                            master=reports,
                            border_color="#1B770C",
                            border_width=1,
                            width=200,
                            font=("Tahoma", 12),
                            validate="key", 
                            validatecommand=(reports.register(on_validates), "%S", "%P"),
                            )
            qty.place(relx=0.68, rely=0.18)

            style = ttk.Style()
            font_size = 12
            header_color = "lightblue"
            style.configure("Treeview.Heading", font=("Tahoma", font_size),background=header_color)
            style.configure("Treeview", font=("Tahoma", 10))
            tree = ttk.Treeview(frame, style="Treeview")

            tree["columns"] = ("ProductID","ProductName", "Description", "Category", "Price", "QuantityOnHand","Current_Stock")
            tree.bind("<Configure>", lambda event: tree.column("#0", width=0))  


            tree.column("#0", width=0)  
            tree.column("ProductID", anchor="center", width=100) 
            tree.column("ProductName", anchor="center", width=200)
            tree.column("Description", anchor="center", width=220)
            tree.column("Category", anchor="center", width=150)
            tree.column("Price", anchor="center", width=200)
            tree.column("QuantityOnHand", anchor="center", width=120)
            tree.column("Current_Stock", anchor="center", width=120)

 


            tree.heading("#0", text="", anchor="center")  
            tree.heading("ProductID", text="ProductID", anchor="center")
            tree.heading("ProductName", text="ProductName", anchor="center")
            tree.heading("Description", text="Description", anchor="center")
            tree.heading("Category", text="Category", anchor="center")
            tree.heading("Price", text="Price", anchor="center")
            tree.heading("QuantityOnHand", text="Quantity", anchor="center")
            tree.heading("Current_Stock", text="Quantity", anchor="center")

                


            query = "SELECT * FROM products"
            my_db.execute(query)
            data = my_db.fetchall()



            for row in data:
                tree.insert("", "end", text="", values=row)



            # tree.place(relx=0.01,rely=0.55)
            tree.pack(expand=True, pady=30)
            #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>


            #Refresh Table>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
            def update_table():
            
                query = "SELECT * FROM products"
                my_db.execute(query)
                data = my_db.fetchall()

            
                for item in tree.get_children():
                    tree.delete(item)

                #
                for row in data:
                    tree.insert("", "end", values=row)
            update_table()
            global seller_id
            seller_id = None
            def on_row_select(event):
                selected_items = tree.selection()
                
                if selected_items:
                    selected_item = selected_items[0]  
                    id = tree.item(selected_item, "values") 
                
                    if id is not None:
                        clear_btn()
                        global seller_id
                        seller_id = id[0]
                        product_name.insert(0, id[1] if len(id) > 1 else "")
                        description.insert(0, id[2] if len(id) > 2 else "")
                        combobox.set(id[3] if len(id) > 3 else "")
                        price.insert(0, id[4] if len(id) > 4 else "")
                        qty.insert(0, id[5] if len(id) > 5 else "")
                        
                    else:
                        messagebox.showerror("Error", "Selected row has no data")

            tree.bind("<<TreeviewSelect>>", on_row_select)

#<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<DASHBOARD>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
class DashboardApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.setup_dashboard()
        self.geometry("1034x600")
        self.minsize(1034, 600)
        self.center_window()
        self.seller_report() 
        self.categories_report()
        self.products_report()
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
    def open_add_product(self):
        self.withdraw()
        Product_Windows(self)
    def open_add_product(self):
        self.withdraw()
        Product_Windows(self)

    def open_add_categories(self):
        self.withdraw()
        Category_Windows(self)
    def open_add_seller(self):
        self.withdraw()
        Addseller_Windows(self)
  
    def setup_dashboard(self):
        

        frame = CTkFrame(
            master=self.master,
            fg_color="#FFFFFF",
            border_color="#1B770C",
            
            width=1000,
            height=600,
            
           
        )
        frame.pack(expand=True, fill="both")

        # SIDE BAR
        sidebar = CTkFrame(
            master=frame,
            height=545,
            width=200,
            border_width=1,
            border_color="#FFFFFF",
            fg_color="#FFFFFF"
        )
        sidebar.place(relx=0.02, rely=0.03)

        button_width = 125
        
        product_btn = CTkButton(
            master=sidebar,
            text="Manage product",
            height=25,
            width=button_width,
            border_width=1,
            hover_color="#C850C0",
            border_color="#FFFFFF",
            corner_radius=10,
            font=("Tahoma", 10, "bold"),
            cursor="hand2",
            command=self.open_add_product
            
        )
        product_btn.place(relx=0.2, rely=0.2)

        # img_2 = Image.open("/DS102PROJECT/Icon/increase.png")
        categories_btn = CTkButton(
            master=sidebar,
            text="Manage category",
            height=25,
            width=button_width,
            border_width=1,
            hover_color="#C850C0",
            border_color="#FFFFFF",
            corner_radius=10,
            font=("Tahoma", 10, "bold"),
            cursor="hand2",
            command=self.open_add_categories
        )
        categories_btn.place(relx=0.2, rely=0.26)

        seller_btn= CTkButton(master=sidebar,
                text="Manage seller",
                height=25,
                width=button_width,
               
                border_width=1,
                border_color="#FFFFFF",
                corner_radius=10,
                font=("Tahoma", 10,"bold"),
                cursor="hand2",
                command=self.open_add_seller
                            )
        seller_btn.place(relx=0.2, rely=0.32)
    

    #DAILY REPORTS

        reports= CTkFrame(master=frame,
                        height=150,
                        width=720,
                        fg_color="#FFFFFF"
                        )
        reports.place(relx=0.25,rely=0.03)

        panel_1= CTkFrame(
                        master=reports,
                        height=135,
                        width=200,
                        fg_color="#DFF5FF",
                        border_color="#DFF5FF",

                        )
    


        panel_2= CTkFrame(
                        master=reports,
                        height=135,
                        width=200,
                        fg_color="#DFF5FF",
                        border_color="#DFF5FF",
                        )
    


        panel_3= CTkFrame(
                        master=reports,
                        height=135,
                        width=200,
                        fg_color="#DFF5FF",
                        border_color="#9391E6"
                        )


        panel_width = 200  
        gap_width = 20  


        total_width = (3 * panel_width) + (2 * gap_width)

        
        start_x = (720 - total_width) / 2


        panel_1.place(relx=start_x / 720, rely=0.04)
        panel_2.place(relx=(start_x + panel_width + gap_width) / 720, rely=0.04)
        panel_3.place(relx=(start_x + 2 * (panel_width + gap_width)) / 720, rely=0.04)



        label_product= CTkLabel(master=panel_1,
                                text="Products",
                                font=("Tahoma",14, "bold"),
                                text_color="#0C0C0C"
                                )
        label_product.place(relx=0.32,rely=0.1)
        global product_count
        product_count= CTkLabel(master=panel_1,
                                text="0",
                                font=("Tahoma",18, "bold"),
                                text_color="#0C0C0C"
                                )
        product_count.place(relx=0.45,rely=0.4)

        label_category= CTkLabel(master=panel_2,
                                text="Categories",
                                font=("Tahoma",14, "bold"),
                                text_color="#0C0C0C"
                                )
        label_category.place(relx=0.32,rely=0.1)
        global category_count
        category_count= CTkLabel(master=panel_2,
                                text="0",
                                font=("Tahoma",18, "bold"),
                                text_color="#0C0C0C"
                                )
        category_count.place(relx=0.45,rely=0.4)
      
        label_seller= CTkLabel(master=panel_3,
                                text="Sellers",
                                font=("Tahoma",14, "bold"),
                                text_color="#0C0C0C"
                                )
        
        label_seller.place(relx=0.32,rely=0.1)

        global seller_count
        seller_count= CTkLabel(master=panel_3,
                                text="0",
                                font=("Tahoma",18, "bold"),
                                text_color="#0C0C0C"
                                )
        seller_count.place(relx=0.45,rely=0.4)
    

    def seller_report(self):  
        global seller_count
        query = "SELECT COUNT(*) FROM sellers_tbl"

        try:
            my_db.execute(query)
            count_result = my_db.fetchone()
            if count_result is not None:
                count = count_result[0] 
                seller_count.configure(text=f"{count}")
              
            else:
                seller_count.configure(text="Sellers: N/A") 

        except mysql.connector.errors.Error as err:
            messagebox.showerror("Error", f"Failed to load count: {err}")
    def categories_report(self):  
        global category_count
        query = "SELECT COUNT(*) FROM category"

        try:
            my_db.execute(query)
            count_result = my_db.fetchone()
            if count_result is not None:
                count = count_result[0] 
                category_count.configure(text=f"{count}")
              
            else:
                category_count.configure(text="Sellers: N/A") 

        except mysql.connector.errors.Error as err:
            messagebox.showerror("Error", f"Failed to load count: {err}")


    def products_report(self):  
        global product_count
        query = "SELECT COUNT(*) FROM products"

        try:
            my_db.execute(query)
            count_result = my_db.fetchone()
            if count_result is not None:
                count = count_result[0] 
                product_count.configure(text=f"{count}")
              
            else:
               product_count.configure(text="Sellers: N/A") 

        except mysql.connector.errors.Error as err:
            messagebox.showerror("Error", f"Failed to load count: {err}")
        
    def chart(self):
        months = ['January', 'February', 'March', 'April', 'May']
        sales = [10000, 12000, 9000, 15000, 18000]

        fig = Figure(figsize=(5, 4), dpi=100)
        plot = fig.add_subplot(1, 1, 1)
        plot.plot(months, sales, marker='o', linestyle='-', color='b', label='Sales')
        plot.set_xlabel('Month')
        plot.set_ylabel('Sales Amount ($)')
        plot.set_title('Monthly Sales Performance')
        plot.legend()

        chart_window = tk.Toplevel(self.master)
        chart_window.title("Sales Chart")

        canvas = FigureCanvasTkAgg(fig, master=chart_window)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack()
  

       


def main():
 
    app= DashboardApp()
    app.mainloop()
    


if __name__ == "__main__":
    main()
