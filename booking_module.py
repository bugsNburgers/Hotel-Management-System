# booking_module.py
import tkinter as tk
from tkinter import ttk, messagebox
from database import Database
from datetime import datetime

db = Database()

class BookingFrame(ttk.Frame):
    def __init__(self, parent, customer_id=None, manager_view=False, manager_id=None):
        super().__init__(parent, padding=10)
        self.customer_id = customer_id
        self.manager_view = manager_view
        self.manager_id = manager_id

        topf = ttk.Frame(self); topf.pack(fill='x', pady=6)
        ttk.Button(topf, text="🔄 Refresh", command=self.refresh).pack(side='left')

        # booking list
        cols = ('BookID','Cust','Hotel','Date','Type')
        self.tree = ttk.Treeview(self, columns=cols, show='headings', height=12)
        for c in cols:
            self.tree.heading(c, text=c)
            self.tree.column(c, width=140)
        self.tree.pack(fill='both', expand=True, pady=6)

        # booking form
        form = ttk.LabelFrame(self, text="Make Booking")
        form.pack(fill='x', pady=6)
        ttk.Label(form, text="Hotel:").grid(row=0,column=0,padx=6,pady=4, sticky='e')
        ttk.Label(form, text="Class:").grid(row=1,column=0,padx=6,pady=4, sticky='e')
        ttk.Label(form, text="Amount:").grid(row=2,column=0,padx=6,pady=4, sticky='e')

        self.e_hotel = tk.StringVar()
        self.e_class = tk.StringVar()
        self.e_amt = tk.StringVar(value="0.0")

        # Hotel dropdown
        hotels = db.fetch("SELECT hotel_id, hotel_name FROM Hotel")
        self.hotel_combo = ttk.Combobox(form, textvariable=self.e_hotel, values=[f"{h[0]} - {h[1]}" for h in hotels], state='readonly')
        self.hotel_combo.grid(row=0,column=1,padx=6,pady=4)
        self.hotel_combo.bind("<<ComboboxSelected>>", self.on_hotel_select)

        # Class dropdown (populated on hotel select)
        self.class_combo = ttk.Combobox(form, textvariable=self.e_class, state='readonly')
        self.class_combo.grid(row=1,column=1,padx=6,pady=4)
        self.class_combo.bind("<<ComboboxSelected>>", self.on_class_select)

        ttk.Entry(form, textvariable=self.e_amt, state='readonly').grid(row=2,column=1,padx=6,pady=4)
        ttk.Button(form, text="📅 Book & Pay", command=self.make_booking).grid(row=3, column=0, columnspan=2, pady=8)

        self.refresh()

    def on_hotel_select(self, event):
        hotel_str = self.e_hotel.get()
        if hotel_str:
            hotel_id = int(hotel_str.split(' - ')[0])
            classes = db.fetch("SELECT class_id, class_name, class_rent FROM Hotel_Class WHERE hotel_id=%s", (hotel_id,))
            self.class_combo['values'] = [f"{c[0]} - {c[1]} ({c[2]})" for c in classes]
            self.class_combo.set('')
            self.e_amt.set('0.0')

    def on_class_select(self, event):
        class_str = self.e_class.get()
        if class_str:
            rent = float(class_str.split('(')[1].strip(')'))
            self.e_amt.set(str(rent))

    def refresh(self):
        if self.manager_view and self.manager_id:
            # show bookings for hotels managed by manager
            q = ("SELECT b.book_id, c.cust_name, h.hotel_name, b.book_date, b.book_type "
                 "FROM Booking b JOIN Customer c ON b.cust_id=c.cust_id JOIN Hotel h ON b.hotel_id=h.hotel_id "
                 "WHERE h.user_id=%s")
            rows = db.fetch(q, (self.manager_id,))
        elif self.customer_id:
            # show bookings for this customer
            q = ("SELECT b.book_id, c.cust_name, h.hotel_name, b.book_date, b.book_type "
                 "FROM Booking b JOIN Customer c ON b.cust_id=c.cust_id JOIN Hotel h ON b.hotel_id=h.hotel_id "
                 "WHERE b.cust_id=%s")
            rows = db.fetch(q, (self.customer_id,))
        else:
            q = ("SELECT b.book_id, c.cust_name, h.hotel_name, b.book_date, b.book_type "
                 "FROM Booking b JOIN Customer c ON b.cust_id=c.cust_id JOIN Hotel h ON b.hotel_id=h.hotel_id")
            rows = db.fetch(q)
        for i in self.tree.get_children():
            self.tree.delete(i)
        for r in rows:
            self.tree.insert('', 'end', values=r)

    def make_booking(self):
        try:
            if not self.customer_id:
                messagebox.showerror("Error", "Customer ID not set")
                return
            hotel_str = self.e_hotel.get()
            class_str = self.e_class.get()
            if not hotel_str or not class_str:
                messagebox.showerror("Error", "Select hotel and class")
                return
            hotel_id = int(hotel_str.split(' - ')[0])
            class_id = int(class_str.split(' - ')[0])
            book_date = datetime.now().strftime('%Y-%m-%d')
            book_type = "standard"  # or from class name
            book_desc = f"Booked class {class_str} by cust {self.customer_id}"
            pay_amt = float(self.e_amt.get())

            results = db.callproc('sp_make_booking', (self.customer_id, hotel_id, book_date, book_type, book_desc, pay_amt))
            messagebox.showinfo("Booked", f"Booking and payment done! Booking ID: {results[0][0][0] if results else 'N/A'}")
            self.refresh()
        except Exception as e:
            messagebox.showerror("Booking error", str(e))
