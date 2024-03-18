                   
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
        self.seller_report() 
        self.categories_report()
        self.products_report()
    def open_add_seller(self):
          self.master.destroy()
          subprocess.Popen(["python", r"D:\DS102PROJECT\Src\addseller.py"])
    def open_add_product(self):
          self.master.destroy()
          subprocess.Popen(["python", r"D:\DS102PROJECT\Src\manage_product.py"])
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

        # SIDE BAR
        sidebar = CTkFrame(
            master=frame,
            height=545,
            width=200,
            border_width=1,
            border_color="#1B770C",
            fg_color="#1B770C"
        )
        sidebar.place(relx=0.02, rely=0.03)

        button_width = 125
        
        product_btn = CTkButton(
            master=sidebar,
            text="Manage product",
            height=25,
            width=button_width,
            fg_color="transparent",
            border_width=1,
            hover_color="#C850C0",
            border_color="#FFFFFF",
            corner_radius=10,
            font=("Tahoma", 10, "bold"),
            cursor="hand2",
            command=self.open_add_product
            
        )
        product_btn.place(relx=0.2, rely=0.2)

        
        categories_btn = CTkButton(
            master=sidebar,
            text="Manage category",
            height=25,
            width=button_width,
            fg_color="transparent",
            border_width=1,
            hover_color="#C850C0",
            border_color="#FFFFFF",
            corner_radius=10,
            font=("Tahoma", 10, "bold"),
            cursor="hand2",
            # image=CTkImage(dark_image=img_2, light_image=img_2)
        )
        categories_btn.place(relx=0.2, rely=0.26)

        # img_3= Image.open("/DS102PROJECT/Icon/business-man.png")
        seller_btn= CTkButton(master=sidebar,
                text="Manage seller",
                height=25,
                width=button_width,
                fg_color="transparent",
                border_width=1,
                hover_color="#C850C0",
                border_color="#FFFFFF",
                corner_radius=10,
                command=self.open_add_seller,
                font=("Tahoma", 10,"bold"),
                # image=CTkImage(dark_image=img_3, light_image=img_3),
                cursor="hand2" 
                            )
        seller_btn.place(relx=0.2, rely=0.32)
        # img_4= Image.open("/DS102PROJECT/Icon/sales.png")
        sales_report= CTkButton(master=sidebar,
                            text="Sales report",
                            height=25,
                            width=button_width,
                            fg_color="transparent",
                            border_width=1,
                            hover_color="#C850C0",
                            border_color="#FFFFFF",
                            corner_radius=10,
                            font=("Tahoma", 10,"bold"),
                            # image=CTkImage(dark_image=img_4, light_image=img_4),

                            cursor="hand2" 
                            )
        sales_report.place(relx=0.2, rely=0.38)

        # img_5 = Image.open("/DS102PROJECT/Icon/increase.png")  # Replace with the actual path
        view_chart = CTkButton(
            master=sidebar,
            text="View Chart",
            height=25,
            width=button_width,
            fg_color="transparent",
            border_width=1,
            hover_color="#C850C0",
            border_color="#FFFFFF",
            corner_radius=10,
            font=("Tahoma", 10, "bold"),
            # image=CTkImage(dark_image=img_5, light_image=img_5),
            cursor="hand2",
            command=self.chart
        )
        view_chart.place(relx=0.2, rely=0.44)

        # img_6= Image.open("/DS102PROJECT/Icon/settings.png")
        view_profile= CTkButton(master=sidebar,
                        text="Manage profile",
                        height=25,
                        width=button_width,
                        fg_color="transparent",
                        border_width=1,
                        hover_color="#C850C0",
                        border_color="#FFFFFF",
                        corner_radius=10,
                        font=("Tahoma", 10,"bold"),
                        # image=CTkImage(dark_image=img_6, light_image=img_6),
                        cursor="hand2" 
                        )
        view_profile.place(relx=0.2, rely=0.50)
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
                        fg_color="#0B666A",
                        border_width=1,
                        border_color="#9391E6",

                        )
    


        panel_2= CTkFrame(
                        master=reports,
                        height=135,
                        width=200,
                        fg_color="#0B666A",
                        border_width=1,
                        border_color="#9391E6",
                        )
    


        panel_3= CTkFrame(
                        master=reports,
                        height=135,
                        width=200,
                        fg_color="#0B666A",
                        border_width=1,
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
                                text_color="#FFFFFF"
                                )
        label_product.place(relx=0.32,rely=0.1)
        global product_count
        product_count= CTkLabel(master=panel_1,
                                text="0",
                                font=("Tahoma",18, "bold"),
                                text_color="#FFFFFF"
                                )
        product_count.place(relx=0.45,rely=0.4)

        label_category= CTkLabel(master=panel_2,
                                text="Categories",
                                font=("Tahoma",14, "bold"),
                                text_color="#FFFFFF"
                                )
        label_category.place(relx=0.32,rely=0.1)
        global category_count
        category_count= CTkLabel(master=panel_2,
                                text="0",
                                font=("Tahoma",18, "bold"),
                                text_color="#FFFFFF"
                                )
        category_count.place(relx=0.45,rely=0.4)
      
        label_seller= CTkLabel(master=panel_3,
                                text="Sellers",
                                font=("Tahoma",14, "bold"),
                                text_color="#FFFFFF"
                                )
        
        label_seller.place(relx=0.32,rely=0.1)

        global seller_count
        seller_count= CTkLabel(master=panel_3,
                                text="0",
                                font=("Tahoma",18, "bold"),
                                text_color="#FFFFFF"
                                )
        seller_count.place(relx=0.45,rely=0.4)
        tabview =CTkTabview(master=frame,
                                        width=720,
                                        height=390)
        tabview.place(relx=0.25,rely=0.3)

        tabview.add("tab 1") 
        tabview.rename("tab 1","View transactions")
        tabview.add("tab 2")  
        tabview.rename("tab 2","View supplier")
        tabview.add("tab 3")
        tabview.rename("tab 3","View purchase")
        tabview.set("View supplier")

        button = CTkButton(master=tabview.tab("View transactions"))
        button.pack(padx=20, pady=20)
        


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
    root = CTk()
    root.title("Your Dashboard Title")  
    app = DashboardApp(root)
    root.mainloop()
    


if __name__ == "__main__":
    main()
