"""" DELTA """
# Your updated Delta class looks clean, modular, and logically structured.
# You're now correctly using: 
# Local imports to avoid circular import issues.
# A self-contained factory pattern via self.factory.
# Good encapsulation of UI widget creation and display logic.
        
# Your Delta class looks solid and well-structured! Here’s a quick recap and a few tips to keep it smooth and maintainable:

# What’s good:
# Local imports inside methods (from .displaying import Displaying) — great to avoid circular import issues.

# WidgetFactory usage: You instantiate it once (self.factory) and then call methods on that instance, which keeps your UI logic nicely encapsulated.

# Clean method create_widgets: Separates widget setup, data display, and event binding logically.

# Proper use of self.pack(): So the frame shows itself.

# Optional enhancements or reminders:
# Consider separation of concerns:
# If Delta grows too large, you could move more logic into your WidgetFactory or another controller class, keeping Delta as a simple view/container.

# Error handling and robustness:
# If any factory methods might fail, consider try/except blocks or validations to catch issues early.

# Comments and docstrings:
# You have a good docstring for the class; consider adding short comments in create_widgets to explain each step briefly if others will read your code.

# Responsiveness:
# Since you use full screen size, consider how your widgets behave on resize or different resolutions—do they scale or stick nicely?


""" WidgetFactory """

# Your code for the WidgetFactory class is well-structured, modular, and thoughtfully designed for scalability. You're clearly applying separation of concerns through helper classes (Saving, Displaying, etc.), which is excellent for maintainability.

# Here’s a comprehensive code review, including praise, suggestions, and minor improvements:

# ✅ Strengths
# Modular Architecture
# The separation into Saving, Displaying, Clearing, etc., follows the Single Responsibility Principle very well. It keeps your main UI logic clean.

# Consistent Styling
# Your use of self.label_opts, self.entry_opts, etc., makes the code more maintainable and easily themeable.

# Widget Grouping
# Frames and group boxes (LabelFrame) help keep the UI visually and structurally organized.

# Scrollbars & Treeview Integration
# You correctly wired both X and Y scrollbars to the Treeview, ensuring usability for large datasets.

# Use of Callbacks
# The use of show_admin_callback, etc., makes this class reusable across contexts.

# Database Handling
# Excellent use of context manager (with) in get_selected_country_id() to manage DB connections.

# 🔍 Suggestions for Improvement
# 1. Encapsulate Style Configuration
# Move styles into a setup_style_dicts() method or even a separate style.py module. This would make it easier to adjust UI themes in one place.

# 2. Widget Identifiers
# Naming widgets like self.sender_build_door_no_ent is descriptive but long. You might consider:


# self.sender_door_ent
# self.sender_street_ent
# to improve readability without losing clarity.

# 3. Reduce Repetition in Entry Fields
# The multiple Entry() widgets could be generated with a loop and a data structure like:


# sender_fields = [
#     ("First Name", 0, 0),
#     ("Last Name", 0, 2),
#     ...
# ]
# and loop through them to create widgets. This would reduce lines by 50%+.

# 4. Magic Numbers
# Constants like .place(x=990, y=70, ...) would benefit from symbolic constants (RECEIPT_X = 990) for easier future refactoring and layout changes.

# 5. Error Handling Granularity
# In get_selected_country_id(), if you get None, you show a messagebox.showerror(). Consider having the caller decide whether to show a dialog or fail silently/log instead.

# 6. Button State Control
# Since you're disabling/enabling buttons (self.btn_save.config(state=DISABLED)), consider creating a helper method like:

# python
# Copy
# Edit
# def set_button_state(self, button, state):
#     button.config(state=state)
# 7. Responsive Layout Consideration
# Consider transitioning to .grid() or .pack() for outermost frames instead of .place(), which doesn’t scale well with window resizing. If the screen size changes, .place() can be brittle.

# 🧪 Future Enhancements
# Tooltips: Add tooltips using ttk.Tooltip or a custom implementation to explain what each entry/button does.

# Field Validation: Include validation on email, mobile number, and weight fields using validatecommand or external validators.

# Keyboard Navigation: Consider enabling keyboard-based navigation between fields for accessibility.

# Theming: Allow toggling between light/dark themes with a settings toggle.

# Form Reset/Prefill Logic: You could abstract logic into populate_fields(data: dict) and reset_fields() methods for DRYness.

# 🧼 Minor Cleanups
# Remove unused imports like textwrap if not used.

# There’s a comment with #lbltitle.pack(side=TOP, fill=X)—clean up if it’s legacy/test code.

# You're using ipady = 3 repeatedly; consider including it in entry_opts to DRY up the code further.

# 📊 Summary
# Category	Rating
# Code Structure	⭐⭐⭐⭐⭐
# UI Design Practices	⭐⭐⭐⭐☆
# Maintainability	⭐⭐⭐⭐⭐
# Future Scalability	⭐⭐⭐⭐☆
# Code Redundancy	🚨 Needs some DRY cleanup


""" Saving """
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


""" Updating """
# Your Updating class is well-structured and performs several essential tasks robustly — form validation, database update, data integrity checks, and UI feedback. Below is a comprehensive review with praise, potential issues, and suggestions for improvements:

# ✅ Strengths
# Clear Method Responsibilities: Each method has a specific job (update_data, get_selected_country_id, validate_goods_status).

# Good Error Handling: You catch exceptions and show appropriate messagebox messages.

# Use of Context Managers: The use of with DatabaseManager.with_connection() ensures clean database handling.

# Field Validation: You’re validating critical inputs like required fields and numeric weight.

# UI Integration: The interaction with the Treeview and input widgets is tight and well-thought out.

# Status Transition Logic: validate_goods_status() is a valuable safeguard against illogical state transitions.

# ⚠️ Potential Issues & Improvements
# 1. Missing Initialization for self.shipped_date
# Issue: If status != "Shipped - In transit", then self.shipped_date is never initialized, but it is used in the SQL statement:


# date_shipped=?, ...
# This could raise an AttributeError.

# Fix: Set a default value:


# self.shipped_date = ""  # default
# if status == "Shipped - In transit":
#     self.shipped_date = datetime.datetime.now().strftime('%d-%m-%Y')
# 2. Numeric Weight Validation Could Be Tighter
# Issue: You're checking isinstance(weight, str) and weight.strip() but converting without catching float() conversion errors early.

# Fix: Wrap the float() conversion directly:


# try:
#     weight_float = float(weight)
# except ValueError:
#     messagebox.showerror("Input Error", "Weight must be a valid number.")
#     return
# 3. Return Behavior of validate_goods_status()
# Issue: It shows an error but does not stop the flow in update_data().

# Fix: Return a boolean indicating success or failure:


# def validate_goods_status(...):
#     ...
#     return False  # on invalid
#     ...
#     return True
# Then use:


# if not self.validate_goods_status(transaction_id, status):
#     return
# 4. Weight Stored as String in Database?
# You pass the original weight (string) to the database, not weight_float:


# total_weight=?, ...
# ...
# goods_type, weight, self.shipped_date, estimated_cost, ...
# Fix:


# goods_type, weight_float, self.shipped_date, estimated_cost, ...
# 5. Code Organization: Consider Splitting Status Logic
# The logic for status == "Shipped - In transit" and other transitions might be better off extracted into a separate method or class to enhance readability/testability.

# 6. Treeview Row Validation
# Your row index assumption row[1] for transaction_id can be risky if the columns are ever reordered.

# Suggestion: Consider assigning column IDs and accessing via column names if possible, or make the column index a constant.

# 7. Better Handling of Disabled Buttons
# After updating:


# self.factory.btn_save.config(state=DISABLED)
# But if this button is shared for both Save and Update, this may confuse users unless it’s clearly labeled or re-enabled when appropriate.

# 🧽 Minor Cleanups
# self.transaction_id = transaction_id isn't used later — can be removed unless intentionally reused elsewhere.

# Your return None, None in get_selected_country_id() is always safe, but might benefit from a comment warning developers to check result unpacking when used.

# ✅ Summary of Suggested Fixes
# Location	Change
# self.shipped_date usage	Set a default value before conditional assignment
# Weight conversion	Wrap float(weight) in a try/except for better robustness
# validate_goods_status()	Return True/False and use in update_data() for better control
# SQL binding for weight	Use weight_float not weight
# Button state logic	Ensure the disabled state doesn't block further updates unnecessarily

""" Displaying """
# Your Displaying class looks solid and well-structured for managing the display and selection of shipment data in the Tkinter Treeview. Below is a detailed review with observations, suggestions, and a couple of minor fixes to help you improve the code clarity and robustness.

# ✅ What works well:
# Data loading and display:
# The display_data() method fetches data from the database and populates the Treeview cleanly, clearing previous data first.

# Event binding:
# You neatly encapsulate the binding in bind_display_event().

# Cursor selection handling:
# The get_cursor() method extracts the clicked row data and populates the form fields accordingly, including splitting the full name.

# Database joins:
# The query in get_cursor() efficiently fetches related address data in a single query.

# Error handling:
# Use of try-except blocks with messagebox error reporting.

# ⚠️ Suggestions & minor fixes:
# 1. Fix exception type in load_country_list
# Current code:


# except DatabaseManager.with_connection().Error as e:
# This is incorrect syntax. You can’t do DatabaseManager.with_connection().Error.

# Instead, catch a general exception or the specific database exception type from your DB library (e.g., sqlite3.Error or just Exception):


# except Exception as e:
#     messagebox.showerror("Database Error", f"Failed to load countries: {e}")
#     return []
# 2. Be explicit on columns for insert()
# You do:


# self.factory.global_table.insert("", END, values=(i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[8], i[9], i[10]))
# This is fine, but consider defining the column names or constants to improve maintainability and readability. For example:


# columns = ("id", "transaction_id", "created_at", "full_name", "mobile", "email", "type_of_goods",
#            "total_weight", "date_shipped", "total_cost", "status_of_goods")

# self.factory.global_table.insert("", END, values=tuple(i[column_index] for column_index in range(len(columns))))
# 3. Check row length and content in get_cursor
# If the user clicks on an empty part of the Treeview or no row is selected, row can be empty or invalid.

# Add a guard:


# if not row:
#     return
# 4. Name splitting edge cases
# Splitting full names into first and last name assumes two parts only. Consider:


# if len(name_parts) >= 2:
#     self.factory.fname_ent.insert(0, name_parts[0])
#     self.factory.lname_ent.delete(0, END)
#     self.factory.lname_ent.insert(0, " ".join(name_parts[1:]))
# else:
#     self.factory.fname_ent.insert(0, full_name)
#     self.factory.lname_ent.delete(0, END)
# This way, multi-part last names (e.g. "Mary Anne Smith") are handled gracefully.

# 5. Consistent use of END
# You're using END correctly for deleting and inserting, good!

# 6. Cursor management
# The focus could be changed before the get_cursor fires, so double-check the focused row exists.

# 7. Avoid SQL join using implicit join syntax
# You have:


# FROM shipments, country_price WHERE shipments.id=? AND country_price.id == shipments.country_price_id
# Prefer explicit JOIN for clarity:


# FROM shipments
# JOIN country_price ON country_price.id = shipments.country_price_id
# WHERE shipments.id=?
# Optional refactor snippet for get_cursor():
# python
# Copy
# Edit
# def get_cursor(self, event=""):
#     from .receipt import Receipt
#     receipt = Receipt(self.factory)

#     cursor_row = self.factory.global_table.focus()
#     if not cursor_row:
#         return

#     content = self.factory.global_table.item(cursor_row)
#     row = content.get("values", [])
#     if not row:
#         return

#     # Split full name safely
#     full_name = row[3]
#     name_parts = full_name.split()
#     self.factory.fname_ent.delete(0, END)
#     self.factory.lname_ent.delete(0, END)
#     if len(name_parts) >= 2:
#         self.factory.fname_ent.insert(0, name_parts[0])
#         self.factory.lname_ent.insert(0, " ".join(name_parts[1:]))
#     else:
#         self.factory.fname_ent.insert(0, full_name)

#     # Populate other fields
#     self.factory.mobile_ent.delete(0, END)
#     self.factory.mobile_ent.insert(0, row[4])

#     self.factory.email_ent.delete(0, END)
#     self.factory.email_ent.insert(0, row[5])

#     self.factory.type_of_goods.set(row[6])

#     self.factory.total_weight_ent.delete(0, END)
#     self.factory.total_weight_ent.insert(0, row[7])

#     self.factory.estimated_cost = row[9]

#     self.factory.status_of_goods.set(row[10])

#     shipment_id = row[0]

#     try:
#         with DatabaseManager.with_connection() as conn:
#             cursor = conn.cursor()
#             cursor.execute(
#                 """SELECT sender_build_door_no, sender_street_road, sender_city_town, sender_postcode,
#                           dest_receiver_title_fullname, dest_first_line_of_address, dest_city_town, dest_mobile,
#                           transaction_id, created_at, country_price.country
#                    FROM shipments
#                    JOIN country_price ON country_price.id = shipments.country_price_id
#                    WHERE shipments.id=?""", (shipment_id,))
#             address_data = cursor.fetchone()

#             if address_data:
#                 (sender_build_door_no, sender_street_road, sender_city_town, sender_postcode,
#                  dest_receiver_title_fullname, dest_first_line_of_address, dest_city_town, dest_mobile,
#                  transaction_id, created_at, country) = address_data

#                 self.factory.sender_build_door_no_ent.delete(0, END)
#                 self.factory.sender_build_door_no_ent.insert(0, sender_build_door_no)

#                 self.factory.sender_street_road_ent.delete(0, END)
#                 self.factory.sender_street_road_ent.insert(0, sender_street_road)

#                 self.factory.sender_city_town_ent.delete(0, END)
#                 self.factory.sender_city_town_ent.insert(0, sender_city_town)

#                 self.factory.sender_postcode_ent.delete(0, END)
#                 self.factory.sender_postcode_ent.insert(0, sender_postcode)

#                 self.factory.dest_receiver_title_fullname_ent.delete(0, END)
#                 self.factory.dest_receiver_title_fullname_ent.insert(0, dest_receiver_title_fullname)

#                 self.factory.dest_first_line_of_address_ent.delete(0, END)
#                 self.factory.dest_first_line_of_address_ent.insert(0, dest_first_line_of_address)

#                 self.factory.dest_city_town_ent.delete(0, END)
#                 self.factory.dest_city_town_ent.insert(0, dest_city_town)

#                 self.factory.dest_country.delete(0, END)
#                 self.factory.dest_country.insert(0, country if country else "Unknown")

#                 self.factory.dest_mobile_ent.delete(0, END)
#                 self.factory.dest_mobile_ent.insert(0, dest_mobile)

#                 receipt.produce_receipt(transaction_id, created_at)

#                 self.factory.btn_update.config(state=NORMAL)
#                 self.factory.btn_delete.config(state=NORMAL)

#     except Exception as e:
#         messagebox.showerror("Database Error", f"Error retrieving addresses: {e}")


""" form_data """
# Your FormData class looks clean and straightforward—great job encapsulating the logic to fetch form values in one place! Here are a couple of tips and a small suggestion to make it even more robust and maintainable:

# 1. Add a method to set form values (optional but useful)
# Often when dealing with forms, you might want to populate the form from data (e.g., when editing an existing record). You could add a method like:


# def set_form_values(self, data: dict):
#     """ Populate form widgets with provided data dictionary """
#     self.factory.fname_ent.delete(0, END)
#     self.factory.fname_ent.insert(0, data.get("fname", ""))
    
#     self.factory.lname_ent.delete(0, END)
#     self.factory.lname_ent.insert(0, data.get("lname", ""))
    
#     self.factory.mobile_ent.delete(0, END)
#     self.factory.mobile_ent.insert(0, data.get("mobile", ""))
    
#     self.factory.email_ent.delete(0, END)
#     self.factory.email_ent.insert(0, data.get("email", ""))
    
#     self.factory.sender_build_door_no_ent.delete(0, END)
#     self.factory.sender_build_door_no_ent.insert(0, data.get("sender_build_door_no", ""))
    
#     self.factory.sender_street_road_ent.delete(0, END)
#     self.factory.sender_street_road_ent.insert(0, data.get("sender_street_road", ""))
    
#     self.factory.sender_city_town_ent.delete(0, END)
#     self.factory.sender_city_town_ent.insert(0, data.get("sender_city_town", ""))
    
#     self.factory.sender_postcode_ent.delete(0, END)
#     self.factory.sender_postcode_ent.insert(0, data.get("sender_postcode", ""))
    
#     self.factory.dest_receiver_title_fullname_ent.delete(0, END)
#     self.factory.dest_receiver_title_fullname_ent.insert(0, data.get("dest_receiver_title_fullname", ""))
    
#     self.factory.dest_first_line_of_address_ent.delete(0, END)
#     self.factory.dest_first_line_of_address_ent.insert(0, data.get("dest_first_line_of_address", ""))
    
#     self.factory.dest_city_town_ent.delete(0, END)
#     self.factory.dest_city_town_ent.insert(0, data.get("dest_city_town", ""))
    
#     self.factory.dest_country.delete(0, END)
#     self.factory.dest_country.insert(0, data.get("dest_country", ""))
    
#     self.factory.dest_mobile_ent.delete(0, END)
#     self.factory.dest_mobile_ent.insert(0, data.get("dest_mobile", ""))
    
#     self.factory.type_of_goods.set(data.get("goods_type", ""))
    
#     self.factory.total_weight_ent.delete(0, END)
#     self.factory.total_weight_ent.insert(0, data.get("weight", ""))
    
#     self.factory.status_of_goods.set(data.get("status", ""))
# 2. Add validation hooks (future improvement)
# You might want to add methods for basic validation, e.g., checking required fields, email format, numeric weight, etc., so you can call it before saving.

# 3. Optional: Use a list of fields to reduce repetition
# To reduce boilerplate, you could store widget references and keys in a list/dict, then loop in get_form_values() like:


# def get_form_values(self):
#     fields = {
#         "fname": self.factory.fname_ent,
#         "lname": self.factory.lname_ent,
#         "mobile": self.factory.mobile_ent,
#         # ... etc
#     }
#     return {key: widget.get() for key, widget in fields.items()}
# But your current explicit approach is very clear, which is often better.

""" Receipt """
# Your Receipt class is well structured and does a solid job generating and saving a shipping receipt both in the text widget and as a PDF. Here are some detailed thoughts and a few improvement suggestions:

# What works well:
# Clean, readable receipt formatting using textwrap.dedent.

# Safe conversion of weight to float with exception handling.

# Dynamically fetches country price for cost calculation with a fallback.

# Saves and retrieves transaction info to ensure the PDF can be generated reliably.

# Uses ReportLab to generate a simple but neat PDF with monospaced font.

# User feedback with messagebox on errors and success.

# Suggestions & improvements:
# 1. Improve PDF line wrapping
# Currently, long lines may overflow the page width or get clipped because you draw each line as-is. Consider wrapping long lines when drawing the PDF, similar to how you wrap in the text widget.

# Example for PDF wrapping:

# python
# Copy
# Edit
# from reportlab.lib.utils import simpleSplit

# max_width = 500  # approx width in points for A4 margins
# for line in receipt_text.split('\n'):
#     wrapped_lines = simpleSplit(line, "Courier", 10, max_width)
#     for wrap_line in wrapped_lines:
#         c.drawString(50, y, wrap_line)
#         y -= 15
#         if y < 50:  # start new page if near bottom
#             c.showPage()
#             c.setFont("Courier", 10)
#             y = height - 50
# 2. Parameterize font and spacing
# Define font size and line height as variables for easy tuning.

# python
# Copy
# Edit
# font_name = "Courier"
# font_size = 10
# line_height = font_size + 5
# c.setFont(font_name, font_size)
# Use line_height for y -= line_height.

# 3. Allow user to select save location
# Instead of hardcoding the filename in the current directory, you can prompt the user with a file dialog:

# python
# Copy
# Edit
# from tkinter import filedialog

# filename = filedialog.asksaveasfilename(
#     defaultextension=".pdf",
#     initialfile=f"receipt_{trans_id}.pdf",
#     filetypes=[("PDF Files", "*.pdf")]
# )
# if not filename:
#     return
# This makes the app friendlier for users to choose where to save.

# 4. Add more metadata to PDF
# You can add title, author, creation date metadata to the PDF canvas, e.g.,

# python
# Copy
# Edit
# c.setTitle(f"Receipt {trans_id}")
# c.setAuthor("Global Shipping Ltd")
# 5. Consider adding a PDF header or logo
# If you want to brand your receipt, you can add a logo or header image (if available) to the PDF with ReportLab's drawImage method.

# Minor code cleanup
# In produce_receipt, the estimated_cost variable is both computed and used. You might want to store it as an attribute or pass it explicitly if used elsewhere.

# You might want to .strip() on all .get() calls for consistency.

# Consider refactoring produce_receipt into smaller helper methods if it grows.

# Example snippet with wrapping for PDF saving:
# python
# Copy
# Edit
# from reportlab.lib.utils import simpleSplit

# def save_receipt_as_pdf(self):
#     receipt_text = self.factory.receipt_text.get("1.0", END).strip()
#     if not receipt_text:
#         messagebox.showerror("Error", "No receipt content to save.")
#         return

#     trans_id = getattr(self.factory, 'generated_trans_id', None)
#     date_created = getattr(self.factory, 'generated_date_created', None)
#     if not trans_id or not date_created:
#         messagebox.showerror("Error", "Missing transaction details. Generate receipt first.")
#         return

#     filename = filedialog.asksaveasfilename(
#         defaultextension=".pdf",
#         initialfile=f"receipt_{trans_id}.pdf",
#         filetypes=[("PDF Files", "*.pdf")]
#     )
#     if not filename:
#         return

#     c = canvas.Canvas(filename, pagesize=A4)
#     _, height = A4
#     font_name = "Courier"
#     font_size = 10
#     line_height = font_size + 5
#     c.setFont(font_name, font_size)

#     y = height - 50
#     max_width = 500

#     for line in receipt_text.split('\n'):
#         wrapped_lines = simpleSplit(line, font_name, font_size, max_width)
#         for wrap_line in wrapped_lines:
#             c.drawString(50, y, wrap_line)
#             y -= line_height
#             if y < 50:
#                 c.showPage()
#                 c.setFont(font_name, font_size)
#                 y = height - 50

#     c.save()
#     messagebox.showinfo("PDF Saved", f"Receipt saved as {filename}")

""" searching """
# Your Searching class is quite well-structured and does a good job handling search logic with different field types, including a join for country search. A few notes and suggestions to polish it further:

# Suggestions & Fixes
# Fix binding target in bind_searching_events
# You wrote:


# self.search_ent.bind(key_release_event , self.check_search_entry)
# It should bind the entry widget on self.factory, i.e.:


# self.factory.search_ent.bind(key_release_event, self.check_search_entry)
# Consistent column indexes when inserting search results
# Your insert line uses indexes:


# (row[0], row[1], row[2], row[3], row[4],
#  row[5], row[8], row[9], row[10], row[11], row[12])
# Double-check if these indexes match your shipments table structure or your Treeview columns. For example, index 8,9,10,11,12 could mismatch if your table doesn't have that many columns or if columns have shifted.

# Search by First or Last Name is both full_name
# Right now, your search by "First Name" or "Last Name" both query full_name column with a LIKE %search_text%. That will work but can return false positives if, say, searching "John" in full_name "John Smith". If you want to distinguish first vs last name, you’d need to store them separately or do a split in query (which is complex in SQL). Otherwise, it's fine.

# Case-insensitive search
# SQLite is case-insensitive by default for LIKE, but some other DBs are not. You might want to enforce case-insensitivity explicitly if portability is needed, e.g.:


# WHERE LOWER(full_name) LIKE LOWER(?)
# This is optional.

# Improve the search_by selection validation
# Right now, if search_by is not in search_map or "Country", it errors. You might want to restrict the combobox options strictly to valid values upfront or handle unexpected values gracefully.

# Minor clean-up example:

# def bind_searching_events(self):
#     self.factory.search_ent.bind("<KeyRelease>", self.check_search_entry)

""" Deleting """
# Your Deleting class looks solid and well-structured! It correctly handles:

# Checking selection and data presence,

# Confirming delete with the user,

# Executing a parameterized delete query safely,

# Refreshing the view and clearing inputs,

# Disabling relevant buttons,

# And handling exceptions gracefully.

# A couple of small suggestions:
# Consider adding a check if any rows were actually deleted.
# After cursor.execute("DELETE ..."), you can check cursor.rowcount to confirm that a row was deleted, and inform the user if none was found:


# cursor.execute("DELETE FROM shipments WHERE transaction_id = ?", (transaction_id,))
# if cursor.rowcount == 0:
#     messagebox.showwarning("Warning", f"No record found with Transaction ID {transaction_id}.")
# else:
#     conn.commit()
#     # ... rest of your code ...
# bind_events is called after clearing and refreshing
# This is good if you want to rebind event handlers on widgets, but make sure this method is idempotent or designed to be called multiple times.

# Add docstring to delete_data()
# For clarity and consistency, adding a docstring helps:


# def delete_data(self):
#     """Delete the selected shipment record from the database."""


""" Deleting """
# Your Clearing class is clean and straightforward, doing exactly what it should: clearing all form input fields, resetting dropdowns/selections, clearing the receipt text widget, and disabling some buttons afterward.

# A few quick tips to enhance or keep in mind:
# Consistent Default Values:
# You set default values for status_of_goods and type_of_goods after clearing. Just double-check those defaults ("Collected" and "Perishable") are always valid options in your dropdowns.

# Disable Buttons Wisely:
# Disabling Save and Clear buttons makes sense here, assuming you want to prevent saving empty forms or unnecessary clears. Just confirm your button enabling logic elsewhere enables these buttons again when appropriate.

# Add Docstring to clear_fields method:
# For completeness and maintainability:


# def clear_fields(self):
#     """Clear all form input fields, reset dropdowns, clear receipt, and disable buttons."""
# Exception Safety (optional):
# If any widget is missing or not properly initialized, calling .delete() might throw an error. You could optionally wrap your clear calls in try-except or assert your factory setup guarantees all widgets exist.


""" Admin """
# Your AdminFrame code is clean and modular, showing good separation of concerns by using a WidgetFactory class for UI component generation. Here's a breakdown of feedback, suggestions, and improvements for code structure, maintainability, and functionality:

# ✅ What’s Good
# Modular Design: Offloading widget creation to WidgetFactory helps keep the AdminFrame tidy.

# Use of super().__init__() ensures proper initialization of the tk.Frame.

# Dependency Injection: Passing callbacks (show_login_callback, logout, etc.) to the factory supports testability and flexibility.

# Consistent naming and spacing.

# Expandable layout: self.pack(fill="both", expand=True) is appropriate for a main frame.

# 🛠️ Suggestions for Improvement
# 1. Redundant Imports
# You're importing modules like sqlite3, datetime, and defaultdict but not using them in this snippet.

# Fix:
# Remove them unless they are used in later parts of this file:

# import sqlite3  # Remove if not used
# import datetime  # Remove if not used
# from collections import defaultdict  # Remove if not used
# 2. Missing Docstrings
# Add class and method docstrings for clarity, especially since this is likely part of a larger system.

# Example:


# class AdminFrame(tk.Frame):
#     """Main admin interface frame that integrates sidebar and main content."""

#     def create_widgets(self):
#         """Initializes all widgets on the admin interface using the widget factory."""
# 3. Late Import of WidgetFactory
# Importing WidgetFactory inside __init__ is non-standard and usually discouraged unless you're doing lazy loading or avoiding circular imports.

# Fix (preferred):
# Move it to the top:


# from admin.admin_widget_factory import WidgetFactory
# Justification: Easier debugging and auto-completion, avoids runtime surprises.

# 4. Unused Method
# #self.factory.set_up_styles() is commented out. If it's important for consistent UI theming, consider enabling or removing it.

# 5. Error Handling
# Consider wrapping the widget creation in a try-except block to catch GUI rendering issues, especially if dynamic data or themes are used:


# try:
#     self.factory.create_sidebar()
#     self.factory.create_main_content()
# except Exception as e:
#     messagebox.showerror("UI Error", f"Failed to create admin UI: {str(e)}")
# 📦 Optional Enhancements
# a. Logging
# Add logging for traceability in production environments (instead of just relying on messageboxes for error tracking).

# b. Theme Support or Dark Mode
# If not yet implemented, consider providing a style/theme switch via the factory or ttk.Style() integration.

# c. Factory Validation
# Validate that the WidgetFactory actually builds required components. (Maybe via a validate() or is_ready() method).

# ✅ Cleaned-up Version

# import tkinter as tk
# from tkinter import ttk, messagebox
# from admin.admin_widget_factory import WidgetFactory


# class AdminFrame(tk.Frame):
#     """Main admin interface frame that integrates sidebar and main content."""

#     def __init__(self, master, controller, return_callback):
#         super().__init__(master)
#         self.controller = controller
#         self.master = master
#         self.return_callback = return_callback

#         self.factory = WidgetFactory(
#             master=self,
#             screen_width=controller.screen_width,
#             screen_height=controller.screen_height,
#             show_login_callback=controller.show_login,
#             show_admin_callback=controller.show_admin,
#             show_dashboard=controller.show_delta_dashboard,
#             back_to_delta_frame=controller.show_delta_frame,
#             logout=controller.logout
#         )

#         self.create_widgets()
#         self.pack(fill="both", expand=True)

#     def create_widgets(self):
#         """Initializes all widgets on the admin interface using the widget factory."""
#         try:
#             self.factory.create_sidebar()
#             self.factory.create_main_content()
#         except Exception as e:
#             messagebox.showerror("UI Error", f"Failed to create admin UI: {str(e)}")


""" Admin_widget_factory """

# Your WidgetFactory class is quite comprehensive and modular. It encapsulates the logic of GUI construction and interactions well. Here's a structured review including feedback, improvements, and best practices:

# ✅ Strengths
# Separation of Concerns: Logic for settings, dashboard, notes, etc., is separated into helper classes and frame classes (Notes, NotesFrame, etc.).

# Consistent Naming: Naming is clear and aligns well with functionality.

# Factory Design Pattern: You're applying a clean factory pattern for building GUI widgets dynamically.

# Reusability: The way each section is handled makes the code easier to maintain and extend.

# UI/UX Considerations: You used pack_propagate(False) in the sidebar and a clear_content() utility method to manage the display area, which is smart UI handling.

# 🛠️ Suggested Improvements
# 1. Remove Unused Imports
# You're importing several unused modules:


# import sqlite3
# import datetime
# from collections import defaultdict
# ✅ Remove them unless you plan to use them later.

# 2. logout Method Is Incomplete

# def logout(self):
#     from admin.navigation import Navigation        
#     #Navigation.logout()
# ✅ Either implement the method or remove the comment. Consider directly calling a passed-in callback, which is already available:


# def logout(self):
#     self.logout()
# Or, if Navigation.logout() is essential:


# def logout(self):
#     from admin.navigation import Navigation        
#     Navigation().logout()
# 3. Redundant notes_logic Storage
# You're both calling set_notes_frame(...) and assigning self.notes = self.notes_logic. This may not be necessary:


# self.notes = self.notes_logic
# ✅ Consider removing this line if it's unused elsewhere.

# 4. Button Styling in Sidebar
# All sidebar buttons are styled identically and don't respond to hover/active states. You can improve this with a loop like:


# for text, command in buttons:
#     btn = tk.Button(
#         self.sidebar,
#         text=text,
#         command=command,
#         bg="#003366",
#         fg="white",
#         font=("Arial", 12),
#         relief="flat",
#         activebackground="#005580",
#         activeforeground="white",
#         cursor="hand2"
#     )
#     btn.pack(fill="x", pady=2)
# 5. Avoid Duplicate Object Creation
# In set_up_dashboard():


# dashboard_logic = Dashboard(self)
# You're creating a new Dashboard instance every time this method is called, even though you already created one in __init__.

# ✅ Better: use the already stored instance:


# dashboard_frame = DashboardFrame(self.content, self.dashboard)
# 6. Add Docstrings
# Adding docstrings will make this much easier for future developers (or yourself).

# Example:


# def set_up_notes(self):
#     """Initializes and displays the notes interface within the admin panel."""
# 🧹 Minor Cleanups
# a. Organize Imports
# Sort them by standard, third-party, and local modules:


# import tkinter as tk
# from tkinter import ttk, messagebox

# # Third-party
# # from matplotlib... (if needed)

# # Local
# from db.db_manager import DatabaseManager
# from .dashboard import Dashboard, DashboardFrame
# # ...
# b. Comment Clarity
# Some comments are redundant or outdated, e.g.:


# # ← move here
# ✅ Clean these up to maintain clarity.

# ✨ Optional Enhancements
# Dynamic Theme Support: Allow switching between light/dark themes by integrating ttk.Style() usage.

# Tooltips on Buttons: Enhance usability by using a tooltip function/class.

# Sidebar Toggle: Let users collapse/expand the sidebar to maximize screen space.

# ✅ Final Thoughts
# You're doing a lot right here — the structure, modularity, and use of helper logic are all solid. A few tweaks to cleanup unused imports, consolidate logic reuse, and polish incomplete methods will take it to the next level.

# If you'd like, I can help you write unit tests for WidgetFactory, improve sidebar responsiveness, or implement role-based visibility in the admin UI.

"""" Settings """

# Thanks for sharing your full SettingsFrame and Setting classes. The structure looks solid, and the use of composition (settings_logic, factory) 
# is clean and maintainable.

# Minor Fixes & Suggestions:
# Edit User - Clear Authenticated Username

# After update_user, consider clearing self.authenticated_username to avoid unintended reuse:


# self.authenticated_username = None
# Add User - Check for Duplicates

# Prevent duplicates:


# cursor.execute("SELECT 1 FROM users WHERE username = ?", (username,))
# if cursor.fetchone():
#     messagebox.showinfo("Error", "Username already exists.")
#     return
# Fix edit_frame Destruction

# In update_user, self.factory.edit_frame.destroy() will raise an error. It should be:


# if hasattr(self.settings_frame, 'edit_frame'):
#     self.settings_frame.edit_frame.destroy()
# Type of Good Button - Missing Logic

# Add a placeholder or comment for type_of_good_add_btn since it's not wired to any logic:


# # TODO: Implement add_type_of_good functionality
# Use Constants or Enums for Section Identifiers

# If sections are referenced dynamically (section argument passed into methods), using descriptive constants may improve readability and reduce confusion.

# If you'd like, I can also help:

# Refactor the class into smaller mixins or handlers for each section (e.g., user management, price management).

# Write unit tests for Setting methods using unittest.mock and a test database.

# Add "Delete User" or "Reset Password" functionalities.

""" Report """
# Your implementation of the ReportFrame and Report classes looks well-structured and clearly separated in terms of UI and logic, which is excellent for maintainability. Here are a few observations and potential suggestions to improve robustness and clarity:

# ✅ Strengths:
# Separation of Concerns: GUI rendering (ReportFrame) and data processing (Report) are cleanly separated.

# Use of Tags for Styling: Alternating row colors improve readability.

# Treeview Height Limiting: Smart UI design with scrollbars for overflow.

# Error Handling: Exception blocks for database operations are present.

# Summary Calculations: The shipment summary table goes beyond raw data and adds analytical insight.

# 🔍 Suggestions for Improvement:
# 1. Avoid Repeating Style Configuration
# The Treeview styling (ttk.Style()) is repeated in sections 0 and 1. Consider initializing styles once (possibly in __init__) to avoid redundancy.

# 2. Clear Treeviews Before Inserting
# If create_report is called multiple times, the Treeviews will accumulate duplicate entries unless you clear them first:


# self.tree_shipping_rates.delete(*self.tree_shipping_rates.get_children())
# Do this before inserting rows in all relevant sections.

# 3. Scroll Bar Issue in Top Countries
# You're using tree_scroll in the top countries section, but it was defined in the shipping rates section. This might cause UI issues or even errors. Define a separate scrollbar for each Treeview or reuse it correctly.

# 4. Guard Against NoneType in Revenue Calculation
# You handle None with or 0, but for better readability:


# total_revenue = revenue_data[0] if revenue_data[0] is not None else 0
# total_shipments = revenue_data[1] if revenue_data[1] is not None else 0
# 5. Standardize Status Normalization
# Instead of repeating normalization logic:


# normalized = status.strip().lower()
# Consider adding a helper function:


# def normalize_status(status):
#     return status.strip().lower()
# 6. Minor: Typo Fix
# shippment_status_frame → shipment_status_frame

# shippment_status_table → shipment_status_table (for consistency)

# 7. Empty Tables Look Odd Without Headings
# If no data is returned, consider inserting a single row like "No data available" in each section to avoid empty tables.

# 🧪 Optional: Add Export to CSV Feature
# In future iterations, adding an export button for each section to download the table as CSV could be valuable for business use.

# Let me know if you'd like help implementing any of the above.

""" Notes """
# Thanks for sharing your NotesFrame class. It's a well-structured Tkinter interface for managing notes. Here's a summary and feedback on your implementation, along with improvements or clarifications you might consider:

# ✅ Key Features Implemented
# Separation of concerns via self.factory.notes_logic for business logic and NotesFrame for UI.

# Widget Layout includes:

# Entry form for adding notes

# A Treeview for listing notes

# A Text widget for viewing selected note content

# Action and search menus

# Contributor selection prioritizes "admin" and deduplicates the list.

# Event Binding connects GUI selection with logic.

# 🔍 Suggestions & Observations
# 1. Avoid Redundant Imports
# You're importing tkinter, ttk, messagebox, and datetime twice:


# from tkinter import messagebox
# import tkinter as tk
# from tkinter import ttk
# from datetime import datetime
# Remove the duplicated block:


# import tkinter as tk
# from tkinter import ttk, messagebox
# from datetime import datetime
# 2. Encapsulation & Setup Separation
# You define a create_notes() method to initialize widgets, but it's not called inside __init__(). This may lead to confusion or missed initializations.

# Solution:
# Call self.create_notes() inside __init__() unless you're managing flow externally.

# 3. bind_events() Should Be Called After Treeview Creation
# Right now self.bind_events() is called in __init__() but before self.notes_listbox exists. This can raise an AttributeError.

# Fix:
# Move self.bind_events() to the end of create_notes() after self.notes_listbox is defined.

# 4. Handling Placeholder Text in Text Widget
# You're inserting:


# self.notes_text.insert("1.0", "Type your notes here...")
# But it never clears on click. That might confuse users.

# Improvement:
# Add focus-in event to clear it once:


# def clear_placeholder(event):
#     if self.notes_text.get("1.0", "end-1c").strip() == "Type your notes here...":
#         self.notes_text.delete("1.0", "end")

# self.notes_text.bind("<FocusIn>", clear_placeholder)
# 5. Missing on_note_select() Implementation
# You bind "<<TreeviewSelect>>" to self.on_note_select, but that method isn’t defined in the provided code.

# Define it:


# def on_note_select(self, event):
#     self.notes_logic.displaying.get_cursor(event)
# Or whatever your internal logic method is for populating note display.

# 🧹 Minor Suggestions
# Use grid_propagate(False) on frames where you want precise control (like notes_container).

# Consider clearing the note form after saving to prepare for a new entry.

# You may want to enable update and delete buttons dynamically when a note is selected.

# ✅ Overall Impression
# This class is thoughtfully built and modular, showing excellent use of Tkinter layout and styles. You're clearly abstracting 
# logic well into notes_logic and factory helpers.

#Improvements
# Positives / Improvements Noted
# Modular Separation:

# You’ve cleanly separated create_notes() from __init__(), deferring widget setup until explicitly needed.

# Logic Layer Decoupling:

# self.notes_logic handles all logic (searching, saving, updating), which keeps your UI clean and maintainable.

# UI Consistency & Readability:

# Nice layout with well-grouped frames (enter_notes_frame, notes_list_frame, action/search/current_note_frame).

# Styling (font, bg, etc.) is consistent with the factory approach.

# Robust Contributor Logic:

# The logic to prioritize "admin" and de-duplicate contributor list is smart and user-friendly.

# Dynamic Treeview:

# Proper column setup, styling, and spacing make it readable.

# 🛠️ Final Suggestions (Optional Polish)
# 1. Guard Against Duplicate Widget Creation
# If create_notes() might be called more than once (e.g., navigating between frames), you should ensure widgets aren’t duplicated:


# def create_notes(self):
#     if hasattr(self, "notes_frame"):
#         return  # Prevent re-creating UI
#     ...
# 2. Clean Up Placeholder Logic
# You’re using:


# self.notes_text.insert("1.0", "Type your notes here...")
# self.notes_text.focus_set()
# But if you want a true placeholder, consider binding <FocusIn> to clear the text if untouched:


# def clear_placeholder(event):
#     if self.notes_text.get("1.0", "end-1c").strip() == "Type your notes here...":
#         self.notes_text.delete("1.0", "end")

# self.notes_text.insert("1.0", "Type your notes here...")
# self.notes_text.bind("<FocusIn>", clear_placeholder)
# 3. Reset Search Entry on Frame Load (Optional UX)
# In create_notes(), consider clearing search_note_ent and notes_text content when the UI is initialized to avoid stale data.

# 4. Button Layout Padding
# Currently all action buttons use the same padding. To center or space them better:


# self.notes_action_menu.grid_columnconfigure((0,1,2,3), weight=1)
# And give each button sticky="ew".

# 5. Comment Cleanup
# Some commented-out lines (#self.clear_content(), etc.) can be removed if no longer needed.

# ✅ Summary
# Your NotesFrame is now solid, readable, and well-designed. You've shown good practice in GUI layout, logical separation, and user-centric details like contributor ordering and scroll handling.

# If you're planning unit/integration testing next or dynamic reloading of notes, I can help with that too.

# Would you like help wiring this frame into your controller (MainApp) or ensuring dynamic note updates (e.g., live refresh after save/delete)?

#''''notes'''
# 1. Enforce Required Fields & Early Validation
# Right now you check for duplicate subjects, but you don’t prevent empty subjects or content. At the top of save_note(), add:


# if not subject:
#     messagebox.showerror("Input Error", "Subject cannot be empty.")
#     return
# if not note_content:
#     messagebox.showerror("Input Error", "Note content cannot be empty.")
#     return
# That way you fail fast, before touching the database.

# 2. Pull DDL Out of “Save”
# You call create_notes_table() on every save. Instead, move your “CREATE TABLE IF NOT EXISTS” into your application startup or a dedicated migration script. That keeps save_note() focused on business logic, not schema management.

# 3. Centralize DB Queries
# There’s a lot of raw SQL scattered through your methods. Consider moving all SQL into a small “NotesRepository” or at least class-level constants:

# _INSERT_NOTE = "INSERT INTO notes(subject, date_time_entered, content, user_id) VALUES(?, ?, ?, ?)"
# _SELECT_ALL   = """SELECT n.id, n.subject, u.username, n.date_time_entered
#                    FROM notes n LEFT JOIN users u ON n.user_id=u.id ORDER BY n.date_time_entered"""
# ...
# That makes it easier to spot typos and swap out storage (e.g. to Postgres) later.

# 4. Reduce Repetition in List-Clearing
# You clear the treeview in exactly the same way every time:


# for iid in self.notes_frame.notes_listbox.get_children():
#     self.notes_frame.notes_listbox.delete(iid)
# Wrap that in a helper:

# def _clear_listbox(self):
#     for iid in self.notes_frame.notes_listbox.get_children():
#         self.notes_frame.notes_listbox.delete(iid)
# and just call _clear_listbox().

# 5. Unify “select then fetch” Pattern
# Both on_note_selected() and get_note_contributor_id() do:

# with DB: cursor.execute(sql, params)

# cursor.fetchone()

# if row: … else: error

# Factor that into a helper:


# def _fetchone(self, sql, params):
#     with DatabaseManager.with_connection() as conn:
#         cur = conn.cursor()
#         cur.execute(sql, params)
#         return cur.fetchone()
# Then you write:


# row = self._fetchone(self._SELECT_USER_ID, (contributor,))
# if not row...
# 6. Non-Editable Flag Handling
# You pull notes.non_editable but default to “No” if the column is missing. If in future you add more special columns, consider returning your note_data as a small namedtuple or dataclass, e.g.:


# Note = namedtuple("Note", ("subject","date_time","content","username","non_editable"))
# note = Note(*cursor.fetchone())
# Then your code becomes more self-documenting.

# 7. Threading / Long-Running Queries
# If your notes table grows large, loading all of them on every save/update could freeze the UI. Consider:

# Loading lazily (e.g. only the first N rows, or searching as you type).

# Spawning a background thread for heavy queries and updating the treeview when ready.

# 8. Error Feedback UX
# Right now every database error pops up as a modal. For frequent operations (e.g. “duplicate subject”), a less intrusive message (e.g. a status bar update) might improve usability.

# 9. Use Consistent Naming
# Your methods mix note_contributor vs. contributor_id vs. get_note_contributor_id(). Consider:

# Field widgets: self.combo_contributor

# Underlying value: contributor_username

# ID lookup: get_user_id(username)

# That way it’s always clear what type each variable holds.

# 10. Docstrings & Type Hints
# Sprinkle in Python type hints and docstrings:


# def save_note(self) -> None:
#     """Validate input, insert new note, refresh list, and clear fields."""
# And for method signatures:


# def get_note_contributor_id(self, contributor: str) -> Optional[int]:
# IDE support & linters will thank you.

# By tightening input validation, isolating your SQL, removing schema-management from runtime paths, and refactoring out repeated patterns, 
# you’ll make your Notes module more robust, maintainable, and ready for future enhancements.









