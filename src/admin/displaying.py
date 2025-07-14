from db.db_manager import DatabaseManager
import tkinter as tk
from tkinter import messagebox

class Displaying:    
    
    def __init__(self, factory):
        self.factory = factory
                
    
    def get_cursor(self, event):
        try:
            cursor_row = self.factory.notes_listbox.focus()
            if not cursor_row:
                return

            # Get row values: [subject, contributor, date_time]
            row = self.factory.notes_listbox.item(cursor_row)["values"]
            if not row or len(row) < 3:
                return

            note_id = row[0]
            
            with DatabaseManager.with_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                        SELECT notes.subject, notes.date_time_entered, notes.content, users.username
                        FROM notes
                        LEFT JOIN users ON notes.user_id = users.id
                        WHERE notes.id = ?
                    """, (note_id,))

            
                note_data = cursor.fetchone()

            if note_data:
                note_subject, note_date_time, note_content, note_username = note_data
                formatted_output = (
                    f"Contributor: {note_username}\t\t\t    Subject: {note_subject}\t\t\t         Date/Time: {note_date_time}\n\n"
                    f"{note_content}"
                )
                self.factory.note_display.delete("1.0", "end")
                self.factory.note_display.insert("1.0", formatted_output)
                
                # populate 
                self.factory.subject_ent.delete(0, tk.END)
                self.factory.subject_ent.insert(0, note_subject)
                
                self.factory.notes_text.delete("1.0", tk.END)
                self.factory.notes_text.insert("1.0", note_content)
                
                # Enable Update Note and Delete Note Buttons
                self.factory.update_btn.config(state=tk.NORMAL)
                self.factory.delete_btn.config(state=tk.NORMAL)
                
            else:
                self.factory.note_display.delete("1.0", "end")
                self.factory.note_display.insert("1.0", "Note not found.")
        except Exception as e:
            messagebox.showerror("Error", f"Could not display note: {e}")