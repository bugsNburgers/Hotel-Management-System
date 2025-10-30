# dashboard_admin.py
import tkinter as tk
from tkinter import ttk
from hotel_module import HotelFrame
from user_module import UserFrame
from booking_module import BookingFrame
from payment_module import PaymentFrame
from customer_module import CustomerFrame

class AdminDashboard:
    def __init__(self, root, user_id):
        self.root = root
        self.user_id = user_id
        root.title("Admin Dashboard")
        root.geometry("1000x700")
        root.configure(bg='#e8f4f8')
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TNotebook', background='#e8f4f8')
        style.configure('TNotebook.Tab', font=('Segoe UI', 11, 'bold'), padding=[10, 5])

        nb = ttk.Notebook(root, style='TNotebook')
        nb.pack(fill='both', expand=True, padx=10, pady=10)

        # Users
        user_tab = UserFrame(nb)
        nb.add(user_tab, text="Users / Roles")

        # Hotels
        hotel_tab = HotelFrame(nb)
        nb.add(hotel_tab, text="Hotels")

        # Bookings (view / manual manage)
        booking_tab = BookingFrame(nb)
        nb.add(booking_tab, text="Bookings")

        # Payments
        pay_tab = PaymentFrame(nb)
        nb.add(pay_tab, text="Payments")

        # Customers
        cust_tab = CustomerFrame(nb)
        nb.add(cust_tab, text="Customers")
