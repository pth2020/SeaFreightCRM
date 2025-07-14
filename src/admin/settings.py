from db.db_manager import DatabaseManager
from tkinter import messagebox
import tkinter as tk
from tkinter import ttk
import sqlite3
import datetime

class SettingsFrame(tk.Frame):
    def __init__(self, master, factory):
        super().__init__(master)
        self.factory = factory
        #self.content = master

        #self.factory.set_up_styles()        # ← you need this
        self.settings_logic = self.factory.settings_logic  # ← required to use logic methods in button callbacks
        
        #self.create_settings()      # ← and you need this to build the UI   
        self.factory.set_up_styles()  
        
        
    def create_settings(self):
        """    
            Settings frame has four sections: 
            1) Edit User Account
            2) Add User Account
            3) Set £ price per kg 
            4) Add drop down menu (e.g. destination country, goods status )
        """
        # clears frame before showing settings frame
        #self.factory.clear_content()
        
        # Initialising settings frame
        self.settings_frame = tk.Frame(self, relief=tk.RIDGE, bd=10, bg="#33bbf9")
        self.settings_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Setting title
        title = tk.Label(self.settings_frame, text="Settings", font=("Arial", 18, "bold"), bg="#33bbf9", fg="white")
        title.pack(pady=10)

        # container inside settings_frame that has four items  
        grid_container = tk.Frame(self.settings_frame, bg="#33bbf9")
        grid_container.pack(fill="both", expand=True, padx=10, pady=10)

        # Configuring grid layout inside grid_container
        for row in range(2):
            grid_container.grid_rowconfigure(row, weight=1)
        for col in range(2):
            grid_container.grid_columnconfigure(col, weight=1)

        # labels for the four sections of the grid_container
        labels = ["Edit User Account", "Add User Account", "Set £ Price per Kg", "Add Drop-down Menu"]

        for i in range(4):
            row = i // 2
            col = i % 2

            # looping through 0 to 3 to position the sections using row and col attributes
            section = tk.Frame(grid_container, relief=tk.RIDGE, bd=5, bg="#f0f0f0")
            section.grid(row=row, column=col, sticky="nsew", padx=10, pady=10)

            # labeling sections
            tk.Label(section, text=labels[i], font=("Arial", 14, "bold"), bg="#f0f0f0").pack(pady=(10, 5))

            # Edit User Account
            if i == 0:  
                # Bordered frame for find username and password
                self.find_form_frame = tk.Frame(section, bd=2, relief="ridge", bg="#f0f0f0")
                self.find_form_frame.place(x=50, y=50, width=500, height=150)
                                        
                tk.Label(self.find_form_frame, text="Username:", **self.factory.label_opts).place(x=10, y=10)
                self.username_ent1 = tk.Entry(self.find_form_frame, **self.factory.entry_opts)
                self.username_ent1.place(x=150, y=15, width=175)  # Position right next to the label

                # Password Label and Entry in the second row
                tk.Label(self.find_form_frame, text="Password:", **self.factory.label_opts).place(x=10, y=50)
                self.password_ent1 = tk.Entry(self.find_form_frame, show="*", **self.factory.entry_opts)
                self.password_ent1.place(x=150, y=55, width=175)  # Right next to the Password label
                
                # lambda s=section: self.find_user(s) ensures section is correctly captured.
                # It delays find_user execution until the user clicks the button.
                # No premature access to .get() or closed cursors.                
                find_btn = tk.Button(self.find_form_frame,text="Find",**self.factory.button_opts,
                                    command=lambda s=section: (self.settings_logic.find_user(s)))
                find_btn.place(x=150, y=95, width=175, height=30)  # Find button to trigger the search
                
                
                
            elif i == 1:  # Add an user account
                # Bordered frame for adding an account
                self.add_form_frame = tk.Frame(section, bd=2, relief="ridge", bg="#f0f0f0")
                self.add_form_frame.place(x=50, y=50, width=500, height=190)
                
                tk.Label(self.add_form_frame, text="Username:", **self.factory.label_opts).place(x=10, y=10)
                self.username_ent2 = tk.Entry(self.add_form_frame, **self.factory.entry_opts)
                self.username_ent2.place(x=180, y=15, width=175)  # Position right next to the label

                # Password Label and Entry in the second row
                tk.Label(self.add_form_frame, text="Password:", **self.factory.label_opts).place(x=10, y=50)
                self.password_ent2 = tk.Entry(self.add_form_frame, show="*", **self.factory.entry_opts)
                self.password_ent2.place(x=180, y=55, width=175)  # Right next to the Password label
                
                # Confirm Password Entry
                tk.Label(self.add_form_frame, text="Confirm Password:", **self.factory.label_opts).place(x=10, y=90)
                self.confirm_password_ent2 = tk.Entry(self.add_form_frame, show="*" ,**self.factory.entry_opts)
                self.confirm_password_ent2.place(x=180, y=95, width=175)
                
                # lambda s=section: self.find_user(s) ensures section is correctly captured.
                # It delays find_user execution until the user clicks the button.
                # No premature access to .get() or closed cursors.                
                add_btn = tk.Button(self.add_form_frame,text="Add",**self.factory.button_opts,command=self.settings_logic.add_user)
                #command=lambda s=section: (self.settings_logic.add_user(s))
                add_btn.place(x=180, y=135, width=175, height=30)  # Find button to trigger the search
                
            elif i == 2:  # Set £ Price per Kg
                # Bordered frame for setting shipping price for countries
                self.set_price_for_country = tk.Frame(section, bd=2, relief="ridge", bg="#f0f0f0")
                self.set_price_for_country.place(x=50, y=50, width=500, height=150)

                tk.Label(self.set_price_for_country, text="Country:", **self.factory.label_opts).place(x=10, y=10)

                # Create and place Combobox  
                self.country_combo = ttk.Combobox(self.set_price_for_country, state="readonly", **self.factory.combo_opts)
                self.country_combo.place(x=150, y=15, width=175)
                #self.settings.load_countries_into_combobox()  # Load country list
                self.settings_logic.load_countries_into_combobox(self)

                # Bind selection to update price field
                #self.country_combo.bind("<<ComboboxSelected>>", self.settings_logic.on_country_selected)
                self.country_combo.bind("<<ComboboxSelected>>", lambda event: self.settings_logic.on_country_selected(self, event))
                
                tk.Label(self.set_price_for_country, text="£", font=("Arial", 12)).place(x=135, y=55)
                
                tk.Label(self.set_price_for_country, text="Price:", **self.factory.label_opts).place(x=10, y=50)
                self.price_entry = tk.Entry(self.set_price_for_country, **self.factory.entry_opts)
                self.price_entry.place(x=150, y=55, width=175)                
                # find_btn = tk.Button(self.set_price_for_country, text="Update", **self.factory.button_opts, 
                #                     command=self.settings_logic.update_country_price)
                find_btn = tk.Button(self.set_price_for_country, text="Update", **self.factory.button_opts, 
                                    command=lambda: self.settings_logic.update_country_price(self))
                
                find_btn.place(x=150, y=95, width=175, height=30)
            
            
            elif i == 3:  # To add dropdown boxes
                
                self.default_price = 0.0
                
                # Bordered frame for adding country and price
                self.add_combo_form_frame = tk.Frame(section, bd=2, relief="ridge", bg="#f0f0f0")
                self.add_combo_form_frame.place(x=50, y=50, width=500, height=150)
                
                # Add country
                tk.Label(self.add_combo_form_frame, text="Country:", **self.factory.label_opts).place(x=10, y=10)
                self.country_ent = tk.Entry(self.add_combo_form_frame, **self.factory.entry_opts)
                self.country_ent.place(x=150, y=15, width=175)

                #  use a lambda to defer the function call until the button is clicked.
                country_add_btn = tk.Button(self.add_combo_form_frame, text="Add", **self.factory.button_opts, 
                #command=lambda s=section: (self.settings_logic.add_country(self.add_combo_form_frame,self.country_ent.get(), self.default_price)))
                command=lambda: self.settings_logic.add_country(self, self.country_ent.get(), self.default_price))
                country_add_btn.place(x=340, y=10, width=100, height=30)

                # Add type of good (positioned below the country)
                tk.Label(self.add_combo_form_frame, text="Type of Good:", **self.factory.label_opts).place(x=10, y=60)
                self.type_of_good_ent = tk.Entry(self.add_combo_form_frame, **self.factory.entry_opts)
                self.type_of_good_ent.place(x=150, y=65, width=175)

                type_of_good_add_btn = tk.Button(self.add_combo_form_frame, text="Add", **self.factory.button_opts)
                type_of_good_add_btn.place(x=340, y=60, width=100, height=30)
                
    def show_update_fields(self, section):
        """ Hides find_form_frame and shows update_fields form frame """
        
        # Bordered frame for find username and password
        self.edit_frame = tk.Frame(section, bd=2, relief="ridge", bg="#f0f0f0")
        self.edit_frame.place(x=50, y=50, width=500, height=190)     
        
        # Prompt user to enter new username and password

        # Username Label and Entry for new username
        tk.Label(self.edit_frame, text="Current / New Username:", **self.factory.label_opts).place(x=10, y=10)
        self.new_username_ent1 = tk.Entry(self.edit_frame, **self.factory.entry_opts)
        self.new_username_ent1.place(x=230, y=15, width=175)

        # Password Label and Entry for new password
        tk.Label(self.edit_frame, text="New Password:", **self.factory.label_opts).place(x=10, y=50)
        self.new_password_ent1 = tk.Entry(self.edit_frame, show="*", **self.factory.entry_opts)
        self.new_password_ent1.place(x=230, y=55, width=175)

        # Confirm Password Entry
        tk.Label(self.edit_frame, text="Confirm Password:", **self.factory.label_opts).place(x=10, y=90)
        self.confirm_password_ent1 = tk.Entry(self.edit_frame, show="*" ,**self.factory.entry_opts)
        self.confirm_password_ent1.place(x=230, y=95, width=175)

        # Add a Button to confirm update
        update_btn = tk.Button(self.edit_frame, text="Update", **self.factory.button_opts, 
                            command=lambda s=section: (self.settings_logic.update_user(s)))
        update_btn.place(x=230, y=135, width=175, height=30)
        
    def show_find_form(self, section):
        # Ensure the find_form_frame is visible or recreated here
        if not hasattr(self, 'find_form_frame'):
            # Create the find_form_frame if it does not exist
            self.find_form_frame = tk.Frame(self.content, bd=2, relief="ridge", bg="#f0f0f0")
            self.find_form_frame.place(x=50, y=50, width=500, height=150)

            tk.Label(self.find_form_frame, text="Username:", **self.factory.label_opts).place(x=10, y=10)
            self.username_ent1 = tk.Entry(self.find_form_frame, **self.factory.entry_opts)
            self.username_ent1.place(x=150, y=15, width=150)  # Position right next to the label

            tk.Label(self.find_form_frame, text="Password:", **self.factory.label_opts).place(x=10, y=50)
            self.password_ent1 = tk.Entry(self.find_form_frame, show="*", **self.factory.entry_opts)
            self.password_ent1.place(x=150, y=55, width=150)  # Right next to the Password label

            # Find button
            find_btn = tk.Button(self.find_form_frame, text="Find", **self.factory.button_opts, 
                                command=lambda s=section: (self.settings_logic.factory.show_settings(), self.settings_logic.find_user(s)))
            find_btn.place(x=150, y=95, width=100, height=30)  # Find button to trigger the search
        else:
            # If the form already exists, just make it visible again
            self.find_form_frame.lift()  # Bring it to the front if it's hidden
            self.find_form_frame.place(x=50, y=50, width=500, height=150)



class Setting:
    """ Use database to find/add/edit data for the four sections of the settings frame """
    
    def __init__(self, factory):
        self.factory = factory
        self.settings_frame = None
        

    def set_settings_frame(self, settings_frame):
        self.settings_frame = settings_frame

    
    def find_user(self, section):
        """ search a user to update their username and/or password """
        # Get input from entry widgets
        username_input = self.settings_frame.username_ent1.get().strip()
        password_input = self.settings_frame.password_ent1.get().strip()
        
        
        try:
            with DatabaseManager.with_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                "SELECT username FROM Users WHERE username = ? AND password = ?",(username_input, password_input))
                # Fetch the next row of a query result, returning it as a tuple, or None if there are no more rows.
                result = cursor.fetchone()
                
                if result:
                    # Save username for use in update_user later
                    self.authenticated_username = username_input
                    # Destroy the form_frame after capturing input
                    if hasattr(self.settings_frame, 'find_form_frame'):
                        # hides parent frame
                        self.settings_frame.find_form_frame.place_forget() 
                        # Show the update fields to update username/password 
                        self.settings_frame.show_update_fields(section)
                else:
                    messagebox.showinfo("Failure", "No matching user found.")
                    self.settings_frame.username_ent1.delete(0, tk.END)
                    self.settings_frame.password_ent1.delete(0, tk.END)
                    self.settings_frame.username_ent1.focus_set()
                    
                
        except DatabaseManager.with_connection().Error as e:
            messagebox.showerror("Database Error", f"Failed to change username/password: {e}")
            
    def update_user(self, section):
        # Get the new username and password from the Entry widgets
        new_username = self.settings_frame.new_username_ent1.get()
        new_password = self.settings_frame.new_password_ent1.get()
        confirm_password = self.settings_frame.confirm_password_ent1.get()

        if new_password != confirm_password:
            messagebox.showinfo("Failure", "Passwords do not match.")
            self.settings_frame.new_username_ent1.delete(0, tk.END)
            self.settings_frame.new_password_ent1.delete(0, tk.END)
            self.settings_frame.confirm_password_ent1.delete(0, tk.END)
            self.settings_frame.new_username_ent1.focus_set()
            return

        # Execute an update query to modify the user's username and password in the database
        try:
            with DatabaseManager.with_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("UPDATE Users SET username = ?, password = ? WHERE username = ?", (new_username, new_password, self.authenticated_username))
            
                conn.commit()
                messagebox.showinfo("Success", "User updated successfully.")
            
            # Destroy the edit_frame after updating username/password
            if hasattr(self, 'edit_frame'):
                self.factory.edit_frame.destroy()
                
            # Clear the username and password fields before showing the find_form_frame
            self.settings_frame.username_ent1.delete(0, tk.END)
            self.settings_frame.password_ent1.delete(0, tk.END)

            # Back to the default find_frame
            self.settings_frame.show_find_form(section)
            
            
        except DatabaseManager.with_connection().Error as e:
            messagebox.showerror("Database Error", f"Failed to update user: {e}")
            
    def add_user(self):
        # Get the new username and password to add 
        username = self.settings_frame.username_ent2.get()
        password = self.settings_frame.password_ent2.get()
        confirm_password = self.settings_frame.confirm_password_ent2.get()

        if password != confirm_password:
            messagebox.showinfo("Failure", "Passwords do not match.")
            self.settings_frame.username_ent2.focus_set()
            return

        # Execute an update query to modify the user's username and password in the database
        try:
            with DatabaseManager.with_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(""" INSERT INTO users(username, password) VALUES(?, ?)""", (username, password))            
                conn.commit()
                messagebox.showinfo("Success", "User added successfully.")
                
                self.settings_frame.username_ent2.delete(0, tk.END)
                password = self.settings_frame.password_ent2.delete(0, tk.END)
                confirm_password = self.settings_frame.confirm_password_ent2.delete(0, tk.END)

        except DatabaseManager.with_connection().Error as e:
            messagebox.showerror("Database Error", f"Failed to add user: {e}")
            
            
    def on_country_selected(self, frame, event=None):
        """ Fetch country's shipping price upon selection of a country """
        selected_country = frame.country_combo.get()
        try:
            with DatabaseManager.with_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT price FROM country_price WHERE country = ?", (selected_country,))
                result = cursor.fetchone()
                if result:
                    frame.price_entry.delete(0, tk.END)
                    #frame.price_entry.insert(0, str(result[0]))
                    # Format to two decimal places:
                    frame.price_entry.insert(0, f"{result[0]:.2f}")
                else:
                    frame.price_entry.delete(0, tk.END)
                    frame.price_entry.insert(0, "0.00")

        except DatabaseManager.with_connection().Error as e:
            messagebox.showerror("Database Error", f"Failed to load price: {e}")
            
                
    def update_country_price(self, frame):
        country = frame.country_combo.get()
        try:
            price = float(frame.price_entry.get().strip())
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid price.")
            return

        try:
            with DatabaseManager.with_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(""" UPDATE country_price  SET price = ? WHERE country =? """, (price, country))
                conn.commit()
                messagebox.showinfo("Success", "Country's price updated successfully.")
                frame.price_entry.delete(0, tk.END)
                frame.country_combo.set("Select a country")
        except DatabaseManager.with_connection().Error as e:
            messagebox.showerror("Database Error", f"Failed to update country's price: {e}")
            
    def add_country(self, frame, country, price):
        """ Add new countries and their shipping prices into country_price table in the database """
        
        # check if shipments table exists first 
        with DatabaseManager.with_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS shipments (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    transaction_id TEXT,
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
        
        try:
            with DatabaseManager.with_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO country_price(country, price) VALUES (?, ?)",
                    (country.strip(), price)
                )
                conn.commit()

            messagebox.showinfo("Success", "Country added successfully.")

            # reload the dropdown
            self.load_countries_into_combobox(frame)

            # then select the newly added country
            frame.country_combo.set(country.strip())

            # clear the entry
            frame.country_ent.delete(0, tk.END)

        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Failed to add country: {e}")

    def load_countries_into_combobox(self, frame):
        """ Load all countries from db and add a default prompt at the top """
        
        if not hasattr(frame, 'country_combo'):
            messagebox.showerror("Error", "Country combo box not found.")
            return

        try:
            with DatabaseManager.with_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT country FROM country_price")
                countries = [row[0] for row in cursor.fetchall()]

            # Prepend the default prompt
            display_values = ["Select a country"] + countries

            # Update the combobox
            frame.country_combo['values'] = display_values
            frame.country_combo.set("Select a country")

        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Failed to load countries: {e}")
            

            
# if hasattr(self.factory, 'edit_frame'):
#     self.factory.edit_frame.destroy()

# 8. [Optional but Recommended] Improve Combobox Reset
# To reset combobox after price update:

# python
# Copy
# Edit
# self.factory.country_combo.set("Select a country")
# Make sure "Select a country" is in the list. Otherwise, do:

# python
# Copy
# Edit
# self.factory.country_combo.set('')

# Minor improvements
# Consider disabling the Add button in add_user() after success to prevent double submissions.

# Add try-except for parsing price as float in update_country_price.

