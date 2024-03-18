

from pathlib import Path
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage
from dash_board import DashboardApp
import mysql.connector
from tkinter import messagebox
OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"\DS102PROJECT\Assets\assets\frame0")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

#MYSQL CONNECTOR 
my_connection= mysql.connector.connect(


    host="localhost",
    user="root",
    password="",
    database="hardware_db"
  
)
my_db= my_connection.cursor()






#<<<<<<<<<<<<<<<<<<<<<<<<<<<<LOGIN PROCES>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    
def login_clicked():
    firstname = entry_1.get()
    password = entry_2.get()

    if not all([firstname, password]):
        messagebox.showerror("Error", "All fields are required!")
        return

    query = "SELECT COUNT(*) FROM sellers_tbl WHERE email=%s AND password=%s"
    data = (firstname, password)

    try:
        my_db.execute(query, data)
        result = my_db.fetchone()

        
        if result and result[0] > 0:
            window.destroy() 
            open_dashboard()
        else:
            messagebox.showerror("Error", "Invalid email or password!")

    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Failed to query database: {err}")
    


#<<<<<<<<<<<<<<<<<<<<<<<< LOGIN WIDGETS>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

window = Tk()

window.geometry("688x375")
window.configure(bg = "#F4F5F6")
window.title('Login')
window.iconbitmap('/DS102PROJECT/Icon/hardwareIco.ico')
window.minsize(688,375)


canvas = Canvas(
    window,
    bg = "#F4F5F6",
    height = 375,
    width = 688,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

canvas.place(x = 0, y = 0)
image_image_1 = PhotoImage(
    file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(
    521.0,
    191.0,
    image=image_image_1
)

entry_image_1 = PhotoImage(
    file=relative_to_assets("entry_1.png"))
entry_bg_1 = canvas.create_image(
    521.0,
    160.5,
    image=entry_image_1
)
entry_1 = Entry(
    canvas,
    bd=0,
    bg="#FFFFFF",
    fg="#000716",
    highlightthickness=0
)
entry_1.place(
    x=412.0,
    y=148.0,
    width=218.0,
    height=23.0
)

entry_image_2 = PhotoImage(
    file=relative_to_assets("entry_2.png"))
entry_bg_2 = canvas.create_image(
    521.0,
    215.5,
    image=entry_image_2
)
entry_2 = Entry(
    canvas,
    bd=0,
    bg="#FFFFFF",
    fg="#000716",
    highlightthickness=0,
    show="*"
)
entry_2.place(
    x=412.0,
    y=203.0,
    width=218.0,
    height=23.0
)

canvas.create_text(
    408.0,
    128.0,
    anchor="nw",
    text="Email",
    fill="#0F0D74",
    font=("IstokWeb Bold", 11 * -1)
)

canvas.create_text(
    408.0,
    181.0,
    anchor="nw",
    text="Password",
    fill="#0F0D74",
    font=("IstokWeb Bold", 11 * -1)
)

button_image_1 = PhotoImage(
    file=relative_to_assets("button_1.png"))
button_1 = Button(
    canvas,
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=login_clicked,
    relief="flat"
)
button_1.place(
    x=408.0,
    y=269.0,
    width=226.0,
    height=27.0
)

image_image_2 = PhotoImage(
    file=relative_to_assets("image_2.png"))
image_2 = canvas.create_image(
    534.0,
    86.0,
    image=image_image_2
)

button_image_2 = PhotoImage(
    file=relative_to_assets("button_2.png"))
button_2 = Button(
    canvas,
    image=button_image_2,
    borderwidth=0,
    highlightthickness=0,
    command=lambda:print("hello world"),
    relief="flat"
)
button_2.place(
    x=499.0,
    y=245.0,
    width=72.0,
    height=14.0
)

image_image_3 = PhotoImage(
    file=relative_to_assets("image_3.png"))
image_3 = canvas.create_image(
    190.0,
    190.0,
    image=image_image_3
)

canvas.pack(expand=True)
window.resizable(True, True)
def open_dashboard():
    root = Tk()
    root.title("Welcome Administrator") 
    app = DashboardApp(root)
    root.mainloop()
window.mainloop()


