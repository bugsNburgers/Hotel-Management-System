# dashboard_manager.py
import tkinter as tk
from tkinter import ttk
from hotel_module import HotelFrame
from booking_module import BookingFrame

class ManagerDashboard:
    def __init__(self, root, user_id):
        self.root = root
        self.user_id = user_id
        root.title("Manager Dashboard")
        root.geometry("980x650")
        root.configure(bg='#fffacd')
        style = ttk.Style(); style.theme_use('clam')
        style.configure('TNotebook', background='#fffacd')
        style.configure('TNotebook.Tab', font=('Segoe UI', 11, 'bold'), padding=[10, 5])

        nb = ttk.Notebook(root, style='TNotebook')
        nb.pack(fill='both', expand=True, padx=8, pady=8)

        hotel_tab = HotelFrame(nb, manager_id=user_id)
        nb.add(hotel_tab, text="My Hotels")

        booking_tab = BookingFrame(nb, manager_view=True, manager_id=user_id)
        nb.add(booking_tab, text="Bookings for my hotels")
