# hotel_module.py
import tkinter as tk
from tkinter import ttk, messagebox
from database import Database

db = Database()

class HotelFrame(ttk.Frame):
    def __init__(self, parent, manager_id=None, allow_book=False):
        super().__init__(parent, padding=10)
        self.manager_id = manager_id
        self.allow_book = allow_book

        # top controls
        ctrl = ttk.Frame(self)
        ctrl.pack(fill='x', pady=6)
        ttk.Button(ctrl, text="🔄 Refresh", command=self.refresh).pack(side='left')
        if self.manager_id is not None:
            ttk.Button(ctrl, text="➕ Add Hotel", command=self.add_hotel).pack(side='left', padx=6)
            ttk.Button(ctrl, text="🏷️ Add Class", command=self.add_class).pack(side='left', padx=6)

        # treeview
        if self.allow_book:
            cols = ('ID', 'Name', 'Type', 'Classes')
            self.tree = ttk.Treeview(self, columns=cols, show='headings', height=15)
            for c in cols:
                self.tree.heading(c, text=c, anchor='w')
                self.tree.column(c, width=140 if c != 'Classes' else 300, anchor='w')
        else:
            cols = ('ID', 'Name', 'Type', 'Rent', 'Desc')
            self.tree = ttk.Treeview(self, columns=cols, show='headings', height=15)
            for c in cols:
                self.tree.heading(c, text=c, anchor='w')
                self.tree.column(c, width=140 if c != 'Desc' else 300, anchor='w')
        self.tree.pack(fill='both', expand=True, pady=6)

        # double-click opens edit
        self.tree.bind("<Double-1>", lambda e: self.edit_selected())

        self.refresh()

    def refresh(self):
        if self.allow_book:
            q = """
            SELECT h.hotel_id, h.hotel_name, h.hotel_type,
                   GROUP_CONCAT(CONCAT(hc.class_name, ' (', hc.class_rent, ')') SEPARATOR ', ') as classes
            FROM Hotel h LEFT JOIN Hotel_Class hc ON h.hotel_id = hc.hotel_id
            GROUP BY h.hotel_id
            """
            rows = db.fetch(q)
            for i in self.tree.get_children():
                self.tree.delete(i)
            for r in rows:
                self.tree.insert('', 'end', values=r)
        else:
            q = "SELECT hotel_id, hotel_name, hotel_type, hotel_rent, hotel_desc FROM Hotel"
            rows = db.fetch(q)
            for i in self.tree.get_children():
                self.tree.delete(i)
            for r in rows:
                self.tree.insert('', 'end', values=r)

    def add_hotel(self):
        d = HotelDialog(self, title="Add Hotel")
        self.wait_window(d.top)
        if d.result:
            name, htype, rent, desc = d.result
            try:
                db.execute("INSERT INTO Hotel (hotel_name, hotel_type, hotel_rent, hotel_desc, user_id) VALUES (%s,%s,%s,%s,%s)",
                           (name, htype, rent, desc, self.manager_id))
                messagebox.showinfo("OK", "Hotel added")
                self.refresh()
            except Exception as e:
                messagebox.showerror("Err", str(e))

    def edit_selected(self):
        sel = self.tree.selection()
        if not sel:
            return
        vals = self.tree.item(sel[0], 'values')
        hid = vals[0]
        d = HotelDialog(self, title="Edit Hotel", values=vals)
        self.wait_window(d.top)
        if d.result:
            name, htype, rent, desc = d.result
            db.execute("UPDATE Hotel SET hotel_name=%s, hotel_type=%s, hotel_rent=%s, hotel_desc=%s WHERE hotel_id=%s",
                       (name, htype, rent, desc, hid))
            messagebox.showinfo("Updated", "Hotel updated")
            self.refresh()

class HotelDialog:
    def __init__(self, parent, title="Hotel", values=None):
        top = tk.Toplevel(parent)
        top.title(title)
        ttk.Label(top, text="Name:").grid(row=0, column=0, sticky='e', padx=6, pady=6)
        ttk.Label(top, text="Type:").grid(row=1, column=0, sticky='e', padx=6, pady=6)
        ttk.Label(top, text="Rent:").grid(row=2, column=0, sticky='e', padx=6, pady=6)
        ttk.Label(top, text="Desc:").grid(row=3, column=0, sticky='ne', padx=6, pady=6)
        self.e_name = tk.StringVar(value=values[1] if values else "")
        self.e_type = tk.StringVar(value=values[2] if values else "")
        self.e_rent = tk.StringVar(value=values[3] if values else "0.0")
        self.e_desc = tk.StringVar(value=values[4] if values else "")
        ttk.Entry(top, textvariable=self.e_name, width=40).grid(row=0, column=1, padx=6, pady=6)
        ttk.Entry(top, textvariable=self.e_type, width=40).grid(row=1, column=1, padx=6, pady=6)
        ttk.Entry(top, textvariable=self.e_rent, width=40).grid(row=2, column=1, padx=6, pady=6)
        ttk.Entry(top, textvariable=self.e_desc, width=60).grid(row=3, column=1, padx=6, pady=6)
        ttk.Button(top, text="OK", command=self.on_ok).grid(row=4, column=0, columnspan=2, pady=8)
        self.top = top
        self.result = None

    def on_ok(self):
        try:
            rent = float(self.e_rent.get())
        except:
            rent = 0.0
        self.result = (self.e_name.get(), self.e_type.get(), rent, self.e_desc.get())
        self.top.destroy()

    def add_class(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Select", "Select a hotel first")
            return
        hid = self.tree.item(sel[0], 'values')[0]
        d = ClassDialog(self, title="Add Class to Hotel")
        self.wait_window(d.top)
        if d.result:
            cname, crent = d.result
            try:
                db.execute("INSERT INTO Hotel_Class (hotel_id, class_name, class_rent) VALUES (%s,%s,%s)",
                           (hid, cname, crent))
                messagebox.showinfo("OK", "Class added")
            except Exception as e:
                messagebox.showerror("Err", str(e))

class ClassDialog:
    def __init__(self, parent, title="Add Class"):
        top = tk.Toplevel(parent)
        top.title(title)
        ttk.Label(top, text="Class Name:").grid(row=0, column=0, sticky='e', padx=6, pady=6)
        ttk.Label(top, text="Rent:").grid(row=1, column=0, sticky='e', padx=6, pady=6)
        self.e_cname = tk.StringVar()
        self.e_crent = tk.StringVar(value="0.0")
        ttk.Entry(top, textvariable=self.e_cname, width=40).grid(row=0, column=1, padx=6, pady=6)
        ttk.Entry(top, textvariable=self.e_crent, width=40).grid(row=1, column=1, padx=6, pady=6)
        ttk.Button(top, text="Add", command=self.on_add).grid(row=2, column=0, columnspan=2, pady=8)
        self.top = top
        self.result = None

    def on_add(self):
        try:
            crent = float(self.e_crent.get())
        except:
            crent = 0.0
        self.result = (self.e_cname.get(), crent)
        self.top.destroy()
