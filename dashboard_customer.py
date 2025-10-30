# dashboard_customer.py
import tkinter as tk
from tkinter import ttk
from hotel_module import HotelFrame
from booking_module import BookingFrame

class CustomerDashboard:
    def __init__(self, root, user_id):
        self.root = root
        self.user_id = user_id
        root.title("Customer Dashboard")
        root.geometry("980x650")
        root.configure(bg='#f0fff0')
        style = ttk.Style(); style.theme_use('clam')
        style.configure('TNotebook', background='#f0fff0')
        style.configure('TNotebook.Tab', font=('Segoe UI', 11, 'bold'), padding=[10, 5])

        nb = ttk.Notebook(root, style='TNotebook')
        nb.pack(fill='both', expand=True, padx=8, pady=8)

        hotels_tab = HotelFrame(nb, allow_book=True)
        nb.add(hotels_tab, text="Browse Hotels")

        book_tab = BookingFrame(nb, customer_id=self.user_id)
        nb.add(book_tab, text="My Bookings / Make Booking")
