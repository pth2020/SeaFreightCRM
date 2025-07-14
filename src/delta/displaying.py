from tkinter import *
from tkinter import messagebox
from db.db_manager import DatabaseManager

class Displaying:
    
    def __init__(self, factory):
        self.factory = factory
        
    def load_country_list(self):
        try:
            with DatabaseManager.with_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT country FROM country_price")
                countries = [row[0] for row in cursor.fetchall()]
                return countries
        except DatabaseManager.with_connection().Error as e:
            messagebox.showerror("Database Error", f"Failed to load countries: {e}")
            return []
        
    def get_selected_country_id(self, country):
        """ Retrieves country id and shipment rate (price) from country_price table """
        try:
            with DatabaseManager.with_connection() as conn: # with closes db connection automatically when job done
                cursor = conn.cursor()
                cursor.execute("SELECT id, price FROM country_price WHERE country =?", (country,))
                row = cursor.fetchone()

            if row: # if data returned
                return row[0], row[1]  # Return the first (id) and second (price) elements of the tuple
            else:
                messagebox.showerror("Database Error", "Country not found.")
                return None, None  # Return None for both if no data found
            
        except Exception as e:
            messagebox.showerror("Database Error", str(e))
            return None, None  # Return None for both if error occurs       
        
    
    def display_data(self):
        """ Display Treeview shipment-transaction data retrieved from database """
        try:
            # Connect to SQLite and fetch data from the db, if db doesn't exist SQLite creates it
            with DatabaseManager.with_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(""" Select id,transaction_id, created_at,full_name, mobile, email,type_of_goods,total_weight, 
                        date_shipped,total_cost, status_of_goods from shipments """)
                # This method fetches all the rows returned by the SQL query.
                # rows stores a list of tuples
                rows = cursor.fetchall()
                
                if len(rows) != 0:
                    # This deletes all the existing rows in the Treeview before adding the new ones. 
                    # It's done to ensure that the Treeview is cleared before inserting fresh data.
                    # This method (get_children()) returns all child items (rows) in the Treeview.
                    self.factory.global_table.delete(*self.factory.global_table.get_children()) 
                    for i in rows:
                        # This inserts a new row into the Treeview for each tuple i. 
                        # The values=i part passes the tuple as the row's values. 
                        # The empty string "" is the parent item (for top-level rows), 
                        # and END places the row at the end of the Treeview.
                        # (id, transaction_id, collected_date, full_name, mobile, email,goods_type, weight,shipped_date, estimated_cost, status))
                        self.factory.global_table.insert("", END, values=(i[0], i[1], i[2], i[3], i[4], 
                                                i[5], i[6], i[7], i[8], i[9], i[10]))
                    
                # save changes to the database
                conn.commit()              

            
            # Back button disabled again
            self.factory.btn_back.config(state=DISABLED)
            
            # Clear search entry
            self.factory.search_ent.delete(0, END)
            
        except Exception as e:
            messagebox.showerror("Database Error", str(e))   
            
        
    def get_cursor(self, event=""):
        from .receipt import Receipt
        
        # create an instance of Receipt
        receipt = Receipt(self.factory)   
        
        # Get the currently focused row in the Treeview (the clicked row)
        # Gets the ID of the currently selected (focused) row in your Treeview widget when a user clicks on a row.
        cursor_row = self.factory.global_table.focus()

        # Get the content of the clicked row - dictionary
        content = self.factory.global_table.item(cursor_row)

        # Retrieve the values of the clicked row
        # Extracts the tuple of values from the dictionary returned by .item(cursor_row) in a ttk.Treeview.
        row = content["values"]
        

        # Set the corresponding entries in DataFrameLeft with the selected row values
        # clear the contents of the Entry widget named fname_ent (which is for the First Name field) before inserting a new value.
        self.factory.fname_ent.delete(0, END)
        # insert a new value
        full_name = row[3]  # full name

        # Check if full name contains space, else use it as a single part
        name_parts = full_name.split()  # split() by default splits a string by whitespace (spaces, tabs, newlines).
        if len(name_parts) >= 2:
            self.factory.fname_ent.insert(0, name_parts[0])
            self.factory.lname_ent.delete(0, END)
            self.factory.lname_ent.insert(0, name_parts[1])
        else:
            self.factory.fname_ent.insert(0, full_name)
            self.factory.lname_ent.delete(0, END)

        self.factory.mobile_ent.delete(0, END) # END - position after the last character in the text field.
        self.factory.mobile_ent.insert(0, row[4])

        self.factory.email_ent.delete(0, END)
        self.factory.email_ent.insert(0, row[5])       

        self.factory.type_of_goods.set(row[6])  # Assuming the value is stored in column index 6 (type_of_goods)
        
        self.factory.total_weight_ent.delete(0, END)
        self.factory.total_weight_ent.insert(0, row[7])
        
        self.factory.estimated_cost = row[9]

        self.factory.status_of_goods.set(row[10])  # Assuming the status is in column index 9

        # Retrieve Billing Address and Destination Address based on the selected id
        # Shipment_id needed to retrieve billing and destination addresses from the database
        # because these two data are not displayed in the Treeview
        shipment_id = row[0]  # Assuming the ID is in the first column (index 0)

        try:
            # Connect to the database to fetch the Billing and Destination address
            with DatabaseManager.with_connection() as conn:
                cursor = conn.cursor()
                # Query to get the Billing and Destination address based on the shipment id
                # id=?: The ? is a placeholder for a parameterized query, which helps to avoid SQL injection attacks and 
                # allows you to safely pass data to the query.
                # (shipment_id,): This tuple contains the value for the id parameter in the query. The tuple is passed as 
                # the second argument to cursor.execute() to safely substitute the ? placeholder with the actual value of shipment_id.
                # The trailing comma is necessary to create a tuple in Python, even if it has only one item. So (shipment_id,) is a 
                # tuple containing the value of shipment_id.
                cursor.execute(
                    "SELECT sender_build_door_no, sender_street_road, sender_city_town, sender_postcode, "
                            "dest_receiver_title_fullname, dest_first_line_of_address, "
                            "dest_city_town, dest_mobile, transaction_id, created_at, country_price.country "
                            "FROM shipments, country_price WHERE shipments.id=? AND country_price.id == shipments.country_price_id", (shipment_id,))
                # After executing the query, the cursor.fetchone() method is used to retrieve the first row of the query result.
                # tuple containing the values from the selected columns
                # The result returned by fetchone() will be a tuple containing the values from the selected columns 
                # (in this case, billing_address and destination_address).
                address_data = cursor.fetchone()  # Fetch the result

                if address_data:
                    # address_data is a tuple with two values - assign to sender and destination data
                    sender_build_door_no, sender_street_road, sender_city_town, sender_postcode, dest_receiver_title_fullname,dest_first_line_of_address, dest_city_town, dest_mobile, transaction_id, created_at, country = address_data
                    
                    # Display the fetched addresses in the corresponding text boxes
                    self.factory.sender_build_door_no_ent.delete(0, END)
                    self.factory.sender_build_door_no_ent.insert(0, sender_build_door_no)
                                    
                    self.factory.sender_street_road_ent.delete(0, END)
                    self.factory.sender_street_road_ent.insert(0, sender_street_road)
                    
                    self.factory.sender_city_town_ent.delete(0, END)
                    self.factory.sender_city_town_ent.insert(0, sender_city_town)
                    
                    self.factory.sender_postcode_ent.delete(0, END)
                    self.factory.sender_postcode_ent.insert(0, sender_postcode)
                    
                    self.factory.dest_receiver_title_fullname_ent.delete(0, END)
                    self.factory.dest_receiver_title_fullname_ent.insert(0, dest_receiver_title_fullname)
                                    
                    self.factory.dest_first_line_of_address_ent.delete(0, END)
                    self.factory.dest_first_line_of_address_ent.insert(0, dest_first_line_of_address)
                    
                    self.factory.dest_city_town_ent.delete(0, END)
                    self.factory.dest_city_town_ent.insert(0, dest_city_town)
                    
                    country = address_data[10] if address_data[10] else "Unknown"
                    self.factory.dest_country.delete(0, END)
                    self.factory.dest_country.insert(0, country)
                    
                    self.factory.dest_mobile_ent.delete(0, END)
                    self.factory.dest_mobile_ent.insert(0, dest_mobile)
            
                    # call produce_receipt() method to generate the receipt
                    receipt.produce_receipt(transaction_id, created_at)
                
                    # Enable update button
                    self.factory.btn_update.config(state=NORMAL)
                
                    # Enable delete button
                    self.factory.btn_delete.config(state=NORMAL)           
            
        except Exception as e:
            messagebox.showerror("Database Error", f"Error retrieving addresses: {e}")  
            
    def bind_display_event(self):
        # Binds a mouse button release event to the Treeview widget (self.global_table),
        # triggering populating data to Entries in the DataFrameLeft  
        self.factory.global_table.bind("<ButtonRelease-1>", self.get_cursor)
            
            
# Your Displaying class is very comprehensive and well-written! Here’s a breakdown and some constructive suggestions to make it even better:

# What’s great:
# Database access with context manager (with DatabaseManager.with_connection() as conn): clean and safe.

# Error handling with message boxes for user-friendly error reporting.

# Data display logic in display_data() is clear and correctly handles clearing and populating the Treeview.

# Detailed get_cursor() method that:

# Extracts row data properly,

# Handles splitting full name into first and last,

# Retrieves additional address info from DB,

# Updates multiple UI fields accordingly,

# Generates a receipt via another class.

# Separation of responsibilities: this class focuses on displaying and retrieving data, leaving other actions (like clearing, deleting) to separate classes.

# Suggestions for improvement:
# Fix error handling on load_country_list:

# python
# Copy
# Edit
# except DatabaseManager.with_connection().Error as e:
# This is incorrect — with_connection() returns a connection object, not an error class. You should catch a more general exception, like:

# python
# Copy
# Edit
# except Exception as e:
# or if your DatabaseManager defines a specific error class, import and catch that instead.

# Improve name splitting logic (in get_cursor):

# Currently, if a name has more than 2 parts (e.g. "John Michael Smith"), only first two parts are used.

# Consider:

# python
# Copy
# Edit
# if len(name_parts) >= 2:
#     self.factory.fname_ent.insert(0, name_parts[0])
#     self.factory.lname_ent.insert(0, " ".join(name_parts[1:]))
# else:
#     self.factory.fname_ent.insert(0, full_name)
#     self.factory.lname_ent.delete(0, END)
# This way, all parts after the first are considered last name.

# Cache or reuse Receipt instance instead of creating a new one every time get_cursor is called (depends on your Receipt implementation).

# Minor efficiency: you call conn.commit() in display_data() after just reading data. commit() is only needed after changes, so it can be removed.

# Code formatting: consider consistent indentations and line breaks to improve readability, e.g., break long SQL queries or parameter lists.

# Add docstrings to methods: you have one for display_data() but none for others. This helps maintainability.

# Example fix for load_country_list:
# python
# Copy
# Edit
# def load_country_list(self):
#     try:
#         with DatabaseManager.with_connection() as conn:
#             cursor = conn.cursor()
#             cursor.execute("SELECT country FROM country_price")
#             countries = [row[0] for row in cursor.fetchall()]
#             return countries
#     except Exception as e:
#         messagebox.showerror("Database Error", f"Failed to load countries: {e}")
#         return []