# main.py
import tkinter as tk
from login_page import LoginPage

def main():
    root = tk.Tk()
    # small tweak to make root size sensible
    root.geometry("900x650")
    LoginPage(root)
    root.mainloop()

if __name__ == "__main__":
    main()
