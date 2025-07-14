from db.db_manager import DatabaseManager
from tkinter import messagebox
import tkinter as tk
from tkinter import ttk
import sqlite3
import datetime

class ReportFrame(tk.Frame):
    def __init__(self, master, factory):
        super().__init__(master)
        self.factory = factory
        self.report_logic = self.factory.report_logic
        self.tree_shipping_rates = None  # declare here
    
        
    def create_report(self):
        """    
            Report frame has four sections: 
            1) Shipping Rates by Country
            2) Top 5 Countries by Transaction Volume
            3) Monthly Revenue 
            4) Pending vs Completed Shipments
        """
        
        #self.clear_content()
        
        # Initialising report_frame 
        self.report_frame = tk.Frame(self.master, relief=tk.RIDGE, bd=10, bg="#33bbf9")
        self.report_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Setting title
        title = tk.Label(self.report_frame, text="Report", font=("Arial", 18, "bold"), bg="#33bbf9", fg="white")
        title.pack(pady=10)
        
        # container inside report_frame that has four items        
        grid_container = tk.Frame(self.report_frame, bg="#33bbf9")
        grid_container.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Configuring grid layout inside grid_container
        for row in range(2): # iterating through row 0  and 1
            # If the parent window (or container) is resized, each of these rows should expand equally.
            # If one row had weight=1 and another weight=2, the second would stretch twice as much vertically.
            grid_container.grid_rowconfigure(row, weight=1) # weight=1 means it gets equal "stretching power".
        for col in range(2): # same applies as the rows
            grid_container.grid_columnconfigure(col, weight=1)
        # Each cell in the grid grows proportionally.

        # labels for the four sections of the grid_container
        labels = ["Shipping Rates by Country", "Top 5 Countries by Transaction Volume", "Monthly Revenue", "Pending vs Completed Shipments"]
        
        # A clever way to place 4 items into a 2x2 grid layout.
        for i in range(4):  #  looping over i from 0 to 3 (range(4))
            row = i // 2  # row = i // 2 → integer division (floor division)
            col = i % 2   # col = i % 2 → remainder (modulo)
            # frames for the four labels
            section = tk.Frame(grid_container, relief=tk.RIDGE, bd=5, bg="#f0f0f0")
            section.grid(row=row, column=col, sticky="nsew", padx=10, pady=10)
            # setting the labels of the four sections
            tk.Label(section, text=labels[i], font=("Arial", 14, "bold"), bg="#f0f0f0").pack(pady=(10, 5))
            
            # Shipping rates by country
            if i == 0:
                # Frame inside section to hold Treeview + Scrollbar
                shipping_rates_frame = tk.Frame(section, bg="#ffffff", bd=2, relief="ridge")
                shipping_rates_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))

                # === Treeview Styling ===
                style = ttk.Style() # Creates a new Style object to modify widget styles (like Treeview, Buttons, etc.).
                style.theme_use("default") # Applies the "default" theme as the base.
                                            # Ensures a known starting point before applying customizations.
                # customizes the main Treeview body (rows):
                style.configure("Treeview", background="#ffffff", foreground="black", rowheight=20, fieldbackground="#ffffff")
                # customizes the header row (column titles):
                style.configure("Treeview.Heading", background="#4a6fa5", foreground="white", font=("Arial", 14, "bold"))
            
                # Create Scrollbar
                tree_scroll = tk.Scrollbar(shipping_rates_frame, orient="vertical")
                tree_scroll.pack(side="right", fill="y")

                # Limit Treeview height to e.g. 5 rows
                # Creates a Treeview widget — a table-like structure.
                self.tree_shipping_rates = ttk.Treeview(
                    shipping_rates_frame,  # parent frame where the Treeview will appear.
                    columns=("Country", "Price"),
                    show="headings", # tells Treeview to show only the column headers, 
                                        # not the built-in tree (used for hierarchical data).
                    yscrollcommand=tree_scroll.set, # Connects the Treeview to a vertical scrollbar (tree_scroll). 
                                                        # This allows scrolling when more rows are added.
                    height=5  # << LIMIT Treeview rows - Limits the visible rows to 5 — users will need to scroll to see more.
                )
                # configures the header for the column identified as "Country".
                self.tree_shipping_rates.heading("Country", text="Country")
                # configures the header for the column identified as "Price".
                self.tree_shipping_rates.heading("Price", text="Price (£/Kg)")
                # adds the Treeview to the GUI layout using the .pack() geometry manager:
                self.tree_shipping_rates.pack(side="left", fill="both", expand=True)
                # to connect a vertical scrollbar (tree_scroll) to a ttk.Treeview widget (tree), 
                # allowing the Treeview to scroll vertically when needed.
                tree_scroll.config(command=self.tree_shipping_rates.yview) # tree.yview is a method of the Treeview that handles vertical scrolling.

                # Row color tags 
                # tree.tag_configure(...): Defines how rows with a specific tag should appear.
                self.tree_shipping_rates.tag_configure('oddrow', background='#f0f0ff')
                self.tree_shipping_rates.tag_configure('evenrow', background='#ffffff')
                
                self.report_logic.show_reports(i)
                
            elif i == 1:
                # Frame inside section to hold Treeview 
                top_five_countries_frame = tk.Frame(section, bg="#ffffff", bd=2, relief="ridge")
                top_five_countries_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))
                
                # === Treeview Styling ===
                style = ttk.Style()
                style.theme_use("default")
                style.configure("Treeview", background="#ffffff", foreground="black", rowheight=30, fieldbackground="#ffffff")
                style.configure("Treeview.Heading", background="#4a6fa5", foreground="white", font=("Arial", 14, "bold"))
                
                self.tree_top_countries = ttk.Treeview(
                    top_five_countries_frame,
                    columns=("Rank", "Country", "TotalWeight"),  
                    show="headings",
                    yscrollcommand=tree_scroll.set,
                    height=5
                )
                
                self.tree_top_countries.heading("Rank", text="Ranking")
                self.tree_top_countries.heading("Country", text="Country")
                self.tree_top_countries.heading("TotalWeight", text="Total Weight (kg)")
                self.tree_top_countries.pack(side="left", fill="both", expand=True)  
                
                self.factory.report_logic.show_reports(i)
                
            elif i == 2:
                revenue_frame = tk.Frame(section, bg="#ffffff", bd=2, relief="ridge")
                revenue_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))

                # Table setup
                self.revenue_table = ttk.Treeview(revenue_frame, columns=("Data", "Value"), show="headings", height=4)
                self.revenue_table.heading("Data", text="Data")
                self.revenue_table.heading("Value", text="Value")
                self.revenue_table.column("Data", width=200, anchor="w")
                self.revenue_table.column("Value", anchor="center")
                self.revenue_table.pack(fill="both", expand=True)
                
                self.factory.report_logic.show_reports(i)
                
            elif i == 3:
                shippment_status_frame = tk.Frame(section, bg="#ffffff", bd=2, relief="ridge")
                shippment_status_frame.pack(fill="both", expand=True, padx=10 , pady=0)
                
                # Table setup
                self.shippment_status_table = ttk.Treeview(
                    shippment_status_frame,
                    columns=("collected", "shipped", "arrived"),
                    show="headings",
                    height=6  # Increased height to show summary rows
                )
                self.shippment_status_table.heading("collected", text="Collected")
                self.shippment_status_table.heading("shipped", text="Shipped (In Transit)")
                self.shippment_status_table.heading("arrived", text="Arrived")
                self.shippment_status_table.pack(fill="both", expand=True)
                
                self.shippment_status_table.tag_configure("highlight", background="#f0f0ff")  # light yellow
                
                # Center align the column values
                self.shippment_status_table.column("collected", anchor="center")
                self.shippment_status_table.column("shipped", anchor="center")
                self.shippment_status_table.column("arrived", anchor="center")
                
                self.factory.report_logic.show_reports(i)

class Report:
    
    def __init__(self, factory):
        self.factory = factory
        self.report_frame = None  # Will be set later

    def set_report_frame(self, report_frame):
        self.report_frame = report_frame

    def show_reports(self, section):
        """ Use database to generate report for the four sections """
        
        # Shipping rates by country
        if section == 0:
            self.display_country_shipping_rates()
        
        # Top 5 Countries by Transaction Volume       
        elif section == 1:
            self.display_top_5_shipping_countries()
        
        # Monthly Revenue 
        elif section == 2:
            self.display_monthly_revenue()            
                    
        # Pending vs Completed Shipments
        elif section == 3:
            self.display_shipment_status_overview()            
            
                
    def display_country_shipping_rates(self):
        # Load data
            try:
                with DatabaseManager.with_connection() as conn:
                    cursor = conn.cursor()
                    cursor.execute("SELECT country, price FROM country_price")
                    rows = cursor.fetchall()                        
                    # rows is a list of data rows (e.g., from a database query).
                    # enumerate(rows) gives you both - index(position of rows)
                    # and row (the actual data)                    
                    for index, row in enumerate(rows):  
                        tag = 'evenrow' if index % 2 == 0 else 'oddrow' # oddrow and evenrow defined above
                        self.report_frame.tree_shipping_rates.insert("", "end", values=row, tags=(tag,)) # This inserts the row into the ttk.Treeview.
                        # "": Insert at the root level (not as a child of another item).
                        # "end": Add to the end of the list.
                        # values=row: Sets the cell values (e.g., "USA", 5.99).
                        # tags=(tag,): Applies the corresponding tag ("evenrow" or "oddrow"), which determines the background color.
            except DatabaseManager.with_connection().Error as e:
                messagebox.showerror("Database Error", f"Could not load reports: {e}")       
                
    def display_top_5_shipping_countries(self):
        try:
            with DatabaseManager.with_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT country, SUM(total_weight) AS total_weight
                    FROM shipments
                    JOIN country_price ON country_price.id = shipments.country_price_id
                    GROUP BY country
                    ORDER BY total_weight DESC
                """)
                rows = cursor.fetchall()
                    
                for index, row in enumerate(rows):
                    tag = 'evenrow' if index % 2 == 0 else 'oddrow'
                    self.report_frame.tree_top_countries.insert("", "end", values=(index + 1, row[0], f"{row[1]:,.2f} kg"), tags=(tag,))
        except DatabaseManager.with_connection().Error as e:
            messagebox.showerror("Database Error", f"Could not load reports: {e}")
        
    def display_monthly_revenue(self):
        # Get current month
        from datetime import datetime
        now = datetime.now()
        current_month = now.strftime("%B %Y")
            
        try:
            with DatabaseManager.with_connection() as conn:
                cursor = conn.cursor()
                # Fetch monthly total revenue and total shipments
                cursor.execute("""
                    SELECT SUM(total_cost) AS total_revenue, COUNT(*) AS total_transactions
                    FROM shipments
                    WHERE strftime('%Y-%m', created_at) = strftime('%Y-%m', 'now')
                """)
                                        
                revenue_data = cursor.fetchone()
                total_revenue = revenue_data[0] or 0
                total_shipments = revenue_data[1] or 0
                avg_revenue = total_revenue / total_shipments if total_shipments else 0

                # Insert rows
                self.report_frame.revenue_table.insert("", "end", values=("Month", current_month))
                self.report_frame.revenue_table.insert("", "end", values=("Total Revenue (£)", f"{total_revenue:,.2f}"))
                self.report_frame.revenue_table.insert("", "end", values=("Total Shipments", total_shipments))
                self.report_frame.revenue_table.insert("", "end", values=("Average Revenue per Shipment (£)", f"{avg_revenue:,.2f}"))

        except DatabaseManager.with_connection().Error as e:
            messagebox.showerror("Database Error", f"Could not load monthly revenue: {e}")   
            
    def display_shipment_status_overview(self):
        # Define counts and flag
        counts = {"Collected": 0, "Shipped(In Transit)": 0, "Arrived": 0}
        data_loaded = False

        try:
            with DatabaseManager.with_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT status_of_goods, COUNT(id) as Numbers                    
                    FROM shipments
                    GROUP BY status_of_goods
                """)
                # get all rows of data
                rows = cursor.fetchall()
                    
                # Normalize and map counts
                status_map = {
                        "collected": "Collected",
                        "shipped(in transit)": "Shipped(In Transit)",
                        "arrived": "Arrived"
                }

                for status, count in rows:
                    normalized = status.strip().lower()
                    if normalized in status_map:
                        mapped_status = status_map[normalized]
                        counts[mapped_status] = count

                    # Insert main row
                    self.report_frame.shippment_status_table.insert("", "end", 
                    values=(counts["Collected"],counts["Shipped(In Transit)"],counts["Arrived"]), tags=("highlight",))
                    
                    data_loaded = True                        
                    self.report_frame.shippment_status_table.insert("", "end", values=("", "", ""))  # spacing above (optional)

        except DatabaseManager.with_connection().Error as e:
                messagebox.showerror("Database Error", f"Could not load shipment status: {e}")

                
        if data_loaded:
            total_shipments = counts["Collected"] + counts["Shipped(In Transit)"] + counts["Arrived"]

            def format_pct(value, total):
                    return f"{(value / total * 100):.1f}%" if total else "0%"

            # Insert summary rows
            self.report_frame.shippment_status_table.insert("", "end", values=("Total Shipments", "", total_shipments))
            self.report_frame.shippment_status_table.insert("", "end", values=("Collected %", "", format_pct(counts["Collected"], total_shipments)))
            self.report_frame.shippment_status_table.insert("", "end", values=("Shipped %", "", format_pct(counts["Shipped(In Transit)"], total_shipments)))
            self.report_frame.shippment_status_table.insert("", "end", values=("Arrived %", "", format_pct(counts["Arrived"], total_shipments)))