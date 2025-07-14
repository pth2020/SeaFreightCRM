from db.db_manager import DatabaseManager
from tkinter import messagebox
import tkinter as tk
from tkinter import ttk
import sqlite3
from datetime import datetime


class NotesFrame(tk.Frame):
    def __init__(self, master, factory):
        super().__init__(master)
        self.factory = factory
        self.notes_logic = self.factory.notes_logic
        self.factory.set_up_styles()

        
    def create_notes(self):
        
        if hasattr(self, "notes_frame"):
            return
        
        # ========= Frames ============
        self.notes_frame = tk.Frame(self, bd=10, relief=tk.RIDGE, bg="#33bbf9")
        self.notes_frame.pack(fill="both",  expand=True, padx= 20, pady=10) 
        
        # == Note entry frame        
        self.enter_notes_frame = tk.LabelFrame(self.notes_frame, bd=8, relief=tk.RIDGE, padx=10,
                                font=("Helvetica", 13, "bold"), text="Add Notes",bg="#ffffff" , fg="#003366") # bg="#E6E6FA"
        self.enter_notes_frame .place(x=0, y=60, width=500, height=415)
        
        # == Note display list
        self.notes_list_frame = tk.LabelFrame(self.notes_frame, bd=8, relief=tk.RIDGE, padx=10,
                                    font=("Helvetica", 13, "bold"), text="List of Notes", bg="#ffffff", fg="#003366")
        self.notes_list_frame.place(x=501, y=60, width=773, height=415)
        
        style = ttk.Style()
        style.configure("Treeview.Heading", font=("Helvetica", 12, "bold"))
        style.configure("Treeview", font=("Helvetica", 11), rowheight=25)
        
        columns = ("id","subject", "contributor", "datetime")
        self.notes_listbox = ttk.Treeview(self.notes_list_frame, columns=columns, show="headings", height=15)

        # Define column headers
        self.notes_listbox.heading("id", text="ID")
        self.notes_listbox.heading("subject", text="Subject")
        self.notes_listbox.heading("contributor", text="Contributor")
        self.notes_listbox.heading("datetime", text="Date/Time")

        # Set column widths
        self.notes_listbox.column("id", width=50)
        self.notes_listbox.column("subject", width=250)
        self.notes_listbox.column("contributor", width=150)
        self.notes_listbox.column("datetime", width=200)

        self.notes_listbox.pack(fill="both", expand=True, padx=10, pady=10)     

                
        # Button holders - action and search menu
        self.notes_action_menu = tk.LabelFrame(self.notes_frame, bd=8, relief=tk.RIDGE, padx=10,
                                font=("Helvetica", 11, "bold"), text="Action Menu", bg="#ffffff", fg="#003366")
        self.notes_action_menu.place(x=0, y=475, width=630, height=80) # 1273
        
        self.notes_search_menu = tk.LabelFrame(self.notes_frame, bd=8, relief=tk.RIDGE, padx=10,
                                font=("Helvetica", 11, "bold"), text="Search Menu", bg="#ffffff", fg="#003366")
        self.notes_search_menu.place(x=630, y=475, width=642, height=80)
        
        
        self.current_note_frame = tk.LabelFrame(self.notes_frame, bd=8, relief=tk.RIDGE, padx=10,
                                    font=("Helvetica", 13, "bold"), text="Note", bg="#ffffff", fg="#003366")
        self.current_note_frame.place(x=0, y=553, width=1272, height=270)
        
        
        #
        self.note_display = tk.Text(self.current_note_frame,font=("Helvetica", 12),wrap="word")        
        self.note_display.pack(fill="both", expand=True, padx=10, pady=10)
        
                    
        # Show ListBox
        self.notes_logic.add_note_to_list()
        
        # Contributor Label + Combobox
        tk.Label(self.enter_notes_frame,text="Contributor:",**self.factory.label_opts).grid(row=0, column=0,sticky="w",padx=(20, 5), pady=(20, 5))
        self.note_contributor = ttk.Combobox(self.enter_notes_frame,**self.factory.combo_opts,state="readonly")
        
        contributors = self.notes_logic.load_contributor_list()
        contributors = sorted(set(contributors), key=lambda x: x.lower())  # Sort case-insensitively and remove exact duplicates

        # Move 'admin' (any casing) to top if present
        admin_username = next((user for user in contributors if user.lower() == "admin"), None)

        if admin_username:
            contributors.remove(admin_username)
            contributors.insert(0, admin_username)
            self.note_contributor.set(admin_username)
        else:
            # If 'admin' not found at all, insert default manually
            contributors.insert(0, "admin")
            self.note_contributor.set("admin")

        self.note_contributor["values"] = contributors
        self.note_contributor.grid(row=0, column=1, sticky="ew", padx=(5, 20), pady=(20, 5), ipady=3)

    
        # Subject Label + Entry
        tk.Label(self.enter_notes_frame,text="Subject:",**self.factory.label_opts).grid(row=1, column=0,sticky="w",padx=(20, 5), pady=(10, 5))

        self.subject_ent = tk.Entry(self.enter_notes_frame,**self.factory.entry_opts)
        self.subject_ent.grid(row=1, column=1,sticky="ew",padx=(5, 20), pady=(10, 5),ipady=5)

        # Note Label + Text + Scrollbar
        tk.Label(self.enter_notes_frame,text="Note:",**self.factory.label_opts).grid(row=2, column=0,sticky="nw",padx=(20, 5), pady=(10, 5))

        # Create a container frame so the Text and its scrollbar sit neatly together
        notes_container = tk.Frame(self.enter_notes_frame,bg="#ffffff", bd=2,relief="ridge")
        notes_container.grid(row=2, column=1, sticky="nsew", padx=(5, 20), pady=(10, 20))

        # Ensure the parent row/column will expand
        self.enter_notes_frame.grid_rowconfigure(2, weight=1)
        self.enter_notes_frame.grid_columnconfigure(1, weight=1)

        # Vertical Scrollbar
        notes_scroll = tk.Scrollbar(notes_container,orient="vertical")
        notes_scroll.pack(side="right", fill="y", pady=(5, 5), padx=(0, 5))

        # Text widget
        self.notes_text = tk.Text(notes_container,**self.factory.text_opts,yscrollcommand=notes_scroll.set)
        self.notes_text.pack(fill="both",expand=True,padx=(5, 0), pady=(5, 5))
        notes_scroll.config(command=self.notes_text.yview)

        # (Optional) placeholder text
        self.notes_text.insert("1.0", "Type your notes here...")
        self.notes_text.focus_set()
        
        # ============= Menu Buttons ==============
        
        # Save Note Button
        self.save_btn = tk.Button(self.notes_action_menu, text="Save Note", command=self.notes_logic.save_note, **self.factory.button_opts)
        self.save_btn .grid(row=0, column=0, padx=2, pady=10)
        #  Note Button
        self.update_btn = tk.Button(self.notes_action_menu, text="Update Note", command=self.notes_logic.update_note, **self.factory.button_opts)
        self.update_btn.config(state=tk.DISABLED)
        self.update_btn .grid(row=0, column=1, padx=2, pady=10)
        # Delete Note Button
        self.delete_btn = tk.Button(self.notes_action_menu, text="Delete Note", command=self.notes_logic.delete_note,  **self.factory.button_opts)
        self.delete_btn.config(state=tk.DISABLED)
        self.delete_btn .grid(row=0, column=3, padx=2, pady=10)
        
        # ===== Search Note ======
        
        # "By" Label
        tk.Label(self.notes_search_menu, text="By", font=("Helvetica", 11)).grid(row=0, column=0, padx=(4, 2), pady=5, sticky="w")
        # Dropdown menu - search
        self.combo_search_opts = ttk.Combobox(self.notes_search_menu, font=("Helvetica", 11), width=15, style="TCombobox")
        self.combo_search_opts["values"] = ("Contributor", "Subject", "Date Created", "Month Created", "Keyword", "Transaction ID")
        self.combo_search_opts.set("Contributor")
        self.combo_search_opts.grid(row=0, column=1, padx=5, pady=5, ipady=2)
        
        # Search Entry
        self.search_note_ent = tk.Entry(self.notes_search_menu,**self.factory.entry_opts)
        self.search_note_ent.grid(row=0, column=2,sticky="ew",padx=(4, 20), pady=(10, 5),ipady=5)     
        
        # Search Button
        self.search_btn = tk.Button(self.notes_search_menu, text="Search Notes", command=self.notes_logic.search_note, **self.factory.button_opts)
        self.search_btn .grid(row=0, column=3, padx=2, pady=10)
        
        self.bind_events()
        
    
    def bind_events(self):
        self.notes_listbox.bind("<<TreeviewSelect>>", self.notes_logic.on_note_selected)
        self.notes_text.bind("<FocusIn>", self.notes_logic.clear_placeholder)
        
        
    
class Notes:
    
    def __init__(self, factory):
        self.factory = factory
        self.notes_frame = None
        # Create notes table if needed
        self.create_notes_table()
        
        
    def set_notes_frame(self, notes_frame):
        """Link the UI frame so we can read/write widgets."""
        self.notes_frame = notes_frame 
        
        
    def load_contributor_list(self):
        try:
            with DatabaseManager.with_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT  username FROM users")
                users = [row[0] for row in cursor.fetchall()]
                return users
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Failed to load contributors: {e}")
            return []        
        
        
    def get_note_contributor_id(self, contributor):
        """ Retrieves note contributor id when contributor username is selected """
        try:
            with DatabaseManager.with_connection() as conn: # with closes db connection automatically when job done
                cursor = conn.cursor()
                cursor.execute("SELECT id FROM users WHERE LOWER(username) = LOWER(?)", (contributor,))
                row = cursor.fetchone()

            if row: # if data returned
                return row[0]  # Returns the id
            else:
                messagebox.showerror("Database Error", "User not found.")
                return None  # Return None for both if no data found
            
        except Exception as e:
            messagebox.showerror("Database Error", str(e))
            return None  # Return None for both if error occurs
        
        
    def create_notes_table(self):
        # Create DB if it doesn't exist
        try:
            with DatabaseManager.with_connection() as conn:
                cursor = conn.cursor()
                
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS notes (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        subject TEXT NOT NULL,
                        date_time_entered TEXT,
                        content TEXT NOT NULL,
                        user_id INTEGER,
                        FOREIGN KEY (user_id) REFERENCES users(id)
                    )
                """)
                
                conn.commit()
                #messagebox.showinfo("Success", "Notes table created successfully.")
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Failed to create notes: {e}")
            
                
    def save_note(self):
        # Get contributor
        note_contributor = self.notes_frame.note_contributor.get()
        if not note_contributor:
            note_contributor = "Admin"

        contributor_id = self.get_note_contributor_id(note_contributor)
        subject = self.notes_frame.subject_ent.get().strip()
        note_content = self.notes_frame.notes_text.get("1.0", "end-1c").strip()
        submitted_date_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # checks if subject and note_content are non-empty before trying to save        
        if not subject:
            messagebox.showerror("Input Error", "Subject cannot be empty.")
            return
        if not note_content:
            messagebox.showerror("Input Error", "Note content cannot be empty.")
            return

        # save notes to the database
        try:
            with DatabaseManager.with_connection() as conn:
                cursor = conn.cursor()

                # Check for duplicate subject
                cursor.execute("SELECT COUNT(*) FROM notes WHERE subject = ?", (subject,))
                existing = cursor.fetchone()[0]
                if existing > 0:
                    messagebox.showwarning("Duplicate Subject", "A note with this subject already exists.")
                    return  # Stop saving

                # Save note
                cursor.execute(
                    "INSERT INTO notes(subject, date_time_entered, content, user_id) VALUES(?, ?, ?, ?)",
                    (subject, submitted_date_time, note_content, contributor_id)
                )
                conn.commit()
                self.add_note_to_list()
                self.notes_frame.update_btn.config(state=tk.DISABLED)
                self.notes_frame.delete_btn.config(state=tk.DISABLED)
                
                # clear fields
                self.clear_fields()
                

        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Failed to save notes: {e}")

    
    def add_note_to_list(self):
        try:
            with DatabaseManager.with_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT notes.id, notes.subject, users.username, notes.date_time_entered
                    FROM notes
                    LEFT JOIN users ON notes.user_id = users.id
                    ORDER BY notes.date_time_entered ASC
                """)
                rows = cursor.fetchall()

                # Clear old entries
                for row in self.notes_frame.notes_listbox.get_children():
                    self.notes_frame.notes_listbox.delete(row)

                if rows:
                    for id, subject, username, date_time in rows:
                        username = username if username else "Unknown"
                        self.notes_frame.notes_listbox.insert("", "end", values=(id,subject, username, date_time))
                else:
                    self.notes_frame.notes_listbox.insert("", "end", values=("No notes", "", ""))
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Failed to fetch notes: {e}")
            
    
    def on_note_selected(self, event):
        try:
            selected = self.notes_frame.notes_listbox.focus()
            if not selected:
                return

            row = self.notes_frame.notes_listbox.item(selected)["values"]
            if not row or len(row) < 1:
                return

            note_id = row[0]

            with DatabaseManager.with_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT notes.subject, notes.date_time_entered, notes.content,
                        users.username
                    FROM notes
                    LEFT JOIN users ON notes.user_id = users.id
                    WHERE notes.id = ?
                """, (note_id,))
                note_data = cursor.fetchone()

            if note_data:
                subject, date_time, content, username = note_data
                contributor = username if username else "Unknown"

                # Populate subject and content fields
                self.notes_frame.subject_ent.delete(0, tk.END)
                self.notes_frame.subject_ent.insert(0, subject)

                self.notes_frame.notes_text.delete("1.0", tk.END)
                self.notes_frame.notes_text.insert("1.0", content)

                # Detailed display
                formatted_output = (
                    f"Contributor: {contributor}\t\tSubject: {subject}\t\t"
                    f"Date/Time: {date_time}\n\n"
                    f"{content}"
                )
                self.notes_frame.note_display.delete("1.0", tk.END)
                self.notes_frame.note_display.insert("1.0", formatted_output)

                # Enable action buttons
                self.notes_frame.update_btn.config(state=tk.NORMAL)
                self.notes_frame.delete_btn.config(state=tk.NORMAL)
            else:
                self.notes_frame.note_display.delete("1.0", tk.END)
                self.notes_frame.note_display.insert("1.0", "Note not found.")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to load note: {e}")
    
    def update_note(self):
        # Get the selected note ID
        selected_item = self.notes_frame.notes_listbox.focus()
        if not selected_item:
            messagebox.showerror("Selection Error", "Please select a note to update.")
            return

        note_id = self.notes_frame.notes_listbox.item(selected_item)["values"][0]

        # Collect updated field values
        contributor = self.notes_frame.note_contributor.get()
        subject = self.notes_frame.subject_ent.get()
        note = self.notes_frame.notes_text.get("1.0", "end-1c")
        contributor_id = self.get_note_contributor_id(contributor)

        try:
            with DatabaseManager.with_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    UPDATE notes
                    SET subject = ?, content = ?, user_id = ?
                    WHERE id = ?
                """, (subject, note, contributor_id, note_id))
                conn.commit()
                messagebox.showinfo("Success", "Note updated successfully.")
                self.add_note_to_list()
                # Disable update and delete buttons
                self.notes_frame.update_btn.config(state=tk.DISABLED)
                self.notes_frame.delete_btn.config(state=tk.DISABLED)
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Failed to update note: {e}")

        
    def delete_note(self):
        # Get the selected note ID
        selected_item = self.notes_frame.notes_listbox.focus()
        if not selected_item:
            messagebox.showerror("Selection Error", "Please select a note to delete.")
            return

        values = self.notes_frame.notes_listbox.item(selected_item)["values"]
        if not values or len(values) < 1:
            messagebox.showerror("Data Error", "Invalid note selected.")
            return

        note_id = values[0]  # First column is assumed to be the note ID
        
        # Confirm delete
        confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete note ID {note_id}?")
        if not confirm:
            return

        try:
            with DatabaseManager.with_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM notes WHERE id = ?", (note_id,))
                conn.commit()
                messagebox.showinfo("Success", f"Note ID {note_id} has been deleted.")
                self.add_note_to_list()  # Refresh list after deletion
                
                # Disable update and delete buttons
                self.notes_frame.update_btn.config(state=tk.DISABLED)
                self.notes_frame.delete_btn.config(state=tk.DISABLED)
                
                self.clear_fields()
                
        except Exception as e:
            messagebox.showerror("Database Error", str(e))
            
            
    def clear_placeholder(self,event):
        if self.notes_frame.notes_text.get("1.0", "end-1c").strip() == "Type your notes here...":
            self.notes_frame.notes_text.delete("1.0", "end")
            
    def clear_fields(self):
        # Clear fields and set default in TEXT
        self.notes_frame.subject_ent.delete(0, tk.END)
        self.notes_frame.notes_text.delete("1.0", "end")
        self.notes_frame.notes_text.insert("1.0", "Type your notes here...")
        self.notes_frame.notes_text.focus_set()                 
        # Clear display text
        self.notes_frame.note_display.delete("1.0", "end")
            
            
    def search_note(self):
        search_type = self.notes_frame.combo_search_opts.get().strip()
        search_term = self.notes_frame.search_note_ent.get().strip()

        if not search_type or not search_term:
            messagebox.showwarning("Search Error", "Please select a search type and enter a keyword.")
            return

        try:
            query, params = self.get_search_query(search_type, search_term)
        except ValueError as ve:
            messagebox.showerror("Input Error", str(ve))
            return

        try:
            with DatabaseManager.with_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(query, params)
                rows = cursor.fetchall()

                self.notes_frame.notes_listbox.delete(*self.notes_frame.notes_listbox.get_children())

                if rows:
                    for id, subject, username, date_time in rows:
                        username = username if username else "Unknown"
                        self.notes_frame.notes_listbox.insert("", "end", values=(id, subject, username, date_time))
                else:
                    messagebox.showinfo("No Results", "No notes found matching your search.")

        except Exception as e:
            messagebox.showerror("Database Error", f"Search failed: {e}")
            
    
    def get_search_query(self, search_type, search_term):
        base_query = """
            SELECT notes.id, notes.subject, users.username, notes.date_time_entered
            FROM notes
            LEFT JOIN users ON notes.user_id = users.id
            WHERE
        """

        if search_type == "Contributor":
            return base_query + " users.username LIKE ?", (f"%{search_term}%",)

        elif search_type == "Subject":
            return base_query + " notes.subject LIKE ?", (f"%{search_term}%",)

        elif search_type == "Date Created":
            return base_query + " DATE(notes.date_time_entered) = ?", (search_term,)

        elif search_type == "Month Created":
            return base_query + " strftime('%Y-%m', notes.date_time_entered) = ?", (search_term,)

        elif search_type == "Keyword":
            return base_query + " notes.content LIKE ?", (f"%{search_term}%",)

        elif search_type == "Transaction ID":
            if not search_term.isdigit():
                raise ValueError("Transaction ID must be a number.")
            return base_query + " notes.id = ?", (int(search_term),)

        else:
            raise ValueError("Invalid search type selected.")
        
    