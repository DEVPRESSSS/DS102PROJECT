                   
from customtkinter import CTk, CTkFrame, CTkButton, CTkImage, CTkLabel, CTkTabview
import tkinter as tk
from PIL import Image
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import subprocess
import mysql.connector
from tkinter import messagebox,ttk





my_connection= mysql.connector.connect(


    host="localhost",
    user="root",
    password="",
    database="hardware_db"
  
)
my_db= my_connection.cursor()

class DashboardApp:
    def __init__(self, master):
        self.master = master
        self.setup_dashboard()
        
    def setup_dashboard(self):
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
                                        height=550)
        tabview.place(relx=0.025,rely=0.01)

        tabview.add("tab 1") 
        tabview.rename("tab 1","View transactions")
        tabview.add("tab 2")  
        tabview.rename("tab 2","View supplier")
        tabview.add("tab 3")
        tabview.rename("tab 3","View purchase")
        tabview.set("View supplier")

        button = CTkButton(master=tabview.tab("View transactions"))
        button.pack(padx=20, pady=20)
        


   

    

       


def main():
    root = CTk()
    root.title("Your Dashboard Title")  
    app = DashboardApp(root)
    root.mainloop()
    


if __name__ == "__main__":
    main()
