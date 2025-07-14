from tkinter import *
from tkinter import messagebox
from db.db_manager import DatabaseManager


class Searching:
    """ Searches data based on various fields """
    
    def __init__(self, factory):
        self.factory = factory    
    
    def search_data(self):
        search_by = self.factory.combo_search_opts.get()
        search_text = self.factory.search_ent.get().strip()
        print("Search text",search_text)
        

        if not search_text:
            messagebox.showerror("Input Error", "Please enter a search term.")
            return

        search_map = {
            "Transaction Id": "transaction_id",
            "First Name": "full_name",
            "Last Name": "full_name",
            "Mobile": "mobile",
            "Email": "email",
            "Status": "status_of_goods",
            # "Country" needs special handling
        }

        try:
            with DatabaseManager.with_connection() as conn:
                cursor = conn.cursor()

                if search_by in ["First Name", "Last Name"]:
                    column = search_map[search_by]
                    query = f"SELECT * FROM shipments WHERE {column} LIKE ?"
                    search_value = f"%{search_text}%"

                else:
                    column = search_map.get(search_by)
                    print("column:", column)
                    if not column:
                        messagebox.showerror("Search Error", "Invalid search criteria selected.")
                        return
                    query = f"SELECT * FROM shipments WHERE {column} = ?" 
                    search_value = search_text
                    
                    
                cursor.execute(query, (search_value,))
                rows = cursor.fetchall()
                
            # deleting all chidren at once
            self.factory.global_table.delete(*self.factory.global_table.get_children())
            

            if rows:
                for row in rows:
                    self.factory.global_table.insert("", END, iid=row[1], values=(
                        row[0], row[1], row[2], row[3], row[4],
                        row[5], row[8], row[9], row[10], row[11], row[12]
                    ))          
            else:
                messagebox.showinfo("Search Result", "No matching records found.")

        except Exception as e:
            messagebox.showerror("Database Error", str(e))
            
    def bind_searching_events(self):
        key_release_event = "<KeyRelease>"
        self.factory.search_ent.bind(key_release_event , self.check_search_entry)
        
    def check_search_entry(self, event=None):
        if self.factory.search_ent.get().strip():
            self.factory.btn_search.config(state=NORMAL)
            self.factory.btn_back.config(state=NORMAL)
        else:
            self.factory.btn_search.config(state=DISABLED)
            self.factory.btn_back.config(state=DISABLED)

            
# Suggestion for improvements

# 2.Search by Last Name in full_name column
# Your search_map maps both "First Name" and "Last Name" to "full_name". But full_name stores the combined first and last names. Searching for last name alone using LIKE on full_name could still work, but might be imprecise.

# If you have separate columns for first name and last name in the database, search by those columns respectively.

# If not, searching full_name LIKE '%search_text%' can work but might give false positives.

# If you want to search last name only and you store full_name as "First Last", you could split it in SQL or store last names separately. Otherwise, keep it as is but know the limitation.

# 3. Search by Country
# In your mapping, "Country": "country" is mapped to country. But in your shipments table definition, the country is not stored directly as country but rather referenced via country_price_id foreign key.

# If you want to search by country name, you need to join the shipments table with the country_price table to filter by country name.

# So the current code will fail for "Country" searches.

