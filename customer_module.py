# customer_module.py
import tkinter as tk
from tkinter import ttk, messagebox
from database import Database

db = Database()

class CustomerFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent, padding=10)
        btnf = ttk.Frame(self); btnf.pack(fill='x', pady=6)
        ttk.Button(btnf, text="🔄 Refresh", command=self.refresh).pack(side='left')
        ttk.Button(btnf, text="➕ Add Customer", command=self.add_customer).pack(side='left', padx=6)

        cols = ('ID','Name','Email','Mobile')
        self.tree = ttk.Treeview(self, columns=cols, show='headings', height=14)
        for c in cols:
            self.tree.heading(c, text=c)
            self.tree.column(c, width=160)
        self.tree.pack(fill='both', expand=True)
        self.refresh()

    def refresh(self):
        rows = db.fetch("SELECT cust_id, cust_name, cust_email, cust_mobile FROM Customer")
        for i in self.tree.get_children():
            self.tree.delete(i)
        for r in rows:
            self.tree.insert('', 'end', values=r)

    def add_customer(self):
        d = AddCustomerDialog(self)
        self.wait_window(d.top)
        if d.result:
            name,email,mobile,password = d.result
            db.execute("INSERT INTO Customer (cust_name, cust_email, cust_mobile, cust_pass) VALUES (%s,%s,%s,%s)",
                       (name,email,mobile,password))
            messagebox.showinfo("OK","Customer added")
            self.refresh()

class AddCustomerDialog:
    def __init__(self, parent):
        top = tk.Toplevel(parent)
        top.title("Add Customer")
        ttk.Label(top, text="Name").grid(row=0, column=0, padx=6, pady=6)
        ttk.Label(top, text="Email").grid(row=1, column=0, padx=6, pady=6)
        ttk.Label(top, text="Mobile").grid(row=2, column=0, padx=6, pady=6)
        ttk.Label(top, text="Password").grid(row=3, column=0, padx=6, pady=6)
        self.e_name = tk.StringVar(); self.e_email = tk.StringVar()
        self.e_mob = tk.StringVar(); self.e_pass = tk.StringVar()
        ttk.Entry(top, textvariable=self.e_name).grid(row=0,column=1)
        ttk.Entry(top, textvariable=self.e_email).grid(row=1,column=1)
        ttk.Entry(top, textvariable=self.e_mob).grid(row=2,column=1)
        ttk.Entry(top, textvariable=self.e_pass, show='*').grid(row=3,column=1)
        ttk.Button(top, text="Add", command=self.on_add).grid(row=4, column=0, columnspan=2, pady=8)
        self.top = top; self.result = None
    def on_add(self):
        self.result = (self.e_name.get(), self.e_email.get(), self.e_mob.get(), self.e_pass.get())
        self.top.destroy()
