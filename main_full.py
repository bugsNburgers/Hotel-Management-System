# main_full.py
"""
HMS Full GUI (single-file)
Requirements:
 - Python 3.8+
 - pip install mysql-connector-python ttkbootstrap

How to run:
 1) Ensure schema.sql and seed.sql have been executed in MySQL.
 2) Set environment variables or edit DB defaults below.
 3) python main_full.py
"""

import os
import mysql.connector
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

# DB config: uses environment variables or defaults
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_USER = os.getenv('DB_USER', 'root')
DB_PASS = os.getenv('DB_PASS', '')
DB_NAME = os.getenv('DB_NAME', 'hms')

def get_conn():
    return mysql.connector.connect(
        host=DB_HOST, user=DB_USER, passwd=DB_PASS, database=DB_NAME, autocommit=False
    )

# ---------------------- Helpers ----------------------
def safe_execute_query(query, params=None, fetch=False):
    conn = get_conn()
    cur = conn.cursor()
    try:
        cur.execute(query, params or ())
        if fetch:
            res = cur.fetchall()
        else:
            res = None
        conn.commit()
        return res
    except Exception as e:
        conn.rollback()
        raise
    finally:
        cur.close()
        conn.close()

def call_proc_return_one(proc_call_sql, params):
    """
    Use CALL proc(...) style and expect the procedure to SELECT a single-column single-row result (result).
    Returns the scalar value.
    """
    conn = get_conn()
    cur = conn.cursor()
    try:
        cur.execute(proc_call_sql, params)
        row = cur.fetchone()
        conn.commit()
        if row:
            return row[0]
        return None
    except Exception as e:
        conn.rollback()
        raise
    finally:
        cur.close()
        conn.close()

# ---------------------- GUI ----------------------
class HMSApp:
    def __init__(self, root):
        self.root = root
        root.title("HMS - Login")
        root.geometry("360x220")
        self.build_login()

    def build_login(self):
        frm = tk.Frame(self.root, padx=10, pady=10)
        frm.pack(expand=True, fill='both')
        tk.Label(frm, text="Username").pack(pady=6)
        self.user_e = tk.Entry(frm); self.user_e.pack()
        tk.Label(frm, text="Password").pack(pady=6)
        self.pass_e = tk.Entry(frm, show="*"); self.pass_e.pack()
        tk.Button(frm, text="Login", command=self.do_login, width=15).pack(pady=12)

    def do_login(self):
        u = self.user_e.get().strip()
        p = self.pass_e.get().strip()
        if not u or not p:
            messagebox.showerror("Login", "Enter username & password")
            return
        # hash client-side same as seed: SHA2('password',256)
        import hashlib
        hashed = hashlib.sha256(p.encode()).hexdigest()
        try:
            res = safe_execute_query("SELECT login_id FROM login WHERE username=%s AND password_hash=%s",
                                     (u, hashed), fetch=True)
            if res and len(res) > 0:
                self.open_main_window()
            else:
                messagebox.showerror("Login", "Invalid credentials")
        except Exception as e:
            messagebox.showerror("DB Error", str(e))

    def open_main_window(self):
        self.root.destroy()
        main = tk.Tk()
        main.title("HMS - Main Menu")
        main.geometry("640x420")
        ttk.Button(main, text="Manage Rooms", command=lambda: RoomWindow(main)).pack(pady=8)
        ttk.Button(main, text="Manage Customers / Checkin", command=lambda: CustomerWindow(main)).pack(pady=8)
        ttk.Button(main, text="Booking & Payments", command=lambda: BookingWindow(main)).pack(pady=8)
        ttk.Button(main, text="Reports", command=lambda: ReportsWindow(main)).pack(pady=8)
        ttk.Button(main, text="Audit Logs", command=lambda: AuditWindow(main)).pack(pady=8)
        ttk.Button(main, text="Exit", command=main.destroy).pack(pady=8)
        main.mainloop()

# ---------------------- Rooms ----------------------
class RoomWindow:
    def __init__(self, master):
        self.win = tk.Toplevel(master); self.win.title("Rooms"); self.win.geometry("720x460")
        self.build()

    def build(self):
        f = tk.Frame(self.win, padx=8, pady=8); f.pack()
        tk.Label(f, text="Room No").grid(row=0,column=0); self.rno = tk.Entry(f); self.rno.grid(row=0,column=1)
        tk.Label(f, text="Type").grid(row=1,column=0); self.rtype = tk.Entry(f); self.rtype.grid(row=1,column=1)
        tk.Label(f, text="Price").grid(row=2,column=0); self.rprice = tk.Entry(f); self.rprice.grid(row=2,column=1)
        tk.Button(f, text="Add Room", command=self.add_room).grid(row=3,column=0, pady=6)
        tk.Button(f, text="Delete Selected", command=self.delete_room).grid(row=3,column=1, pady=6)
        tk.Button(f, text="Refresh", command=self.refresh).grid(row=3,column=2, pady=6)
        cols = ("rno","type","price","vacancy")
        self.tree = ttk.Treeview(self.win, columns=cols, show='headings', height=15)
        for c in cols:
            self.tree.heading(c, text=c); self.tree.column(c, width=160, anchor='center')
        self.tree.pack(padx=10, pady=10)
        self.refresh()

    def refresh(self):
        for i in self.tree.get_children(): self.tree.delete(i)
        data = safe_execute_query("SELECT rno,type,price,vacancy FROM room ORDER BY rno", fetch=True)
        for r in data:
            self.tree.insert('', 'end', values=r)

    def add_room(self):
        try:
            rn = int(self.rno.get().strip()); tp = self.rtype.get().strip(); pr = float(self.rprice.get().strip())
        except:
            messagebox.showerror("Input", "Invalid room number or price")
            return
        try:
            safe_execute_query("INSERT INTO room (rno,type,price) VALUES (%s,%s,%s)", (rn, tp, pr))
            messagebox.showinfo("Added","Room added")
            self.refresh()
        except Exception as e:
            messagebox.showerror("DB Error", str(e))

    def delete_room(self):
        sel = self.tree.selection()
        if not sel: messagebox.showerror("Select","Select a row"); return
        rno = self.tree.item(sel[0])['values'][0]
        if not messagebox.askyesno("Confirm","Delete room %s?"%rno): return
        try:
            safe_execute_query("DELETE FROM room WHERE rno=%s", (rno,))
            messagebox.showinfo("Deleted","Room deleted")
            self.refresh()
        except Exception as e:
            messagebox.showerror("DB Error", str(e))

# ---------------------- Customers (checkin / checkout) ----------------------
class CustomerWindow:
    def __init__(self, master):
        self.win = tk.Toplevel(master); self.win.title("Customers"); self.win.geometry("980x520")
        self.build()

    def build(self):
        f = tk.Frame(self.win, padx=8, pady=8); f.pack()
        tk.Label(f, text="Name").grid(row=0,column=0); self.name = tk.Entry(f); self.name.grid(row=0,column=1)
        tk.Label(f, text="Proof").grid(row=1,column=0); self.proof = tk.Entry(f); self.proof.grid(row=1,column=1)
        tk.Label(f, text="Checkin (YYYY-MM-DD)").grid(row=2,column=0); self.checkin = tk.Entry(f); self.checkin.grid(row=2,column=1)
        tk.Label(f, text="Checkout (YYYY-MM-DD)").grid(row=3,column=0); self.checkout = tk.Entry(f); self.checkout.grid(row=3,column=1)
        tk.Label(f, text="Room No").grid(row=4,column=0); self.room = tk.Entry(f); self.room.grid(row=4,column=1)
        tk.Button(f, text="Check In (proc)", command=self.checkin_proc).grid(row=5,column=0, pady=6)
        tk.Button(f, text="Check Out (update -> trigger)", command=self.checkout).grid(row=5,column=1, pady=6)
        tk.Button(f, text="Refresh", command=self.refresh).grid(row=5,column=2, pady=6)

        cols = ("cid","name","room","checkin","checkout","cost","status")
        self.tree = ttk.Treeview(self.win, columns=cols, show='headings', height=16)
        for c in cols:
            self.tree.heading(c, text=c); self.tree.column(c, anchor='center', width=130)
        self.tree.pack(padx=10, pady=10)
        self.refresh()

    def refresh(self):
        for i in self.tree.get_children(): self.tree.delete(i)
        data = safe_execute_query("SELECT cid,name,room,checkin,checkout,cost,status FROM customer ORDER BY cid DESC", fetch=True)
        for r in data:
            self.tree.insert('', 'end', values=r)

    def checkin_proc(self):
        p_name = self.name.get().strip(); p_proof = self.proof.get().strip()
        p_checkin = self.checkin.get().strip(); p_checkout = self.checkout.get().strip()
        p_rno = self.room.get().strip()
        if not all([p_name, p_proof, p_checkin, p_checkout, p_rno]):
            messagebox.showerror("Input","All fields required")
            return
        try:
            # CALL stored proc proc_add_customer(...) which SELECTs result at end
            sql = "CALL proc_add_customer(%s,%s,%s,%s,%s)"
            out = call_proc_return_one(sql, (p_name, p_proof, p_checkin, p_checkout, int(p_rno)))
            # out codes: >0 => new cid, -1 room not found, -2 occupied, -3 invalid dates
            if out is None:
                messagebox.showerror("Proc", "No result from procedure")
            elif out > 0:
                messagebox.showinfo("Success", f"Checked in CID={out}")
                self.refresh()
            else:
                if out == -1:
                    messagebox.showerror("Error", "Room not found")
                elif out == -2:
                    messagebox.showerror("Error", "Room occupied")
                elif out == -3:
                    messagebox.showerror("Error", "Invalid dates")
                else:
                    messagebox.showerror("Error", f"Unknown error code {out}")
        except Exception as e:
            messagebox.showerror("DB Error", str(e))

    def checkout(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showerror("Select", "Select a customer")
            return
        cid = self.tree.item(sel[0])['values'][0]
        if not messagebox.askyesno("Confirm", f"Checkout CID={cid}?"):
            return
        try:
            safe_execute_query("UPDATE customer SET status='Checked Out' WHERE cid=%s", (cid,))
            messagebox.showinfo("Checked out", "Customer checked out; room vacancy updated by trigger.")
            self.refresh()
        except Exception as e:
            messagebox.showerror("DB Error", str(e))

# ---------------------- Booking & Payment ----------------------
class BookingWindow:
    def __init__(self, master):
        self.win = tk.Toplevel(master); self.win.title("Booking & Payment"); self.win.geometry("980x520")
        self.build()

    def build(self):
        f = tk.Frame(self.win, padx=8, pady=8); f.pack()
        tk.Label(f, text="Customer ID").grid(row=0,column=0); self.cust = tk.Entry(f); self.cust.grid(row=0,column=1)
        tk.Label(f, text="Hotel ID").grid(row=1,column=0); self.hotel = tk.Entry(f); self.hotel.grid(row=1,column=1)
        tk.Label(f, text="Booking Type").grid(row=2,column=0); self.btype = tk.Entry(f); self.btype.grid(row=2,column=1)
        tk.Label(f, text="Payment Amount").grid(row=3,column=0); self.amt = tk.Entry(f); self.amt.grid(row=3,column=1)
        tk.Button(f, text="Create Booking + Payment (proc)", command=self.create_booking).grid(row=4,column=0)
        tk.Button(f, text="Refresh", command=self.refresh).grid(row=4,column=1)

        cols = ("book_id","cust_id","hotel_id","book_date","paid_amt")
        self.tree = ttk.Treeview(self.win, columns=cols, show='headings', height=16)
        for c in cols:
            self.tree.heading(c, text=c); self.tree.column(c, width=150, anchor='center')
        self.tree.pack(padx=10, pady=10)
        self.refresh()

    def refresh(self):
        for i in self.tree.get_children(): self.tree.delete(i)
        sql = """
            SELECT b.book_id, b.cust_id, b.hotel_id, b.book_date,
                   COALESCE((SELECT SUM(pay_amt) FROM payment p WHERE p.book_id = b.book_id),0) AS paid_amt
            FROM booking b ORDER BY b.book_id DESC
        """
        data = safe_execute_query(sql, fetch=True)
        for r in data: self.tree.insert('', 'end', values=r)

    def create_booking(self):
        p_cust = self.cust.get().strip(); p_hotel = self.hotel.get().strip()
        p_type = self.btype.get().strip(); p_amt = self.amt.get().strip()
        if not p_cust or not p_hotel or not p_amt:
            messagebox.showerror("Input", "Customer, Hotel, and Amount required")
            return
        try:
            sql = "CALL proc_create_booking_with_payment(%s,%s,%s,%s,%s)"
            out = call_proc_return_one(sql, (int(p_cust), int(p_hotel), p_type, "", float(p_amt)))
            if out and out > 0:
                messagebox.showinfo("Created", f"Booking created: BOOKID={out}")
                self.refresh()
            else:
                messagebox.showerror("Error", f"Failed to create booking: code {out}")
        except Exception as e:
            messagebox.showerror("DB Error", str(e))

# ---------------------- Reports ----------------------
class ReportsWindow:
    def __init__(self, master):
        self.win = tk.Toplevel(master); self.win.title("Reports"); self.win.geometry("700x400")
        self.build()

    def build(self):
        tk.Button(self.win, text="Occupancy now", command=self.occupancy).pack(pady=8)
        tk.Button(self.win, text="Revenue by Month (last 12)", command=self.revenue_by_month).pack(pady=8)

    def occupancy(self):
        try:
            data = safe_execute_query("""
                SELECT SUM(CASE WHEN vacancy='Occupied' THEN 1 ELSE 0 END) AS occupied,
                       COUNT(*) AS total,
                       ROUND(100 * SUM(CASE WHEN vacancy='Occupied' THEN 1 ELSE 0 END) / COUNT(*),2) AS pct
                FROM room
            """, fetch=True)
            if data:
                occupied, total, pct = data[0]
                messagebox.showinfo("Occupancy", f"Occupied: {occupied}\nTotal: {total}\nOccupancy %: {pct}")
        except Exception as e:
            messagebox.showerror("DB Error", str(e))

    def revenue_by_month(self):
        try:
            rows = safe_execute_query("""
                SELECT YEAR(pay_date) yr, MONTH(pay_date) mon, SUM(pay_amt) total
                FROM payment
                GROUP BY YEAR(pay_date), MONTH(pay_date)
                ORDER BY yr DESC, mon DESC LIMIT 12
            """, fetch=True)
            top = tk.Toplevel(self.win); top.title("Revenue by Month")
            cols = ("yr","mon","total")
            tree = ttk.Treeview(top, columns=cols, show='headings')
            for c in cols: tree.heading(c, text=c)
            tree.pack(fill='both', expand=True)
            for r in rows: tree.insert('', 'end', values=r)
        except Exception as e:
            messagebox.showerror("DB Error", str(e))

# ---------------------- Audit ----------------------
class AuditWindow:
    def __init__(self, master):
        self.win = tk.Toplevel(master); self.win.title("Audit Logs"); self.win.geometry("800x400")
        self.build()

    def build(self):
        cols = ("log_id","event_type","event_desc","created_at")
        self.tree = ttk.Treeview(self.win, columns=cols, show='headings')
        for c in cols:
            self.tree.heading(c, text=c); self.tree.column(c, width=180, anchor='center')
        self.tree.pack(fill='both', expand=True)
        self.refresh()

    def refresh(self):
        for i in self.tree.get_children(): self.tree.delete(i)
        rows = safe_execute_query("SELECT log_id,event_type,event_desc,created_at FROM audit_logs ORDER BY log_id DESC LIMIT 200", fetch=True)
        for r in rows: self.tree.insert('', 'end', values=r)

# ---------------------- Run App ----------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = HMSApp(root)
    root.mainloop()
