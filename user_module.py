# user_module.py
import tkinter as tk
from tkinter import ttk, messagebox
from database import Database

db = Database()

class UserFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent, padding=10)
        btnf = ttk.Frame(self); btnf.pack(fill='x', pady=6)
        ttk.Button(btnf, text="🔄 Refresh", command=self.refresh).pack(side='left')
        ttk.Button(btnf, text="➕ Add User", command=self.add_user).pack(side='left', padx=6)
        ttk.Button(btnf, text="👤 Assign Role", command=self.assign_role).pack(side='left', padx=6)

        cols = ('UserID','Name','Email','Mobile')
        self.tree = ttk.Treeview(self, columns=cols, show='headings', height=14)
        for c in cols:
            self.tree.heading(c, text=c); self.tree.column(c, width=160)
        self.tree.pack(fill='both', expand=True)
        self.refresh()

    def refresh(self):
        rows = db.fetch("SELECT user_id, user_name, user_email, user_mobile FROM `User`")
        for i in self.tree.get_children():
            self.tree.delete(i)
        for r in rows:
            self.tree.insert('', 'end', values=r)

    def add_user(self):
        d = AddUserDialog(self)
        self.wait_window(d.top)
        if d.result:
            name,email,mobile,username,password = d.result
            # insert into user + login
            uid = db.execute("INSERT INTO `User` (user_name, user_email, user_mobile) VALUES (%s,%s,%s)",
                            (name,email,mobile))
            db.execute("INSERT INTO Login (user_id, username, password) VALUES (%s,%s,%s)",
                       (uid, username, password))
            messagebox.showinfo("OK","User created")
            self.refresh()

    def assign_role(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Select", "Select a user first")
            return
        uid = self.tree.item(sel[0], 'values')[0]
        # show roles
        roles = db.fetch("SELECT role_id, role_name FROM Roles")
        if not roles:
            messagebox.showwarning("Roles", "No roles present. Add roles in DB first.")
            return
        # simple assignment dialog
        top = tk.Toplevel(self)
        top.title("Assign Role")
        ttk.Label(top, text="Choose role:").pack(padx=6,pady=6)
        rb = ttk.Combobox(top, values=[r[1] for r in roles])
        rb.pack(padx=6,pady=6)
        def do_assign():
            choice = rb.get()
            rid = next(r[0] for r in roles if r[1]==choice)
            db.execute("INSERT INTO User_Roles (user_id, role_id) VALUES (%s,%s)", (uid, rid))
            messagebox.showinfo("OK","Assigned")
            top.destroy()
        ttk.Button(top, text="Assign", command=do_assign).pack(pady=6)

class AddUserDialog:
    def __init__(self, parent):
        top = tk.Toplevel(parent); top.title("Add User")
        ttk.Label(top,text="Name").grid(row=0,column=0,padx=6,pady=4)
        ttk.Label(top,text="Email").grid(row=1,column=0,padx=6,pady=4)
        ttk.Label(top,text="Mobile").grid(row=2,column=0,padx=6,pady=4)
        ttk.Label(top,text="Username (login)").grid(row=3,column=0,padx=6,pady=4)
        ttk.Label(top,text="Password").grid(row=4,column=0,padx=6,pady=4)
        self.en = tk.StringVar(); self.ee = tk.StringVar(); self.em = tk.StringVar()
        self.eu = tk.StringVar(); self.ep = tk.StringVar()
        ttk.Entry(top, textvariable=self.en).grid(row=0,column=1)
        ttk.Entry(top, textvariable=self.ee).grid(row=1,column=1)
        ttk.Entry(top, textvariable=self.em).grid(row=2,column=1)
        ttk.Entry(top, textvariable=self.eu).grid(row=3,column=1)
        ttk.Entry(top, textvariable=self.ep, show='*').grid(row=4,column=1)
        ttk.Button(top, text="Create", command=self.on_create).grid(row=5,column=0,columnspan=2,pady=8)
        self.top = top; self.result = None
    def on_create(self):
        self.result = (self.en.get(), self.ee.get(), self.em.get(), self.eu.get(), self.ep.get())
        self.top.destroy()
