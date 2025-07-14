from tkinter import *
from tkinter import messagebox
import datetime
import random
import uuid
from tkinter import ttk
from db.db_manager import DatabaseManager
from .displaying import Displaying 
from .receipt import Receipt 
from .clearing import Clearing 
from .form_data import FormData 


class Saving:
    
    def __init__(self, factory):
        self.factory = factory
        self.transaction_id = None
        self.displaying = Displaying(self.factory)
        self.fd = FormData(self.factory)
        self.receipt = Receipt(self.factory)
        
    
    def save_data(self):
        """ Saves sender and destination data to the database """
        
        # Simple validation - checks if all entries are entered 
        self.check_entries()
        
        # Create shipments table if it does not exist
        self.create_shipments_table()

        # ====== Transaction ID ===============
        
        # Generate a random transaction id for a sender
        self.transaction_id = self.generate_unique_transaction_id()
        
        # ===== Collect all form values =======
        
        # Create instance of FormData that collects data entered in the frame
        form_values = self.fd.get_form_values()

        # Extract variables from dictionary (form_values)
        fname = form_values["fname"]
        lname = form_values["lname"]
        full_name = f"{fname} {lname}"
        mobile = form_values["mobile"]
        email = form_values["email"]
        sender_build_door_no = form_values["sender_build_door_no"]
        sender_street_road = form_values["sender_street_road"]
        sender_city_town = form_values["sender_city_town"]
        sender_postcode = form_values["sender_postcode"]
        dest_receiver_title_fullname = form_values["dest_receiver_title_fullname"]
        dest_first_line_of_address = form_values["dest_first_line_of_address"]
        dest_city_town = form_values["dest_city_town"]
        dest_country = form_values["dest_country"]
        dest_mobile = form_values["dest_mobile"]
        goods_type = form_values["goods_type"]
        weight = form_values["weight"]
        status = form_values["status"]
        
        # ==== Current date =====
        
        # current date for collection date
        collected_date = datetime.datetime.now().strftime('%Y-%m-%d')

        # Initialily shipped_date is set to empty, updated later when goods get shipped
        shipped_date = ""
        # When goods shipped date is updated to current date
        if self.factory.status_of_goods.get() == 'Shipped - In Transit':
            shipped_date = datetime.datetime.now().strftime('%Y-%m-%d')
        
        # ===== Full Name = {first name} + {last name}  ===
        
        # concanate first name and last name of sender to full name before saving to db
        full_name = f"{fname} {lname}"
        
        #===== Weight =======
                
        # Validate weight entered is numeric        
        if not isinstance(weight, str) or not weight.strip():
            messagebox.showerror("Input Error", "Weight is required and must be numeric.")
            return
        
        # conversion of string to float type for weight entered
        try:
            weight_float = float(weight)
        except ValueError:
            messagebox.showerror("Input Error", "Weight must be a valid number.")
            return
        
        # To Get country Id (foreign key) from shipments table, use country name, dest_country, 
        # and match it with country in country_price table in the database - connect to db
        result = self.displaying.get_selected_country_id(dest_country) # returns a tuple, (id, price)
                
        if result == (None, None):
            return  # Already shows error in the method
        country_id, country_price = result # assigns first and second elements of tuple to country_id and country_price

        # works out total cost of shipment 
        estimated_cost = weight_float * country_price
        
        # connect to db to insert data
        try:
            with DatabaseManager.with_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(""" 
                    INSERT INTO shipments (transaction_id, created_at, full_name, mobile, email,
                        sender_build_door_no, sender_street_road, sender_city_town, sender_postcode,
                        dest_receiver_title_fullname, dest_first_line_of_address, dest_city_town, dest_mobile,
                        type_of_goods, total_weight, date_shipped, total_cost, status_of_goods, country_price_id) 
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", 
                    (self.transaction_id, collected_date, full_name, mobile, email,
                    sender_build_door_no, sender_street_road, sender_city_town, sender_postcode,
                    dest_receiver_title_fullname, dest_first_line_of_address, dest_city_town, dest_mobile,
                    goods_type, weight_float, shipped_date, estimated_cost, status, country_id))
                
                #commit save
                conn.commit()
                
            # Show saved data on treeview at the bottom of the frame
            self.displaying.display_data()
            
            # display receipt
            self.receipt.produce_receipt(self.transaction_id, collected_date)            

            # confirm data saving
            messagebox.showinfo("Success", "Record saved to database.")
            
            # disable save button
            self.factory.btn_save.config(state=DISABLED)
            
            # Clear fields
            clearing = Clearing(self.factory) 
            clearing.clear_fields()
            
            # binding fields - displaying hints
            self.factory.bind_event()

        except Exception as e:
            messagebox.showerror("Database Error", str(e))
            
    def transaction_id_exists(self, transaction_id):
        """ Checking for duplicate Transaction id """
        with DatabaseManager.with_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT 1 FROM shipments WHERE transaction_id = ?", (transaction_id,))
            return cursor.fetchone() is not None
        
    def generate_unique_transaction_id(self):
        while True:
            # Create hexadecimal transaction id
            trx_id = f"TRX{uuid.uuid4().hex[:8].upper()}"

            # call method to verfiy uniqueness of transaction_id
            if not self.transaction_id_exists(trx_id):
                return trx_id
        
    def create_shipments_table(self):
        """ creates shipments table if not exists - called only once """
        
        with DatabaseManager.with_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS shipments (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    transaction_id TEXT UNIQUE,
                    created_at TEXT DEFAULT (DATE('now')),
                    full_name TEXT,
                    mobile TEXT,
                    email TEXT,
                    sender_build_door_no TEXT,
                    sender_street_road TEXT,
                    sender_city_town TEXT,
                    sender_postcode TEXT,
                    dest_receiver_title_fullname TEXT,
                    dest_first_line_of_address TEXT,
                    dest_city_town TEXT,
                    dest_mobile TEXT,
                    type_of_goods TEXT,
                    total_weight TEXT,                    
                    date_shipped TEXT, 
                    total_cost FLOAT,
                    status_of_goods TEXT,
                    country_price_id INTEGER,
                    FOREIGN KEY (country_price_id) REFERENCES country_price(id)
                )
            """)
            
    def bind_saving_events(self):
        # Bind Entry events to check if entries are filled out
        key_release_event = "<KeyRelease>"
        self.factory.fname_ent.bind(key_release_event, self.check_entries)
        self.factory.lname_ent.bind(key_release_event, self.check_entries)
        self.factory.mobile_ent.bind(key_release_event, self.check_entries)
        self.factory.email_ent.bind(key_release_event, self.check_entries)
        self.factory.total_weight_ent.bind(key_release_event, self.check_entries) 
        
                
    def check_entries(self, event=None):
        # Check if all required fields are filled
        if (self.factory.fname_ent.get().strip() != "" and
            self.factory.lname_ent.get().strip() != "" and
            self.factory.mobile_ent.get().strip() != "" and
            self.factory.email_ent.get().strip() != "" and
            self.factory.total_weight_ent.get().strip() != ""):
            
            # Enable Save button if all required fields are filled
            # NORMAL means the button is active and clickable.
            self.factory.btn_save.config(state=NORMAL)
            self.factory.btn_clear.config(state=NORMAL)
        else:
            # Disable Save button if any required field is empty
            # DISABLED would make it grayed out and unclickable.
            self.factory.btn_save.config(state=DISABLED)
            
            
# Your Saving class looks very well organized and robust, nicely tying together data validation, database saving, and UI updates. Here’s some feedback and suggestions for clarity, safety, and potential improvements:

# What’s working well:
# Validation: Checks essential fields before proceeding.

# Transaction ID: Generates a unique-ish transaction ID for each shipment.

# Data extraction: Uses FormData class to fetch form values cleanly.

# Date handling: Uses current datetime consistently.

# Database interaction: Creates table if needed and inserts data with a context manager.

# UI updates: Refreshes display, generates receipt, disables save button, clears fields, and re-binds events after saving.

# Error handling: Catches exceptions and informs the user clearly.


# Defensive Programming
# Here are a number of defensive-programming techniques you can layer into your save_data() flow to make it more robust, 
# maintainable, and easier to debug:


# Suggestions for Enhancement
# Transaction ID Uniqueness Check (Optional):
# You could check if transaction_id exists in the DB before using it.

# Better Date Management:
# Consider storing datetimes instead of date-only strings, especially for tracking.

# Logging (optional):
# Add logging instead of print() or silent return on DB errors for better debugging in production.

# 🧪 Recommended Testing
# Create test scenarios for:

# Saving with all fields filled (normal)

# Saving with missing weight (should error)

# Country not in DB (should show message)

# Weight as non-numeric string (should error)

# Status set to "Shipped - In Transit" (check if shipped_date is populated)

# Attempting to reuse the same transaction ID (unlikely with UUID, but still)


