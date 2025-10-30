# payment_module.py
import tkinter as tk
from tkinter import ttk, messagebox
from database import Database
from datetime import datetime

db = Database()

class PaymentFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent, padding=10)
        btnf = ttk.Frame(self)
        btnf.pack(fill='x', pady=6)
        ttk.Button(btnf, text="🔄 Refresh", command=self.refresh).pack(side='left')
        ttk.Button(btnf, text="💳 Add Payment", command=self.add_payment).pack(side='left', padx=6)

        cols = ('PayID','BookID','Date','Amount','Desc')
        self.tree = ttk.Treeview(self, columns=cols, show='headings', height=14)
        for c in cols:
            self.tree.heading(c, text=c)
            self.tree.column(c, width=140)
        self.tree.pack(fill='both', expand=True)
        self.refresh()

    def refresh(self):
        rows = db.fetch("SELECT pay_id, book_id, pay_date, pay_amt, pay_desc FROM Payment")
        for i in self.tree.get_children():
            self.tree.delete(i)
        for r in rows:
            self.tree.insert('', 'end', values=r)

    def add_payment(self):
        d = AddPaymentDialog(self)
        self.wait_window(d.top)
        if d.result:
            book_id, amt, desc = d.result
            db.execute("INSERT INTO Payment (book_id, pay_date, pay_amt, pay_desc) VALUES (%s, %s, %s, %s)",
                       (book_id, datetime.now().strftime('%Y-%m-%d'), amt, desc))
            messagebox.showinfo("OK", "Payment recorded")
            self.refresh()

class AddPaymentDialog:
    def __init__(self, parent):
        top = tk.Toplevel(parent)
        top.title("Add Payment")
        ttk.Label(top, text="Booking ID").grid(row=0, column=0, padx=6, pady=6)
        ttk.Label(top, text="Amount").grid(row=1, column=0, padx=6, pady=6)
        ttk.Label(top, text="Desc").grid(row=2, column=0, padx=6, pady=6)
        self.e_bid = tk.StringVar(); self.e_amt = tk.StringVar(); self.e_desc = tk.StringVar()
        ttk.Entry(top, textvariable=self.e_bid).grid(row=0, column=1)
        ttk.Entry(top, textvariable=self.e_amt).grid(row=1, column=1)
        ttk.Entry(top, textvariable=self.e_desc).grid(row=2, column=1)
        ttk.Button(top, text="Add", command=self.on_add).grid(row=3, column=0, columnspan=2, pady=8)
        self.top = top; self.result = None
    def on_add(self):
        try:
            amt = float(self.e_amt.get())
        except: amt = 0.0
        self.result = (int(self.e_bid.get()), amt, self.e_desc.get())
        self.top.destroy()
