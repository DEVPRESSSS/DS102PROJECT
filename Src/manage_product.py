from customtkinter import*
import tkinter
import customtkinter
from PIL import Image
from CTkTable import *
import mysql.connector
from tkinter import messagebox,ttk
from dash_board import DashboardApp
from tkinter import filedialog

def run_dashboard():
    global app
    app.withdraw() 
    root = CTk()
    root.title("Dashboard")  
    app = DashboardApp(root)
    root.mainloop()
my_connection= mysql.connector.connect(


    host="localhost",
    user="root",
    password="",
    database="hardware_db"
  
)
my_db= my_connection.cursor()

app= CTk()
    
customtkinter.set_appearance_mode("light")
app.geometry("1034x600")
app.minsize(1034,600)

frame= CTkFrame(master=app,
                    
                fg_color="#FFFFFF", 
                border_color="#FFCC70",
                width=1000,
                height=580,
                corner_radius=20,
                border_width=0
                )
frame.place(relx=0.5, rely=0.5,anchor=tkinter.CENTER)

label_1= CTkLabel(master=frame,
                  text="Add product here",
                  font=("Tahoma",18,"bold"),
                  text_color="#1B770C"
                  )
label_1.place(relx=0.52,rely=0.01)
sidebar= CTkFrame(master=frame,
                    height=545,
                    width=200,
                    border_width=1,
                    border_color="#1B770C",                  
                    fg_color="#1B770C"
                    )
sidebar.place(relx=0.02,rely=0.03)

dashboard_button= CTkButton(
                       master=sidebar,
                       width=150,
                       text="Dashboard",
                       fg_color="transparent",
                       font=("Tahoma",14,"bold"),
                       hover_color="#C850C0",
                       cursor="hand2",
                       border_color="#FFFFFF",
                       border_width=0.5,
                       command=run_dashboard

                       )

dashboard_button.place(relx=0.1, rely=0.19)
reports= CTkFrame(master=frame,
                    height=160,
                    width=720,
                    fg_color="#FFFFFF"
                    )
reports.place(relx=0.25,rely=0.048)
label_for_pname= CTkLabel(
                 master=reports,
                 font=("Tahoma",10,"bold"),
                 text_color="#1B770C",
                 text="Product name:"

                )
label_for_pname.place(relx=0.05,rely=0.04)

#Validations for entriess>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

def on_validate(char, entry_value):
   
    return not char.isdigit() and len(entry_value) < 50 or char == ""

#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

product_name= CTkEntry(
                   master=reports,
                   border_color="#1B770C",
                   border_width=1,
                   width=200,
                   validate="key", 
                   validatecommand=(reports.register(on_validate), "%S", "%P"),
                   font=("Tahoma", 10)
                  )
product_name.place(relx=0.05, rely=0.18)


description_label= CTkLabel(
                 master=reports,
                 font=("Tahoma",10,"bold"),
                 text_color="#1B770C",
                 text="Description:"

                )
description_label.place(relx=0.05,rely=0.45)


#Validations for entriess>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
def on_validate(char, entry_value):
    return char.isdigit() and len(entry_value) < 11 or char == ""
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>


description= CTkEntry(
                   master=reports,
                   border_color="#1B770C",
                   border_width=1,
                   width=200,
                   font=("Tahoma", 10),
                #    validate="key",
                #    validatecommand=(frame.register(on_validate), "%S", "%P"),
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

    if not all([pname, pdescription, category, pprice, pqty ]):
        messagebox.showerror("Error", "All fields are required!")
        return

    query = "INSERT INTO products (ProductName, Description, Category, Price, QuantityOnHand) VALUES ( %s, %s, %s, %s, %s)"
    values = (pname, pdescription, category, pprice, pqty )

    try:
        my_db.execute(query, values)
        my_connection.commit()
        messagebox.showinfo("Success", "Record created successfully!")
        # update_table()
        clear_btn()
        

    except mysql.connector.Error as err:
        messagebox.showerror("Error", "Failed to create record:Email is already exist")

add= CTkButton(
                   master=reports,
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

# Update the selected row>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

def update_data():
    pname = product_name.get()
    pdescription = description.get().strip()
    cat = combobox.get().strip()
    pprice = price.get().strip()
    pqty = qty.get().strip()
   
   
   
    try:
        if seller_id is not None:
            query = """
            UPDATE products
            SET ProductName = %s, Description = %s, Category = %s, Price = %s, QuantityOnHand = %s
            WHERE ProductID = %s
            """
            values = (pname,pdescription, cat,  pprice, pqty,seller_id)

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
                   master=reports,
                   text="Update",
                   border_color="#4D606E",
                   border_width=1,
                   fg_color="#4D606E",
                   width=94,
                   hover_color="#3FBAC2",
                   font=("Tahoma",10,"bold"),
                   cursor="hand2",
                   command=update_data
                  )
update.place(relx=0.2, rely=0.79)



label_for_cat= CTkLabel(
                 master=reports,
                 font=("Tahoma",10,"bold"),
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
                                     command=combobox_callback
                                    )
combobox.set("Choose category")
combobox.place(relx=0.37, rely=0.17 )



#<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

label_for_price= CTkLabel(
                 master=reports,
                 font=("Tahoma",10,"bold"),
                 text_color="#1B770C",
                 text="Price:"

                )
label_for_price.place(relx=0.37,rely=0.45)



price= CTkEntry(
                   master=reports,
                   border_color="#1B770C",
                   border_width=1,
                   width=200,
                   font=("Tahoma", 10)
                  )
price.place(relx=0.37, rely=0.6)



def choose_file():
    file_path = filedialog.askopenfilename()
    if file_path:
        display_image(file_path)
def display_image(file_path):
    img = Image.open(file_path)
    img.thumbnail((300, 300)) 
    img = CTkImage(img)
    image_label.configure(image=img)
    image_label.image = img,
 

image_frame= CTkFrame(master=reports,
                    
                  
                    border_color="#D37676",
                    border_width=1,
                    fg_color="#FFFFFF",
                    width=65,
                    height=65
                      
                      )
image_frame.place(relx=0.68, rely=0.38)

image_label = CTkLabel(
    master=image_frame,
    height=60,
    width=60,
  
    text="",
   

  
   
)
image_label.place(relx=0.03, rely=0.02)

file= CTkButton(
                   master=reports,
                   text="Choose File",
                   border_color="#D37676",
                   border_width=1,
                   fg_color="#D37676",
                   width=94,
                   hover_color="#EBC49F",
                   font=("Tahoma",10,"bold"),
                   cursor="hand2",
                   command=choose_file
                  )
file.place(relx=0.83, rely=0.5)


clear= CTkButton(
                   master=reports,
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
                   border_color="#BF3131",
                   border_width=1,
                   fg_color="#BF3131",
                   width=94,
                   hover_color="#EBC49F",
                   font=("Tahoma",10,"bold"),
                   cursor="hand2",
                   command=delete_record
                  )
delete.place(relx=0.52, rely=0.79)


search= CTkEntry(
                master=reports,
                border_color="#1B770C",
                border_width=1,
                width=150,
                placeholder_text="Search here....",
                font=("Tahoma", 10)
           )

search.place(relx=0.68, rely=0.79)


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
                   master=reports,
                   text="Search",
                   border_color="#1B770C",
                   border_width=1,
                   fg_color="#1B770C",
                   width=60,
                   hover_color="#87A922",
                   font=("Tahoma",10,"bold"),
                   cursor="hand2",
                    command=search_sellers
                 
     
                )
search_btn.place(relx=0.89, rely=0.79)
qty_label= CTkLabel(
                 master=reports,
                 font=("Tahoma",10,"bold"),
                 text_color="#1B770C",
                 text="Quantity:"

                )
qty_label.place(relx=0.68,rely=0.04)
qty= CTkEntry(
                   master=reports,
                   border_color="#1B770C",
                   border_width=1,
                   width=200,
                   font=("Tahoma", 10)
                  )
qty.place(relx=0.68, rely=0.18)

style = ttk.Style()
font_size = 14
header_color = "lightblue"
style.configure("Treeview.Heading", font=("Tahoma", font_size),background=header_color)
style.configure("Treeview", font=("Tahoma", 12))
tree = ttk.Treeview(frame, style="Treeview")

tree["columns"] = ("ProductID","ProductName", "Description", "Category", "Price", "QuantityOnHand")
tree.bind("<Configure>", lambda event: tree.column("#0", width=0))  


tree.column("#0", width=0)  
tree.column("ProductID", anchor="center", width=100) 
tree.column("ProductName", anchor="center", width=200)
tree.column("Description", anchor="center", width=120)
tree.column("Category", anchor="center", width=150)
tree.column("Price", anchor="center", width=200)
tree.column("QuantityOnHand", anchor="center", width=200)




tree.heading("#0", text="", anchor="center")  
tree.heading("ProductID", text="ProductID", anchor="center")
tree.heading("ProductName", text="ProductName", anchor="center")
tree.heading("Description", text="Description", anchor="center")
tree.heading("Category", text="Category", anchor="center")
tree.heading("Price", text="Price", anchor="center")
tree.heading("QuantityOnHand", text="Quantity", anchor="center")




query = "SELECT * FROM products"
my_db.execute(query)
data = my_db.fetchall()



for row in data:
    tree.insert("", "end", text="", values=row)



tree.place(relx=0.29,rely=0.4)
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
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>




app.mainloop()
      