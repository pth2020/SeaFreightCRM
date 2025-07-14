import tkinter as tk
from tkinter import ttk
import sqlite3
import datetime
from tkinter import messagebox
from collections import defaultdict

from db.db_manager import DatabaseManager
from .dashboard import Dashboard, DashboardFrame
from .settings import Setting, SettingsFrame
from .report import Report, ReportFrame
from .statistics import Statistics, StatisticsFrame
from .notes import Notes, NotesFrame
from .displaying import Displaying

class WidgetFactory:
    def __init__(self, master, screen_width, screen_height, show_login_callback, show_admin_callback, show_dashboard,
                back_to_delta_frame, logout):
        self.master = master
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.show_login = show_login_callback
        self.show_admin = show_admin_callback
        self.show_dashboard = show_dashboard
        self.back_to_delta_frame = back_to_delta_frame
        self.logout = logout  
        
        # ===== Creating instance of classes =====
        # Create a dashboard-helper instance and store in the factory
        self.dashboard = Dashboard(self)       
        
        # Create a Setting‐helper instance and store it on the factory:
        self.settings_logic = Setting(self)
                
        # Create a report-helper instance and store it on the facatory
        self.report_logic = Report(self)
        
        # Create a statistics-helper instance and store in on the factory
        self.statistics_logic = Statistics(self)
        
        # Create a note-helper instance and store in on the factory
        self.notes_logic = Notes(self)  
        

    def create_sidebar(self):
        self.sidebar = tk.Frame(self.master, bg="#003366", width=200)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)  # <- This is crucial

        buttons = [
            ("Dashboard", self.set_up_dashboard),
            ("Settings", self.set_up_settings),
            ("Reports", self.set_up_report),
            ("Statistics", self.set_up_statistics),
            ("Notes", self.set_up_notes),
            ("Back To Main", self.back_to_delta_frame),
            ("Log Out", self.logout)
        ]

        for text, command in buttons:
            btn = tk.Button(self.sidebar, text=text, fg="white", bg="#003366", font=("Arial", 12), command=command)
            btn.pack(fill="x", pady=2)
            
    def set_up_styles(self):
        # Set widget properties
        self.label_opts = {"font": ("Helvetica", 12, "bold"), "bg": "#f0f0f0", "fg": "#333", "padx": 10, "pady": 10}
        self.text_opts = {"font": ("Helvetica", 12, "bold"), "bg": "#f0f0f0", "fg": "#333", "padx": 10, "pady": 10}
        self.entry_opts = {"font": ("Helvetica", 12), "width": 25, "bg":"white"}
        self.combo_opts = {"font": ("Helvetica", 12), "width" : 28}
        self.button_opts = {"bg":"#003366", "fg":"white", "activebackground":"#005580", "activeforeground":"white", 
                            "font":("Helvetica", 13, "bold"), "width":15, "bd":0, "padx":10, "pady":6, "cursor":"hand2", "relief":tk.FLAT}  

    def create_main_content(self):
        self.content = tk.Frame(self.master, bg="white") # child of self - which is AdminFrame
        # This places the self.content frame on the right side of the main window (AdminFrame).
        self.content.pack(side="right", fill="both", expand=True) # This frame acts as the main content area, 
        
        self.set_up_dashboard()
        
    def set_up_dashboard(self):    
        self.clear_content()
        dashboard_logic = Dashboard(self)  # self = factory
        dashboard_frame = DashboardFrame(self.content, dashboard_logic)
        dashboard_frame.pack(fill="both", expand=True)# ← pack it into the GUI       
    
    
    def set_up_settings(self):       
        self.clear_content()        
        settings_frame = SettingsFrame(master=self.content, factory=self)
        self.settings_logic.set_settings_frame(settings_frame)  # link frame to logic    
        settings_frame.create_settings()  # now it's safe to call, frame is fully initialized    
        settings_frame.pack(fill="both", expand=True)                
            

    def set_up_report(self):        
        self.clear_content()
        report_frame = ReportFrame(master=self.content, factory=self)
        self.report_logic.set_report_frame(report_frame)  # link frame to logic    
        report_frame.create_report()  # now it's safe to call, frame is fully initialized    
        report_frame.pack(fill="both", expand=True)
        
                
    def set_up_statistics(self):   
        self.clear_content()     
        statistics_frame = StatisticsFrame(master=self.content, factory=self)  # Create instance
        statistics_frame.create_statistics()   # Call instance method
        statistics_frame.pack(fill="both", expand=True)
        
                
    def set_up_notes(self):
        self.clear_content()    
        self.notes_frame = NotesFrame(master=self.content, factory=self)
        self.notes_logic.set_notes_frame(self.notes_frame) 
        #self.notes_logic.set_notes_frame(self.notes_frame)  # link frame to logic
        self.notes_frame.create_notes()
        #self.notes_frame.notes_listbox.bind("<ButtonRelease-1>", self.notes_logic.get_cursor)  # ← move here
        self.notes_frame.pack(fill="both", expand=True)
        
                    
            
    def back_to_delta_frame(self):
        from admin.navigation import Navigation
        navigation = Navigation(self.content)        
        navigation.to_delta_frame()

        
    def logout(self):
        from admin.navigation import Navigation        
        #Navigation.logout()
                
    # This is a utility method that clears out the content area (self.content) by destroying all widgets inside it.
    def clear_content(self):
        for widget in self.content.winfo_children(): # This returns a list of all the widgets that are children of self.content.
            # The method winfo_children() in Tkinter is used to retrieve all immediate child widgets of a given widget.
            widget.destroy()          
        

#  def create_main_content(self):
#         self.content = tk.Frame(self.master, bg="white") # child of self - which is AdminFrame
#         # This places the self.content frame on the right side of the main window (AdminFrame).
#         self.content.pack(side="right", fill="both", expand=True) # This frame acts as the main content area, 
#                                                                 # where all the dynamic views (Dashboard, Settings, Reports, etc.) will be shown.
#         # fill="both" means it expands to fill both horizontal and vertical space.
#         # expand=True allows it to take up any additional space when the window is resized.
#         # self.show_dashboard()  # Default view
#         # This calls the method show_dashboard() right after creating the content area.
#         # It means that when the content area is created, the dashboard view is loaded by default.