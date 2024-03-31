import tkinter as tk
from customtkinter import*
import customtkinter
from PIL import Image
from tkinter import messagebox,ttk
import mysql.connector
import random
import string
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import dash_board
import subprocess
import re


my_connection= mysql.connector.connect(


                host="localhost",
                user="root",
                password="",
                database="hardware_db"
            
)


cursor= my_connection.cursor()



#Change passs
class ChangePassWindow(tk.Toplevel):
    def __init__(self, login_app):
        super().__init__(login_app)
        self.login_app = login_app
        self.title("Change Password")
        self.geometry("688x375")
        self.setup_ui()
    def back_to_login(self):
        self.destroy()
        self.login_app.deiconify()
    def setup_ui(self):


        def change_pass():
            p1= password_one.get()
            p2= password_two.get()
            verified_email
        
            query_users="SELECT * FROM sellers_tbl WHERE email= %s"

            cursor.execute(query_users, (verified_email,))
            user_data = cursor.fetchone()

            if not user_data:
                query_users="SELECT * FROM admin WHERE email= %s"
                cursor.execute(query_users, (verified_email,))
                user_data = cursor.fetchone()
            if user_data:
                if p1 == p2:
                        query_update_sellers = "UPDATE sellers_tbl SET password = %s WHERE email = %s"
                        cursor.execute(query_update_sellers, (p1, verified_email))

                        query_update_admin = "UPDATE admin SET password = %s WHERE email = %s"
                        cursor.execute(query_update_admin, (p1, verified_email))


                        my_connection.commit()
                        messagebox.showinfo("Success", "Password updated successfully!")
                        self.back_to_login()
                else:
                    messagebox.showerror("Error", "Passwords do not match!")



        frame = CTkFrame(master=self, width=688, height=375, fg_color="#F4F5F6")
        frame.pack(padx=10, pady=10,expand=True,)

        back = CTkButton(master=frame, font=("Tahoma",12,"bold"),fg_color="#9391E6",text="BACK TO LOGIN", width=100, command=self.back_to_login)
        back.place(relx=0.80, rely=0.05)

        my_image = customtkinter.CTkImage(light_image=Image.open("D:\\DS102PROJECT\\Icon\\image_1.png"),
                                  size=(300, 300))

        image_label = customtkinter.CTkLabel(master=frame, image=my_image, text="")
        image_label.place(relx=0.1,rely=0.1)


        password_label= CTkLabel(master=frame, text="Enter password",font=("Tahoma",12),text_color="#100E75")
        password_label.place(relx=0.6, rely=0.23)

        password_one=CTkEntry(master=frame,width=200, placeholder_text="Enter password",border_color="#9391E6",border_width=2)
        password_one.place(relx=0.6, rely=0.3)

        password_two_label= CTkLabel(master=frame, text="Confirm password",font=("Tahoma",12),text_color="#100E75")
        password_two_label.place(relx=0.6, rely=0.48)
        
        password_two=CTkEntry(master=frame,width=200, placeholder_text="Enter codes",border_color="#9391E6",border_width=2)
        password_two.place(relx=0.6, rely=0.56)
      
        changepass_btn = CTkButton(master=frame, font=("Tahoma",12,"bold"),fg_color="#9391E6",text="SUBMIT", width=200,command=change_pass)
        changepass_btn.place(relx=0.6, rely=0.68)


    


#forgot pass Classs
class ForgotPassWindow(tk.Toplevel):
    def __init__(self, login_app):
        super().__init__(login_app)
        self.login_app = login_app
        self.title("Forgot Password")
        self.geometry("688x375")
        self.setup_ui()
    def back_to_login(self):
        self.destroy()
        self.login_app.deiconify()
    
    def change_password(self):
        self.withdraw()
        ChangePassWindow(self)
    def setup_ui(self):
        def generate_code():
            code_length = 6
            return ''.join(random.choices( string.digits, k=code_length))
        def send_code_method():
            email_text = email.get()
            if not email_text:
                messagebox.showerror("Error", "Please fill the email textbox!")
            else:
               
                query_users = "SELECT * FROM sellers_tbl WHERE email = %s"
                cursor.execute(query_users, (email_text,))
                user_data = cursor.fetchone()

                if not user_data:
                    query_admin = "SELECT * FROM admin WHERE email = %s"
                    cursor.execute(query_admin, (email_text,))
                    user_data = cursor.fetchone()

                if user_data:
                    global codes
                    codes = generate_code()
                    global verified_email
                    verified_email= email_text
                    send_email(email_text, codes)
                   
                    code.configure(state='normal')
                    messagebox.showinfo("Success", "Code sent to your email. Check your inbox.")
                    email.delete(0,'end')

                else:
                    messagebox.showerror("Error", "Email not registered. Please try again.")

        def send_email(receiver_email, codes):
            sender_email = "xmontemorjerald@gmail.com" 
            password = "cict wsqr cadd jjio" 

            message = MIMEMultipart()
            message["From"] = sender_email
            message["To"] = receiver_email
            message["Subject"] = "Password Reset Code"

            body = f"Your password reset code is: {codes}"
            message.attach(MIMEText(body, "plain"))

            with smtplib.SMTP("smtp.gmail.com", 587) as server:
                server.starttls()
                server.login(sender_email, password)
                server.sendmail(sender_email, receiver_email, message.as_string())
    
        def the_code():
            global codes
             
            six_codes = code.get()
            
        
          
            
            if not six_codes:
                messagebox.showerror("Error", "Invalid Input.")

   
            elif six_codes==codes:
                 
                  messagebox.showinfo("Succcess", "You can now change your password!.")

                  self.change_password()
            else:
                messagebox.showerror("Error", "The code have entered did not match.")
        
         
        frame = CTkFrame(master=self, width=688, height=375, fg_color="#F4F5F6")
        frame.pack(padx=10, pady=10,expand=True,)

        back = CTkButton(master=frame, font=("Tahoma",12,"bold"),fg_color="#9391E6",text="BACK TO LOGIN", width=100, command=self.back_to_login)
        back.place(relx=0.80, rely=0.05)

        my_image = customtkinter.CTkImage(light_image=Image.open("D:\\DS102PROJECT\\Icon\\image_1.png"),
                                  size=(300, 300))

        image_label = customtkinter.CTkLabel(master=frame, image=my_image, text="")
        image_label.place(relx=0.1,rely=0.1)

        email_label= CTkLabel(master=frame, text="Email:",font=("Tahoma",12),text_color="#100E75")
        email_label.place(relx=0.6, rely=0.23)

        def on_validate( entry_value):
   
            return  len(entry_value) < 30 
        def on_limit(char, entry_value):
            return  len(entry_value) < 30
        def on_code(char, entry_value):
             return char.isdigit() and len(entry_value) <= 6
#<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<EMAIL VALIDATAION AND CODE>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        email=CTkEntry(master=frame,width=200, placeholder_text="Enter email",border_color="#9391E6",border_width=2,
                       validate="key",validatecommand=(frame.register(on_validate),"%P"))
        email.place(relx=0.6, rely=0.3)

        send_code=CTkButton(master=frame, font=("Tahoma",12,"bold"),text="SEND CODE",fg_color="#9391E6", width=100,command=send_code_method)
        send_code.place(relx=0.75, rely=0.40)

        code_label= CTkLabel(master=frame, text="Enter 6 digits code",font=("Tahoma",12),text_color="#100E75")
        code_label.place(relx=0.6, rely=0.48)
        
        code=CTkEntry(master=frame,width=200, placeholder_text="Enter codes",border_color="#9391E6",border_width=2,
                       validate="key",validatecommand=(frame.register(on_code), "%S", "%P"),justify="center", state='disabled')
        code.place(relx=0.6, rely=0.56)
#<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
      
        verify = CTkButton(master=frame, font=("Tahoma",12,"bold"),fg_color="#9391E6",text="SUBMIT", width=200, command=the_code)
        verify.place(relx=0.6, rely=0.68)

       


   

        

#Login class
class LoginApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Login")
        self.geometry("688x375")
        self.setup_login()

    def open_add_seller(self):
        self.withdraw()
        ForgotPassWindow(self)
   
     

    def setup_login(self):

        def login_clicked():
       
            my_db= my_connection.cursor()
            emails = email.get()
            passwords = password.get()
            
            if not all([emails,passwords]):
                messagebox.showerror("Error", "All fields are required!")
                return

            query = "SELECT COUNT(*) FROM sellers_tbl WHERE email=%s AND password=%s"
            data = (emails, passwords)

            try:
                my_db.execute(query, data)
                result = my_db.fetchone()

                
                if result and result[0] > 0:

                    self.withdraw()
                    subprocess.Popen(["python", r"D:\DS102PROJECT\Src\\dash_board.py"])
                  
                    
                    
                else:
                    messagebox.showerror("Error", "Invalid email or password!")

            except mysql.connector.Error as err:
                messagebox.showerror("Error", f"Failed to query database: {err}")

#<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<lOGIN WIDGETS>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        frame = CTkFrame(master=self, width=688, height=375, fg_color="#F4F5F6")
        frame.pack(padx=10, pady=10,expand=True,)

       
        
        my_image = customtkinter.CTkImage(light_image=Image.open("D:\\DS102PROJECT\\Icon\\image_3.png"),
                                  size=(300, 300))

        image_label = customtkinter.CTkLabel(master=frame, image=my_image, text="")
        image_label.place(relx=0.1,rely=0.1)


        email_label= CTkLabel(master=frame, text="Email:",font=("Tahoma",12),text_color="#100E75")
        email_label.place(relx=0.6, rely=0.32)

#<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<EMAIL VALIDATION AND PASSWORD>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        def on_validate( entry_value):
   
            return  len(entry_value) < 30 
        def on_limit(char, entry_value):
            return  len(entry_value) < 30 
      
#<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<EMAIL VALIDATION>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
      
        email=CTkEntry(master=frame,width=200, placeholder_text="Enter email",border_color="#9391E6",border_width=2,
                       validate="key",validatecommand=(frame.register(on_validate),"%P")
)
        email.place(relx=0.6, rely=0.4)
#<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<EMAIL VALIDATION>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>


        password_label= CTkLabel(master=frame, text="Password:",font=("Tahoma",12),text_color="#100E75")
        password_label.place(relx=0.6, rely=0.48)
        
        password=CTkEntry(master=frame,width=200, placeholder_text="Enter password",border_color="#9391E6",border_width=2,show="*",
                          validate="key",validatecommand=(frame.register(on_limit),"%S","%P"))
        password.place(relx=0.6, rely=0.56)


        def checkbox_event():
    
            if check_var.get() == "on":
                password.configure(show="")
            else:
                password.configure(show="*")
        check_var = customtkinter.StringVar(value="off")

        checkbox = CTkCheckBox(master=frame, text="Show password", command=checkbox_event,
                                            variable=check_var, onvalue="on", offvalue="off",checkbox_height=15, checkbox_width=17,
                                            bg_color="#F4F5F6", font=("Tahoma", 10))
        checkbox.place(relx=0.76, rely=0.66)
        
        login_btn = CTkButton(master=frame, font=("Tahoma",12,"bold"),text="Login", width=200,command=login_clicked)
        login_btn.place(relx=0.6, rely=0.75)

        forgot_pass = CTkButton(master=frame, hover_color="#F4F5F6",text="forgot password?",font=("Tahoma",10),text_color="#100E75",fg_color="#F4F5F6", width=200,command=self.open_add_seller)
        forgot_pass.place(relx=0.6, rely=0.85)

def main():
    app = LoginApp()
    app.mainloop()

if __name__ == "__main__":
    main()

