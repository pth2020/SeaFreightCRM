from db.db_manager import DatabaseManager
from tkinter import messagebox
import tkinter as tk
from tkinter import ttk
import sqlite3
import datetime
from collections import defaultdict # for auto-initializing dictionary keys
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure # for creating charts inside the Tkinter window

class StatisticsFrame(tk.Frame):
    def __init__(self, master, factory):
        super().__init__(master)
        self.factory = factory
        self.statistics_logic = self.factory.statistics_logic
        
        
    def create_statistics(self):
        #self.clear_content()

        stats_frame = tk.Frame(self, bg="white")
        stats_frame.pack(fill="both", expand=True)

        # Create a Matplotlib figure
        fig = Figure(figsize=(6, 4), dpi=100)
        ax = fig.add_subplot(111)

        # Get the current year
        current_year = datetime.datetime.now().year

        # Initialize a dictionary to store month -> count
        monthly_counts = defaultdict(int)

        # Query the database for counts per month
        try:
            with DatabaseManager.with_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT strftime('%m', created_at) AS month, COUNT(*) 
                    FROM shipments 
                    WHERE strftime('%Y', created_at) = ?
                    GROUP BY month
                    ORDER BY month
                """, (str(current_year),))
                
                rows = cursor.fetchall()
                for month, count in rows:
                    monthly_counts[int(month)] = count  # '01' -> 1, etc.

        except Exception as e:
            messagebox.showerror("Database Error", str(e))
            return

        # Prepare x and y axes
        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        x = months
        y = [monthly_counts.get(i + 1, 0) for i in range(12)]  # Ensure 0 if no data for a month

        # Plot data
        ax.plot(x, y, marker='o', linestyle='-')
        ax.set_title(f"Total Monthly Shipments {current_year}")
        ax.set_xlabel("Month")
        ax.set_ylabel("Total Shipments")

        # Show chart in Tkinter
        canvas = FigureCanvasTkAgg(fig, master=stats_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)  

class Statistics:
    
    def __init__(self, factory):
        self.factory = factory
    
    def show_statistics(self):
        self.factory.clear_content()
        tk.Label(self.content, text="Statistics", font=("Arial", 18)).pack(pady=20)
        
# Imports
# python
# Copy
# Edit
# from db.db_manager import DatabaseManager
# from tkinter import messagebox
# import tkinter as tk
# from tkinter import ttk
# import sqlite3
# import datetime
# from collections import defaultdict
# from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
# from matplotlib.figure import Figure
# These imports bring in the necessary modules:

# tkinter: for the GUI

# matplotlib: for creating charts inside the Tkinter window

# datetime: for getting the current year

# defaultdict: for auto-initializing dictionary keys

# DatabaseManager: a custom class to manage database connections

# 🔹 StatisticsFrame class
# This class is a Tkinter Frame that displays a chart of monthly shipment counts.

# 🔸 __init__ method
# python
# Copy
# Edit
# def __init__(self, master, factory):
#     super().__init__(master)
#     self.factory = factory
#     self.statistics_logic = self.factory.statistics_logic
# Initializes the frame.

# Saves the factory, which is likely a central controller holding shared logic or services.

# Sets self.statistics_logic to whatever logic layer is defined in factory.

# 🔸 create_statistics method
# This is the heart of the statistics display logic.

# 1. Create a container Frame
# python
# Copy
# Edit
# stats_frame = tk.Frame(self, bg="white")
# stats_frame.pack(fill="both", expand=True)
# Creates a child frame inside the current frame (self) to hold the chart.

# 2. Set up Matplotlib figure
# python
# Copy
# Edit
# fig = Figure(figsize=(6, 4), dpi=100)
# ax = fig.add_subplot(111)
# Initializes a Matplotlib figure and adds a subplot (ax) where the chart will go.

# 3. Get the current year
# python
# Copy
# Edit
# current_year = datetime.datetime.now().year
# Dynamically fetches the current year (e.g., 2025).

# 4. Prepare a dictionary to hold monthly counts
# python
# Copy
# Edit
# monthly_counts = defaultdict(int)
# Uses defaultdict so that any new month accessed will default to 0.

# 5. Query the database
# python
# Copy
# Edit
# with DatabaseManager.with_connection() as conn:
#     cursor = conn.cursor()
#     cursor.execute("""
#         SELECT strftime('%m', created_at) AS month, COUNT(*) 
#         FROM shipments 
#         WHERE strftime('%Y', created_at) = ?
#         GROUP BY month
#         ORDER BY month
#     """, (str(current_year),))
# Connects to the database using a context manager.

# Executes a SQL query:

# Extracts the month (%m) from the created_at timestamp.

# Filters only rows from the current year.

# Groups results by month.

# Example result: [('01', 5), ('02', 10)]

# 6. Store results in dictionary
# python
# Copy
# Edit
# for month, count in rows:
#     monthly_counts[int(month)] = count
# Converts string month like '01' to integer 1, and stores the count.

# 7. Handle exceptions
# python
# Copy
# Edit
# except Exception as e:
#     messagebox.showerror("Database Error", str(e))
#     return
# If the database fails, show a pop-up error and exit the method early.

# 8. Prepare chart data
# python
# Copy
# Edit
# months = ['Jan', 'Feb', 'Mar', ..., 'Dec']
# x = months
# y = [monthly_counts.get(i + 1, 0) for i in range(12)]
# x is the month labels.

# y pulls the counts from the monthly_counts dictionary, filling in 0 for any missing months.

# 9. Plot the chart
# python
# Copy
# Edit
# ax.plot(x, y, marker='o', linestyle='-')
# ax.set_title(f"Total Monthly Shipments {current_year}")
# ax.set_xlabel("Month")
# ax.set_ylabel("Total Shipments")
# Plots the line graph with month on the x-axis and shipment count on the y-axis.

# 10. Render the chart in Tkinter
# python
# Copy
# Edit
# canvas = FigureCanvasTkAgg(fig, master=stats_frame)
# canvas.draw()
# canvas.get_tk_widget().pack(fill="both", expand=True)
# Embeds the Matplotlib chart inside the stats_frame using a canvas widget.

# 🔹 Statistics class
# This looks like a logic or controller class (though it appears unfinished).

# 🔸 __init__ method
# python
# Copy
# Edit
# def __init__(self, factory):
#     self.factory = factory
# Stores the factory reference to access shared components.

# 🔸 show_statistics method (INCOMPLETE)
# python
# Copy
# Edit
# def show_statistics(self):
#     self.factory.clear_content()
#     tk.Label(self.content, text="Statistics", font=("Arial", 18)).pack(pady=20)
# Intended to clear the main view and show the statistics label.

# But self.content is undefined here, which will raise an error unless self.content is set somewhere else.

# ✅ Summary
# StatisticsFrame builds and shows a line graph of monthly shipment data.

# It queries a database table (shipments) for the current year and plots totals per month.

# Uses matplotlib inside Tkinter for dynamic visual reporting.

# The Statistics class appears to be a separate controller, but its show_statistics method is incomplete or partially copied.

# Would you like me to help you finish the Statistics class or integrate it properly with StatisticsFrame?








# You said:
# I need detailed explanation on this                                                                                                                    Set up Matplotlib figure

# fig = Figure(figsize=(6, 4), dpi=100)
# ax = fig.add_subplot(111)
# Initializes a Matplotlib figure and adds a subplot (ax) where the chart will go.


# ChatGPT said:
# Here’s a deep dive into those two lines—breaking down exactly what’s happening under the hood:

# python
# Copy
# Edit
# fig = Figure(figsize=(6, 4), dpi=100)
# ax  = fig.add_subplot(111)
# 1. Figure(figsize=(6, 4), dpi=100)
# Figure class

# Provided by Matplotlib’s object-oriented API (matplotlib.figure.Figure), it represents the entire drawing canvas or “figure” you’ll display.

# figsize=(6, 4)

# Specifies the width and height of the figure in inches.

# Our figure will be 6 inches wide and 4 inches tall.

# Why inches? Matplotlib uses physical units so that when you save or print, the size is consistent regardless of your screen’s pixel density.

# dpi=100

# Stands for Dots Per Inch.

# Controls the resolution: how many pixels are used per inch when rendering.

# 100 dpi means 100 pixels for every inch.

# For our 6×4″ figure, the final pixel dimensions are 600 × 400 (6 × 100 by 4 × 100).

# Putting it together

# fig is now a blank canvas of size 600 × 400 pixels (on‐screen or in an image file), ready to hold one or more plots.

# 2. ax = fig.add_subplot(111)
# What is a “subplot”?

# In Matplotlib, the figure can contain one or more axes—the individual regions where data is plotted.

# Each axes has its own x and y axis, labels, title, etc.

# Calling add_subplot(111)

# The three-digit code 111 is shorthand for “1×1 grid, first subplot”:

# First digit (1): Number of rows.

# Second digit (1): Number of columns.

# Third digit (1): Index of the active subplot (counting left-to-right, top-to-bottom, starting at 1).

# Since it’s a 1×1 grid, 111 simply gives you a single axes that fills the entire figure.

# Return value

# add_subplot returns an Axes object, here stored in ax.

# You’ll use ax to:

# Plot data (ax.plot(...))

# Set titles and labels (ax.set_title(...), ax.set_xlabel(...), etc.)

# Customize ticks, legends, gridlines, and more.

# 3. Why use this object-oriented approach?
# Explicit control: You can create multiple subplots (ax1, ax2, …) in the same figure, each with different data and styling.

# Clean code: Keeps figure-level settings (fig) separate from axes-level settings (ax).

# Reusability: You can pass around fig and ax objects to functions that further modify or save them.

# 4. Visual summary
# less
# Copy
# Edit
# ┌──────────────────────────────────────────────┐
# │                  Figure                     │  ← fig: defined size (6×4″) & resolution (100 dpi)
# │  ┌────────────────────────────────────────┐  │
# │  │               Axes (ax)               │  │  ← ax: the plotting area inside the figure
# │  │  (plots, labels, title, ticks happen  │  │
# │  │   here)                                │  │
# │  └────────────────────────────────────────┘  │
# └──────────────────────────────────────────────┘
        
