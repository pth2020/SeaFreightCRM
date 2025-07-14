import tkinter as tk
from tkinter import ttk
from db.db_manager import DatabaseManager
import sqlite3
import datetime
from tkinter import messagebox
from collections import defaultdict
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure


class AdminFrame(tk.Frame):
    def __init__(self, master, controller, return_callback):
        super().__init__(master)
        self.controller = controller
        self.master = master
        self.return_callback = return_callback  
        
        from admin.admin_widget_factory import WidgetFactory 
        self.factory = WidgetFactory(
            master=self,
            screen_width=controller.screen_width,
            screen_height=controller.screen_height,
            show_login_callback=controller.show_login,
            show_admin_callback=controller.show_admin,
            show_dashboard=controller.show_delta_dashboard,  
            back_to_delta_frame=controller.show_delta_frame, 
            logout=controller.logout
        )        
        
        # Create widgets
        self.create_widgets()
        self.pack(fill="both", expand=True) # Show the frame
        
    def create_widgets(self): 
        # Call WidgetFactory methods 
        self.factory.create_sidebar()
        self.factory.create_main_content()  
        #self.factory.set_up_styles()     
        
        

                


        
            


        
        
        


        
# AdminFrame represents a self-contained frame (or screen) in a larger Tkinter GUI — 
# specifically for admin-related functionality. It can be one of many frames managed by 
# a controller to support multi-page navigation.

# If you're building a multi-page app (e.g., login screen, admin dashboard, shipment form), you pass a controller object that:
# Keeps track of all frames
# Provides methods like show_frame("AdminFrame") to switch views
# Acts as a central app manager

# AdminFrame is a reusable frame that represents a screen in your GUI app.
# It uses the master to connect to the parent widget.
# It uses the controller to interact with the rest of the app (especially to switch screens).
# pack(fill="both", expand=True) makes sure it fully occupies the window.
        
# The hasattr() function in Python is used to check if an object has a specific attribute. 
# It returns True if the attribute exists, and False if it does not. This can be helpful 
# when you need to verify that an attribute or a property exists on an object before you 
# try to access it, which helps to prevent errors like AttributeError.

# Example
# hasattr(object, name)
# object: The object you're checking for an attribute.
# name: A string that represents the name of the attribute you're checking for.
# Returns
# True if the object has the specified attribute.
# False if the object does not have the specified attribute.

# class MyClass:
    #def __init__(self):
        #self.my_attr = 10

# obj = MyClass()

# Check if 'obj' has an attribute 'my_attr'
# print(hasattr(obj, 'my_attr'))  # True

# Check if 'obj' has an attribute 'other_attr'
# print(hasattr(obj, 'other_attr'))  # False


# for i in range(4):  #  looping over i from 0 to 3 (range(4))
        # row = i // 2  # row = i // 2 → integer division (floor division)
        # col = i % 2   # col = i % 2 → remainder (modulo)

# 🔢 Breakdown per iteration:
# i	    row = i // 2	   col = i % 2	    Placement
# 0	    0	               0	            (0, 0)
# 1	    0	               1	            (0, 1)
# 2	    1	               0	            (1, 0)
# 3	    1	               1	            (1, 1)

# So you're mapping the list of 4 elements to:

# [ (0, 0), (0, 1), 
#   (1, 0), (1, 1) 
# ]

# List Comprehension  
# List comprehension offers a shorter syntax when you want to create a new list based on the values of an existing list.
# Example:
# Based on a list of fruits, you want a new list, containing only the fruits with the letter "a" in the name.
# Without list comprehension you will have to write a for statement with a conditional test inside:
# fruits = ["apple", "banana", "cherry", "kiwi", "mango"]
# newlist = []
# for x in fruits:
#   if "a" in x:
#     newlist.append(x)
#     print(newlist)
# prints:  ["apple", "banana", "mango"]
# With list comprehension you can do all that with only one line of code:
# fruits = ["apple", "banana", "cherry", "kiwi", "mango"]
# [x for x in fruits if "a" in x]

# cursor.fetchall() - what does it return?
# cursor.fetchall() returns a list of all rows fetched from the database query result.
# Each row is returned as a tuple containing the column values for that row.
# Assuming your table country_price has the following data:
# country
# Nigeria
# Ghana
# Kenya

# Then:
# rows = cursor.fetchall()
# print(rows)
# [('Nigeria',), ('Ghana',), ('Kenya',)]
# Using List comprehension
# countries = [row[0] for row in rows]
# Output: ['Nigeria', 'Ghana', 'Kenya']


# timedelta
# Why it's used:
# To add or subtract time (like days, hours, minutes) from a datetime object.
# from datetime import datetime, timedelta

# today = datetime.now()
# print("Today:", today)

# Subtract 3 days
# three_days_ago = today - timedelta(days=3)
# print("3 Days Ago:", three_days_ago)

# Add 7 days
# next_week = today + timedelta(days=7)
# print("Next Week:", next_week)
        

