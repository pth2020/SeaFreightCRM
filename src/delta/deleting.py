from tkinter import *
from tkinter import messagebox
from db.db_manager import DatabaseManager
from .displaying import Displaying
from .clearing import Clearing

class Deleting:
    """ Delete a selected row or data """
    
    def __init__(self, factory):
        self.factory = factory
    
    def delete_data(self):
        # Check if a record is selected
        selected = self.factory.global_table.focus()
        if not selected:
            messagebox.showerror("Selection Error", "Please select a record to delete.")
            return

        content = self.factory.global_table.item(selected)
        row = content["values"]
    
        if not row:
            messagebox.showerror("Selection Error", "Selected record has no data.")
            return

        transaction_id = row[1]  # Assuming transaction_id is in column 1

        # Confirm deletion
        confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete transaction ID {transaction_id}?")
        if not confirm:
            return

        try:
            # Connect to the database and delete the record
            with DatabaseManager.with_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM shipments WHERE transaction_id = ?", (transaction_id,))
                conn.commit()

            # Refreshing the Treeview
            self.factory.global_table.delete(*self.factory.global_table.get_children())
            displaying = Displaying(self.factory)
            displaying.display_data()

            # Clearing fields 
            clearing = Clearing(self.factory)
            clearing.clear_fields()
            
            # binding fields - displaying hints
            self.factory.bind_event()
            
            # Disabling buttons
            self.factory.btn_delete.config(state=DISABLED)
            self.factory.btn_update.config(state=DISABLED)

            messagebox.showinfo("Success", f"Record with Transaction ID {transaction_id} has been deleted.")

        except Exception as e:
            messagebox.showerror("Database Error", str(e))
            
# Highlights
#Proper error handling: You check if a record is selected and whether it contains valid data.
#Safe deletion: A confirmation dialog ensures users don’t delete accidentally.
#Database integrity: Using with DatabaseManager.with_connection() is a clean, reliable pattern.
#Modular design: Instantiating Displaying and Clearing properly:


