from tkinter import *
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from tkinter import messagebox
import textwrap
from .displaying import Displaying 


class Receipt:
    """ Generates receipt for a shipping transaction """
    
    def __init__(self, factory):
        self.factory = factory
        self.displaying = Displaying(self.factory)
        
    def produce_receipt(self, trans_id, date_created):
        # collect data
        full_name = f"{self.factory.fname_ent.get().strip()} {self.factory.lname_ent.get().strip()}"
        sender_first_line_of_address = f"{self.factory.sender_build_door_no_ent.get().strip()} {self.factory.sender_street_road_ent.get().strip()}"
        sender_city = self.factory.sender_city_town_ent.get().strip()
        sender_postcode = self.factory.sender_postcode_ent.get().strip()
        dest_receiver_title_fullname = self.factory.dest_receiver_title_fullname_ent.get().strip()
        dest_first_line_of_address = self.factory.dest_first_line_of_address_ent.get().strip()
        dest_city = self.factory.dest_city_town_ent.get().strip()
        dest_country = self.factory.dest_country.get().strip()
        goods_type = self.factory.type_of_goods.get()
        total_weight = self.factory.total_weight_ent.get()

        # Estimate cost
        try:
            weight_float = float(total_weight)

            # Get country price from DB
            result = self.displaying.get_selected_country_id(dest_country)
            if result:
                _, country_price = result
                country_price = float(country_price)
            else:
                country_price = 2.0  # fallback default price per kg

            estimated_cost = weight_float * country_price

        except ValueError:
            estimated_cost = 0.0
            messagebox.showerror("Input Error", "Invalid weight input. Please enter a valid number.")

        receipt = textwrap.dedent(f"""
        -------------------------------------------------
           GLOBAL SHIPPING LTD - RECEIPT
        -------------------------------------------------
           Date: {date_created}
           Transaction ID: {trans_id}

           Customer: {full_name}
                     {sender_first_line_of_address}
                     {sender_city},{sender_postcode}
           Type of Goods: {goods_type}
           Total Weight:  {total_weight} kg

           Destination: {dest_receiver_title_fullname}
                        {dest_first_line_of_address}
                        {dest_city}, {dest_country}        

           Estimated Cost: £{estimated_cost:.2f}
        -------------------------------------------------
           Thank you for choosing us to ship your goods. 
           We appreciate your trust in our service.
        -------------------------------------------------
        """)
        self.factory.receipt_text.delete("1.0", END)
        self.factory.receipt_text.insert(END, receipt.strip())  
        
        # Save transaction info for later use 
        self.factory.generated_trans_id = trans_id
        self.factory.generated_date_created = date_created
        
        # Enable Save Receipt Button
        self.factory.btn_save_receipt.config(state=NORMAL)
        
    def save_receipt_as_pdf(self):
        receipt_text = self.factory.receipt_text.get("1.0", END).strip()

        if not receipt_text:
            messagebox.showerror("Error", "No receipt content to save.\nSelect data first.")
            return

        # Use stored trans_id and date_created
        trans_id = getattr(self.factory, 'generated_trans_id', None)
        date_created = getattr(self.factory, 'generated_date_created', None)

        if not trans_id or not date_created:
            messagebox.showerror("Error", "Missing transaction details. Generate receipt first.")
            return

        # Save as PDF
        filename = f"receipt_{trans_id}.pdf"
        c = canvas.Canvas(filename, pagesize=A4)
        _, height = A4
        c.setFont("Courier", 10)

        y = height - 50
        for line in receipt_text.split('\n'):
            c.drawString(50, y, line.strip())
            y -= 15

        c.save()
        messagebox.showinfo("PDF Saved", f"Receipt saved as {filename}")     
        
        
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