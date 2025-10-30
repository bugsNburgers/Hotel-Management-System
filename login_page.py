# login_page.py
import tkinter as tk
from tkinter import ttk, messagebox
from database import Database
from dashboard_admin import AdminDashboard
from dashboard_manager import ManagerDashboard
from dashboard_customer import CustomerDashboard

db = Database()

class LoginPage:
    def __init__(self, root):
        self.root = root
        self.root.title("Hotel Booking — Login")
        self.root.configure(bg='#f0f8ff')
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TFrame', background='#f0f8ff')
        style.configure('TLabel', background='#f0f8ff', font=('Segoe UI', 12))
        style.configure('TEntry', font=('Segoe UI', 11))
        style.configure('TButton', font=('Segoe UI', 11, 'bold'), background='#4CAF50', foreground='white')

        frm = ttk.Frame(root, padding=30, style='TFrame')
        frm.place(relx=0.5, rely=0.5, anchor='center')

        ttk.Label(frm, text="🏨 Hotel Booking System", font=('Segoe UI', 18, 'bold'), foreground='#2E8B57').grid(row=0, column=0, columnspan=2, pady=(0,20))

        ttk.Label(frm, text="Username:").grid(row=1, column=0, sticky='e', pady=8)
        ttk.Label(frm, text="Password:").grid(row=2, column=0, sticky='e', pady=8)

        self.username = tk.StringVar()
        self.password = tk.StringVar()

        ttk.Entry(frm, textvariable=self.username, width=35).grid(row=1, column=1, padx=10, pady=8)
        ttk.Entry(frm, textvariable=self.password, show='*', width=35).grid(row=2, column=1, padx=10, pady=8)

        ttk.Button(frm, text="🔐 Login", command=self.do_login).grid(row=3, column=0, columnspan=2, pady=15)
        ttk.Separator(frm, orient='horizontal').grid(row=4, column=0, columnspan=2, sticky='ew', pady=10)
        ttk.Label(frm, text="(Admin: admin/adminpass | Customer: johndoe@example.com/secret)", font=('Segoe UI', 9), foreground='#666').grid(row=5, column=0, columnspan=2)

    def do_login(self):
        u = self.username.get().strip()
        p = self.password.get().strip()
        if not u or not p:
            messagebox.showerror("Login", "Enter credentials")
            return
        try:
            # First check Login table for staff
            row = db.fetch("SELECT user_id FROM Login WHERE username=%s AND password=%s", (u, p))
            if row:
                user_id = row[0][0]
                # find role (assume single role per user for routing)
                role_rows = db.fetch(
                    "SELECT r.role_name FROM Roles r JOIN User_Roles ur ON r.role_id=ur.role_id WHERE ur.user_id=%s",
                    (user_id,)
                )
                role = role_rows[0][0] if role_rows else 'customer'
                # open appropriate dashboard
                self.root.destroy()
                root2 = tk.Tk()
                if role.lower() in ('admin',):
                    AdminDashboard(root2, user_id)
                elif role.lower() in ('manager',):
                    ManagerDashboard(root2, user_id)
                else:
                    CustomerDashboard(root2, user_id)
                root2.mainloop()
            else:
                # Check Customer table for customers (use email as username)
                cust_row = db.fetch("SELECT cust_id FROM Customer WHERE cust_email=%s AND cust_pass=%s", (u, p))
                if cust_row:
                    cust_id = cust_row[0][0]
                    # open customer dashboard
                    self.root.destroy()
                    root2 = tk.Tk()
                    CustomerDashboard(root2, cust_id)
                    root2.mainloop()
                else:
                    messagebox.showerror("Login Failed", "Invalid username/password")
        except Exception as e:
            messagebox.showerror("DB Error", str(e))
