from tkinter import *
from tkinter import messagebox
import datetime
from db.db_manager import DatabaseManager
from .displaying import Displaying
from .clearing import Clearing
from .form_data import FormData


class Updating:
    
    def __init__(self, factory):
        self.factory = factory
        self.displaying = Displaying(self.factory)
        self.fd = FormData(self.factory)
        self.save_status_to = None
        self.shipped_date = ""

    def update_data(self):
        """ Updates a selected data (row) from the Treeview """
        
        # Getting form values       
        self.form_data = self.fd.get_form_values()
        
        # Ensure a row is selected from the Treeview
        selected = self.factory.global_table.focus() # Treeview in setup_details_table() function
        if not selected:
            messagebox.showerror("Selection Error", "Please select a shipment record to update.")
            return

        # Get data from selected row to retrieve the transaction_id
        content = self.factory.global_table.item(selected)
        row = content["values"]
    
        # Checking a row contains more than an id
        if len(row) < 2 or not row[1]:  # transaction_id should be in row[1]
            messagebox.showerror("Data Error", "Selected row does not have a valid transaction ID.")
            return

        # transaction_id = local variable, self.transaction_id = instance variable 
        transaction_id = row[1]  # Fetch from Treeview directly, ensures reliability
        self.transaction_id = transaction_id  # Optionally re-set it for consistency

        # Validate required fields
        if self.factory.fname_ent.get().strip() == "" or self.factory.mobile_ent.get().strip() == "":
            messagebox.showerror("Input Error", "First Name and Mobile are required.")
            return
        
        # Extract variables from dictionary
        fname = self.form_data["fname"]
        lname = self.form_data["lname"]
        full_name = f"{fname} {lname}"
        mobile = self.form_data["mobile"]
        email = self.form_data["email"]
        sender_build_door_no = self.form_data["sender_build_door_no"]
        sender_street_road = self.form_data["sender_street_road"]
        sender_city_town = self.form_data["sender_city_town"]
        sender_postcode = self.form_data["sender_postcode"]
        dest_receiver_title_fullname = self.form_data["dest_receiver_title_fullname"]
        dest_first_line_of_address = self.form_data["dest_first_line_of_address"]
        dest_city_town = self.form_data["dest_city_town"]
        dest_country = self.form_data["dest_country"]
        dest_mobile = self.form_data["dest_mobile"]
        goods_type = self.form_data["goods_type"]
        weight = self.form_data["weight"]
        form_status = self.form_data["status"]
        
        # Validate weight entered is numeric        
        if not isinstance(weight, str) or not weight.strip().replace('.', '', 1).isdigit():
            messagebox.showerror("Input Error", "Weight is required and must be numeric.")
            return

        # convert weight(string) into weight(float)
        weight_float = float(weight)
            
        # get country_id, price for selected country
        result = self.get_selected_country_id(dest_country)
            
        if result is None:
            return  # Already shows error in the method
        
        # retrieve country_id and shipping price from country_price table
        country_id, country_price = result

        # Calculate estimated cost 
        estimated_cost = weight_float *  country_price
        
        # FETCH existing date_shipped from DB
        with DatabaseManager.with_connection() as conn:
            cur = conn.cursor()
            cur.execute("SELECT date_shipped FROM shipments WHERE transaction_id = ?", (transaction_id,))
            result = cur.fetchone()
        existing_date_shipped = result[0] if result and result[0] else ""

        # Store it on the instance so validate() can see it
        self.shipped_date = existing_date_shipped
        
        # validate/change status of goods (disallow backward update) 
        new_status = self.validate_goods_status(transaction_id, form_status)
        if new_status is None:
            # Illegal transition — already handled with message in validate_goods_status()
            return
        self.save_status_to = new_status
            
        
        # Update database            
        try:
                
            with DatabaseManager.with_connection() as conn: # with closes db connection automatically when job done
                cursor = conn.cursor()
                cursor.execute("""
                        UPDATE shipments
                        SET full_name=?, mobile=?, email=?, sender_build_door_no=?, sender_street_road=?, 
                            sender_city_town=?, sender_postcode=?, dest_receiver_title_fullname=?, dest_first_line_of_address=?,
                            dest_city_town=?, dest_mobile=?, type_of_goods=?, total_weight=?, 
                            date_shipped=?, total_cost=?, status_of_goods=?, country_price_id=?
                        WHERE transaction_id=?
                        """, (
                        full_name, mobile, email, sender_build_door_no, sender_street_road, sender_city_town,
                        sender_postcode, dest_receiver_title_fullname, dest_first_line_of_address, dest_city_town,
                        dest_mobile, goods_type, weight_float, self.shipped_date, estimated_cost, self.save_status_to, country_id, transaction_id
)                   )                
                conn.commit()
            
                # Display/show updated data on treeview at the bottom of the frame                
                self.displaying.display_data()
                # confirm updating of data
                messagebox.showinfo("Success", "Record updated on database.")
                # disable update button
                self.factory.btn_save.config(state=DISABLED)
                # clear fields
                clearing = Clearing(self.factory)
                clearing.clear_fields()
                # binding fields - displaying hints
                self.factory.bind_event()
            
        
        except ValueError:
            messagebox.showerror("Input Error", "Invalid weight input. Please enter a valid number.")

        except Exception as e:
            messagebox.showerror("Database Error", str(e))            
            
            
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
                
        
    def validate_goods_status(self, transaction_id, update_to_status):
        """Updates goods status"""
        """Disallows backward status updates like Arrived → Shipped, Arrived → Collected."""

        try:
            with DatabaseManager.with_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT status_of_goods FROM shipments WHERE transaction_id = ?", (transaction_id,))
                result = cursor.fetchone()

            if not result:
                messagebox.showerror("Error", f"No shipment found for Transaction ID {transaction_id}")
                return

            current_db_status = result[0]
            transit_status = "Shipped - In transit"

            # Illegal transitions
            if current_db_status == "Arrived" and update_to_status in ("Collected", transit_status):
                messagebox.showerror("Status Error", f"Cannot update status from {current_db_status} to {update_to_status}.")
                return None
                
            elif current_db_status == transit_status and update_to_status == "Collected":
                messagebox.showerror("Status Error", f"Cannot update status from {current_db_status} to {update_to_status}.")
                return None
            
            elif current_db_status == "Collected" and update_to_status == "Arrived":
                messagebox.showerror("Status Error", f"You must change status to {transit_status} before {update_to_status}.")
                return None  

            # Collected → Shipped (allowed)
            if current_db_status == "Collected" and update_to_status == transit_status:
                self.shipped_date = datetime.datetime.now().strftime('%d-%m-%Y')
                self.save_status_to = transit_status
                return self.save_status_to

            # Shipped → Arrived (allowed)
            if current_db_status == transit_status and update_to_status == "Arrived":
                self.save_status_to = "Arrived"
                return self.save_status_to 

            # Already same status (no update)
            if current_db_status == update_to_status:
                messagebox.showinfo("Status Info", f"Status is already '{current_db_status}'. Good's status not updated.")
                return current_db_status

            # For any other case, show a message (optional)
            messagebox.showwarning("Status Warning", f"Transition from '{current_db_status}' to '{update_to_status}' is not defined.")
            
        except Exception as e:
            messagebox.showerror("Database Error", str(e))