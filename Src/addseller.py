from customtkinter import*
import tkinter
import customtkinter
from PIL import Image
from CTkTable import *
import mysql.connector
from tkinter import messagebox,ttk
from dash_board import DashboardApp


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
                  text="Add seller",
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
# img_1= Image.open("/DS102PROJECT/Icon/dashboard.png")
# dashboard_instance = DashboardApp(master=app)
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
                    height=155,
                    width=720,
                    border_width=0,
                    # border_color="#9391E6",
                    fg_color="#FFFFFF"
                    )
reports.place(relx=0.25,rely=0.048)
label_for_name= CTkLabel(
                 master=reports,
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
                 text_color="#1B770C",
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

def create_record():
    name = full_name.get()
    contacts = contact.get()
    addresss = address.get()
    emails = email.get()
    passwords = password.get()

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



label_for_address= CTkLabel(
                 master=reports,
                 font=("Tahoma",10,"bold"),
                 text_color="#1B770C",
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
                 text_color="#1B770C",
                 text="Email:"

                )
label_for_email.place(relx=0.37,rely=0.45)



email= CTkEntry(
                   master=reports,
                   border_color="#1B770C",
                   border_width=1,
                   width=200,
                   font=("Tahoma", 10)
                  )
email.place(relx=0.37, rely=0.6)
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
password_label= CTkLabel(
                 master=reports,
                 font=("Tahoma",10,"bold"),
                 text_color="#1B770C",
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
    global password
    
    if check_var.get() == "on":
        password.configure(show="")
    else:
        password.configure(show="*")
    print("checkbox toggled, current value:", check_var.get())


check_var = customtkinter.StringVar(value="off")
checkbox = customtkinter.CTkCheckBox(master=reports, text="show password", command=checkbox_event,
                                     variable=check_var, onvalue="on", offvalue="off",checkbox_height=15, checkbox_width=15)

checkbox.place(x=561, y=65)

refresh=CTkButton(master=frame,
                  
                   text="Refresh",
                   border_color="#1B770C",
                   border_width=1,
                   fg_color="#1B770C",
                   width=60,
                   hover_color="#87A922",
                   font=("Tahoma",10,"bold"),
                   cursor="hand2",
                   command=search_sellers
                  )

refresh.place(relx=0.88,rely=0.33)


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



tree.place(relx=0.29,rely=0.4)
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
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>


app.mainloop()
      