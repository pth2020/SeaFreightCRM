from db.db_manager import DatabaseManager
from tkinter import messagebox
import datetime
import tkinter as tk
from tkinter import ttk

class DashboardFrame(tk.Frame):
    
    def __init__(self, master, dashboard):  # master = parent frame, dashboard = logic helper
        super().__init__(master)
        self.dashboard = dashboard
        self.create_dashboard()
        
                
    def create_dashboard(self):
        
        #self.clear_content() 
        
        # ===== Widgets in Dashboard ======
        
        self.lbl_customers=tk.Label(self, text=self.dashboard.get_total_customers(), bd=20, relief=tk.RAISED, bg="#33bbf9", fg="white",
                                font=("Arial",20, "bold"))
        self.lbl_customers.place(x=100, y=50, height=150, width=460)
        
        self.lbl_destinations=tk.Label(self, text=self.dashboard.get_total_destinations(), bd=20, relief=tk.RAISED, bg="#75FA8D", fg="white",
                                font=("Arial",20, "bold"))
        self.lbl_destinations.place(x=800, y=50, height=150, width=460)
        
        self.lbl_total_items_to_ship=tk.Label(self, text=self.dashboard.get_total_items_to_ship(), bd=20, relief=tk.RAISED, bg="#732BF5", fg="white",
                                font=("Arial",20, "bold"))
        self.lbl_total_items_to_ship.place(x=450, y=300, height=150, width=460)
        
        self.lbl_todays_total_transactions=tk.Label(self, text=self.dashboard.get_todays_total_transactions(), bd=20, relief=tk.RAISED, bg="#6E6D25", fg="white",
                                font=("Arial",20, "bold"))
        self.lbl_todays_total_transactions.place(x=100, y=570, height=150, width=460)
        
        self.lbl_this_weeks_total_transactions=tk.Label(self, text=self.dashboard.get_this_weeks_total_transactions(), bd=20, relief=tk.RAISED, bg="#BFBD14", fg="white",
                                font=("Arial",20, "bold"))
        self.lbl_this_weeks_total_transactions.place(x=800, y=570, height=150, width=460)  

class Dashboard:
    
    def __init__(self, factory):
        self.factory = factory
    
    def show_dashboard(self):
        self.factory.clear_content()
        
    def get_total_customers(self):        
        
        try:
            with DatabaseManager.with_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT COUNT(DISTINCT full_name || mobile || email)
                    FROM shipments               
                """)
                result = cursor.fetchone()
                total_customers = result[0] if result else 0                
                return f"Total Customers\n{total_customers}"
        except Exception as e:
            messagebox.showerror("Database Error", f"Failed to count customers: {e}")
            
    def get_total_destinations(self):
        try:
            with DatabaseManager.with_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT COUNT(country)
                    FROM country_price
                """)
                result = cursor.fetchone()
                total_destinations = result[0] if result else 0
                return f"Total Destinations\n{total_destinations}"
        except Exception as e:
            messagebox.showerror("Database Error", f"Failed to count destinations: {e}")
                    
    def get_total_items_to_ship(self):
        try:
            with DatabaseManager.with_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT COUNT(status_of_goods)
                    FROM shipments
                    WHERE status_of_goods=?                
                """, ("Collected",))
                result = cursor.fetchone()
                total_items_to_ship = result[0] if result else 0
                return f"Total Items To Be Shipped\n{total_items_to_ship}"
        except Exception as e:
            messagebox.showerror("Database Error", f"Failed to count destinations: {e}")    
            
    def get_todays_total_transactions(self):
        todays_date = datetime.datetime.now().strftime("%YYYY-%mm-%dd")    #strftime("%dd-%mm-%YYYY")  # Format to match date in DB
        try:
            with DatabaseManager.with_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT COUNT(*)
                    FROM shipments
                    WHERE DATE(created_at) = ?
                """, (todays_date,))
                result = cursor.fetchone()
                total_transactions = result[0] if result else 0
                return f"Today's Transactions\n{total_transactions}"
        except Exception as e:
            messagebox.showerror("Database Error", f"Failed to count today's transactions: {e}")
            
    def get_this_weeks_total_transactions(self):
        from datetime import timedelta # timedelta a class in  Python’s datetime module 
                                    # that represents a duration, i.e., the difference between two dates or times
                                    
        today = datetime.datetime.now()
        start_of_week = today - timedelta(days=today.weekday())  # Monday
        start_date = start_of_week.strftime("%dd-%mm-%YYYY")
        end_date = today.strftime("%dd-%mm-%YYYY")

        try:
            with DatabaseManager.with_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT COUNT(*)
                    FROM shipments
                    WHERE DATE(created_at) BETWEEN ? AND ?
                """, (start_date, end_date))
                result = cursor.fetchone()
                total_transactions = result[0] if result else 0

                return f"This Week's Transactions\n{total_transactions}"
        except Exception as e:
            messagebox.showerror("Database Error", f"Failed to count this week's transactions: {e}")        