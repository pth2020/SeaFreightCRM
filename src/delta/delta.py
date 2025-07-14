from tkinter import *
import random
import time
import datetime

class Delta(Frame):
    """ A custom Tkinter Frame subclass — meaning it's a GUI container class 
        that represents a screen or view in your application.
    """
    def __init__(self, root, controller, show_login_callback, show_admin_callback): 
        # calling the constructor of the parent class, which in this case is tkinter.Frame.
        super().__init__(root) 
        self.controller = controller  # save controller ref - passed from Appcontroller
        # assign show_login_callback to call login back later in response to an event
        self.show_login_callback = show_login_callback   
        #  It allows the object to call this function later to show the admin interface or dashboard.
        self.show_admin_callback = show_admin_callback   
        # Assigns the root parameter (typically an instance of tk.Tk() in Tkinter) to self.root, making it accessible throughout the class.
        self.root = root
        self.root.title("Sea Freight Management System")

        # Get screen width and height
        self.screen_width = self.winfo_screenwidth()
        self.screen_height = self.winfo_screenheight()

        # Set window size
        self.root.geometry(f"{int(self.screen_width)}x{int(self.screen_height)}+0+0")
        self.root.configure(bg="#f0f0f0")

        # Instantiate factory here
        # Pass the main Tkinter window or frame (tk.Tk() - root and other callbacks) to the factory (instance of WidgetFactory class)
        from delta.widget_factory import WidgetFactory 
        self.factory = WidgetFactory( # allows factory to add widgets to the main GUI window  
            root=self.root,
            screen_width=self.screen_width,
            screen_height=self.screen_height,
            show_admin_callback=self.show_admin_callback,
            show_login_callback=self.show_login_callback,
        )
        #
        self.pack()
        

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


            
