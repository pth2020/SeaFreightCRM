import textwrap
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from db.db_manager import DatabaseManager
from .displaying import Displaying
from .saving import Saving
from .updating import Updating
from .deleting import Deleting
from .clearing import Clearing
from .searching import Searching 
from .receipt import Receipt



class WidgetFactory:
    """ Builds the UI for Delta Dashboard """

    def __init__(self, root, screen_width, screen_height,
                    show_admin_callback=None,
                    show_login_callback=None,
                    save_data_callback=None):

        self.root = root
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.show_admin_callback = show_admin_callback
        self.show_login_callback = show_login_callback
        self.save_data_callback = save_data_callback
        
        self.displaying = Displaying(self)
        self.saving = Saving(self)
        self.updating = Updating(self)
        self.deleting = Deleting(self)
        self.clearing = Clearing(self)
        self.searching = Searching(self)
        self.receipt = Receipt(self)
                
        # Create widgets
        self.create_widgets()      
        
        
    def create_widgets(self):   
                        
        # Call WidgetFactory methods
        self.setup_frames()
        self.setup_styles()
        self.setup_left_frame_widgets()
        self.setup_right_frame_widget()
        self.setup_admin_buttons()
        self.setup_menu_buttons()
        self.setup_details_table()

        self.displaying.display_data()
        
        self.bind_event()
        self.saving.bind_saving_events()
        self.searching.bind_searching_events()

        
    def setup_styles(self):
        self.label_opts = {"font": ("Helvetica", 12, "bold"), "bg": "#E6E6FA", "fg": "#333", "padx": 10, "pady": 10}
        self.entry_opts = {"font": ("Helvetica", 12), "width": 30, "bg":"white"}
        self.combo_opts = {"font": ("Helvetica", 12), "width" : 28}
        self.combo_search_opts = {"font": ("Helvetica", 12), "width" : 25}
        self.button_opts = {"bg":"#003366",         # Deep blue background
            "fg":"white",           # White text
            "activebackground":"#005580",  # Hover background
            "activeforeground":"white",
            "font":("Helvetica", 13, "bold"),
            "width":15,
            "bd":0,                 # No border for flat look
            "padx":10,
            "pady":6,
            "cursor":"hand2",       # Pointer cursor on hover
            "relief":FLAT,           # Flat design        
        }   
        
    def setup_frames(self):
        """ Setting up the layout for all frames in Delta Dashboard """
        
        # ========= Main Container Frame ====================================
        self.Dataframe = Frame(self.root, bd=10, relief=RIDGE, bg="#E6E6FA")
        self.Dataframe.place(x=0, y=0, width=self.screen_width, height=self.screen_height)   
        
        # Title Frame 
        self.lbltitle = Label(self.Dataframe, bd=10, relief=RIDGE, text="DELTA SEA FREIGHT MANAGEMENT SYSTEM",
                        fg="#003366", bg="white", font=("Helvetica", 30, "bold"), pady=10)
        #lbltitle.pack(side=TOP, fill=X)
        self.lbltitle.place(x=0, y=0, width=0.98*self.screen_width, height=70 )
        
        # Left container Frame - to hold most data Entry widgets
        self.DataFrameLeft = LabelFrame(self.Dataframe, bd=8, relief=RIDGE, padx=10,
                                font=("Helvetica", 13, "bold"), text="Sender Information", bg="#E6E6FA", fg="#003366")
        self.DataFrameLeft.place(x=0, y=70, width=980, height=415)

        # Right container Frame - to hold the receipt 
        self.DataFrameRight = LabelFrame(self.Dataframe, bd=8, relief=RIDGE, padx=10,
                                    font=("Helvetica", 13, "bold"), text="Receipt", bg="#E6E6FA", fg="#003366")
        self.DataFrameRight.place(x=990, y=70, width=490, height=415)
        
        # ================== Admin Buttons ====================================
        # LabelFrame
        self.Admin_menu = LabelFrame(self.Dataframe, bd=8, relief=RIDGE, padx=10,
                                font=("Helvetica", 11, "bold"), text="Admin Menu", bg="#E6E6FA", fg="#003366")
        self.Admin_menu.place(x=0, y=490, width=0.98*self.screen_width, height=80)        
        
        # ==================== Data Menu Buttons ===============================
        self.Data_menu = LabelFrame(self.Dataframe, bd=8, relief=RIDGE, padx=10,
                                font=("Helvetica", 11, "bold"), text="Data Menu", bg="#E6E6FA", fg="#003366")
        self.Data_menu.place(x=0, y=570, width=0.98*self.screen_width, height=80)        

        # ===================== Details Frame - TreeView  ============================
        self.Detailsframe = Frame(self.root, bd=10, relief=RIDGE, bg="#E6E6FA")
        self.Detailsframe.place(x=0, y=660, width=0.98*self.screen_width, height=170)
        
    def setup_left_frame_widgets(self):
        
        # ============  Widgets on the Left container Frame ================
        
        # ==== Main Sender details labels and entries ====
        Label(self.DataFrameLeft, text="First Name:", **self.label_opts).grid(row=0, column=0, sticky=W)
        self.fname_ent = Entry(self.DataFrameLeft, **self.entry_opts)
        self.fname_ent.grid(row=0, column=1, padx=5, pady=10, ipady = 3)

        Label(self.DataFrameLeft, text="Last Name:", **self.label_opts).grid(row=0, column=2, sticky=W)
        self.lname_ent = Entry(self.DataFrameLeft, **self.entry_opts)
        self.lname_ent.grid(row=0, column=3, padx=5, pady=10, ipady = 3)

        Label(self.DataFrameLeft, text="Mobile:", **self.label_opts).grid(row=1, column=0, sticky=W)
        self.mobile_ent = Entry(self.DataFrameLeft, **self.entry_opts)
        self.mobile_ent.grid(row=1, column=1, padx=5, pady=10, ipady = 3)

        Label(self.DataFrameLeft, text="Email:", **self.label_opts).grid(row=1, column=2, sticky=W)
        self.email_ent = Entry(self.DataFrameLeft, **self.entry_opts)
        self.email_ent.grid(row=1, column=3, padx=5, pady=10, ipady = 3)
        
        # ==== Sender Address ====
        Label(self.DataFrameLeft, text="Sender Address:", **self.label_opts).grid(row=2, column=0, sticky=W)
        
        ### building name or door number
        self.sender_build_door_no_ent = Entry(self.DataFrameLeft, **self.entry_opts)
        self.sender_build_door_no_ent.grid(row=2, column=1, padx=5, pady=10, ipady = 3)
        
        ### street or road name
        self.sender_street_road_ent = Entry(self.DataFrameLeft, **self.entry_opts)
        self.sender_street_road_ent.grid(row=3, column=1, padx=5, pady=10, ipady = 3)
        
        ### city or town 
        self.sender_city_town_ent = Entry(self.DataFrameLeft, **self.entry_opts)
        self.sender_city_town_ent.grid(row=4, column=1, padx=5, pady=10, ipady = 3)
        
        ### postcode
        self.sender_postcode_ent = Entry(self.DataFrameLeft, **self.entry_opts)
        self.sender_postcode_ent.grid(row=5, column=1, padx=5, pady=10, ipady = 3)
        
        #  ===== Destination Address ====
        Label(self.DataFrameLeft, text="Receiver Address:", **self.label_opts).grid(row=2, column=2, sticky=W)
        
        ## Receiver title and full name
        self.dest_receiver_title_fullname_ent = Entry(self.DataFrameLeft, **self.entry_opts)
        self.dest_receiver_title_fullname_ent.grid(row=2, column=3, padx=5, pady=10, ipady=3)
        
        ### destination first line of address
        self.dest_first_line_of_address_ent = Entry(self.DataFrameLeft, **self.entry_opts)
        self.dest_first_line_of_address_ent.grid(row=3, column=3, padx=5, pady=10, ipady=3)
        
        ### destination city or town 
        self.dest_city_town_ent = Entry(self.DataFrameLeft, **self.entry_opts)
        self.dest_city_town_ent.grid(row=4, column=3, padx=5, pady=10, ipady=3)
        
        ### destination country        
        self.dest_country = ttk.Combobox(self.DataFrameLeft, **self.combo_opts, style="TCombobox")
        self.dest_country["values"] = self.displaying.load_country_list()  # import from Displaying class (displaying.py)
        #self.type_of_goods.set("Perishable")  # Set default value
        self.dest_country.grid(row=5, column=3, padx=5, pady=10, ipady = 3)        
                
        ### Mobile
        self.dest_mobile_ent = Entry(self.DataFrameLeft, **self.entry_opts)
        self.dest_mobile_ent.grid(row=6, column=3, padx=5, pady=10, ipady=3)
        
        ### Add the Combobox for Type of Goods with a custom style
        Label(self.DataFrameLeft, text="Type of Goods:", **self.label_opts).grid(row=6, column=0, sticky=NW)
        self.type_of_goods = ttk.Combobox(self.DataFrameLeft, **self.combo_opts, style="TCombobox")
        self.type_of_goods["values"] = ("Perishable", "Hazardous", "General")
        self.type_of_goods.set("Perishable")  # Set default value
        self.type_of_goods.grid(row=6, column=1, padx=5, pady=10, ipady = 3)
        
        ### Weight 
        Label(self.DataFrameLeft, text="Total Weight (KG):", **self.label_opts).grid(row=7, column=2, sticky=W)
        self.total_weight_ent = Entry(self.DataFrameLeft, **self.entry_opts)
        self.total_weight_ent.grid(row=7, column=3, padx=5, pady=10, ipady = 3)
        
        ### Add the Combobox for Status of goods with a custom style
        Label(self.DataFrameLeft, text="Status of Goods:", **self.label_opts).grid(row=7, column=0, sticky=NW)
        self.status_of_goods = ttk.Combobox(self.DataFrameLeft, **self.combo_opts, style="TCombobox")
        self.status_of_goods["values"] = ("Collected", "Shipped - In transit", "Arrived")
        self.status_of_goods.set("Collected")  # Set default value
        self.status_of_goods.grid(row=7, column=1, padx=5, pady=10, ipady = 3)
        
    def setup_right_frame_widget(self):
        # ========= Widgets on the DataFrameRight ===========        
        self.receipt_text = Text(self.DataFrameRight, font=("Courier New", 11), width=50, height=25, bg="white")
        self.receipt_text.grid(row=0, column=0, columnspan=2)   
        
    def setup_admin_buttons(self):
        # ========= Widgets Admin Buttons ============
        self.btn_admin = Button(self.Admin_menu, text="Open Admin", command=self.show_admin_callback, **self.button_opts)
        self.btn_admin.grid(row=0, column=0, padx=2, pady=10)
    
        # Exit button to exit from the system
        btn_exit = Button(self.Admin_menu, text="Exit", **self.button_opts, command=self.root.quit)
        btn_exit.grid(row=0, column=1, padx=2, pady=10)

        
    def setup_menu_buttons(self):
        # ========== Widget Data Menu =============
        # Save Button - Disable save button initially
        #saving = Saving(factory=self) 
        self.btn_save = Button(self.Data_menu, text="Save", command=self.saving.save_data, **self.button_opts)
        self.btn_save.grid(row=0, column=0, padx=2, pady=5)
        self.btn_save.config(state=DISABLED)  # Disable Save button initially        
        
        # Update Button - Disabled initially until a row (data) is selected
        #updating = Updating(factory=self)
        self.btn_update = Button(self.Data_menu, text="Update", command=self.updating.update_data, **self.button_opts)
        self.btn_update.grid(row=0, column=1, padx=2, pady=5)
        self.btn_update.config(state=DISABLED)

        # Delete Button - Disabled initially until a row (data) is selected
        #deleting = Deleting(factory=self)
        self.btn_delete = Button(self.Data_menu, text="Delete", command=self.deleting.delete_data, **self.button_opts)
        self.btn_delete.grid(row=0, column=2, padx=2, pady=5)
        self.btn_delete.config(state=DISABLED)

        # Clear button - Disabled initially until data is entered on Entries or a rwo is selected
        #clearing = Clearing(factory=self)
        self.btn_clear = Button(self.Data_menu, text="Clear", command=self.clearing.clear_fields, **self.button_opts)
        self.btn_clear.grid(row=0, column=3, padx=2, pady=5)
        self.btn_clear.config(state=DISABLED)

        # === Search Section ===
        # Search Button - Disabled initially until search word is entered
        #searching = Searching(factory=self)
        self.btn_search = Button(self.Data_menu, text="Search by ", command=self.searching.search_data, **self.button_opts)
        self.btn_search.grid(row=0, column=5, padx=2, pady=5)
        self.btn_search.config(state=DISABLED)
        
        # Drop down menu - combobox
        self.combo_search_opts = ttk.Combobox(self.Data_menu, font=("Helvetica", 11), width=15, style="TCombobox")
        self.combo_search_opts["values"] = ("Transaction Id","First Name", "Last Name", "Mobile", "Email", "Status")
        self.combo_search_opts.set("Transaction Id")
        self.combo_search_opts.grid(row=0, column=6, padx=5, pady=5, ipady=2)
        
        # Search Entry
        self.search_ent = Entry(self.Data_menu, font=("Helvetica", 12), width=15, bg="white")
        self.search_ent.grid(row=0, column=7, padx=6, pady=5, ipady = 3)
        
        # Back button
        #displaying = Displaying(factory=self)
        self.btn_back = Button(self.Data_menu, text="Back", command=self.displaying.display_data, padx=10, pady = 6, font =("Helvetica", 13, "bold"),
                            bg="#003366", fg="white", width = 5, cursor="hand2", relief=FLAT )
        self.btn_back.grid(row=0, column=8, padx=2, pady=5)
        self.btn_back.config(state=DISABLED)         
        
        # Save Receipt button
        #receipt = Receipt(factory=self)
        self.btn_save_receipt = Button(self.Data_menu, text="Save Receipt", command=self.receipt.save_receipt_as_pdf, **self.button_opts)
        self.btn_save_receipt.grid(row=0, column=9, padx=2, pady=5)
        self.btn_save_receipt.config(state=DISABLED)    
        
            
    def setup_details_table(self):
        # Table
        # Scrollbar 
        scroll_x = ttk.Scrollbar(self.Dataframe, orient=HORIZONTAL)
        scroll_y = ttk.Scrollbar(self.Dataframe, orient=VERTICAL)

        # Treeview widget with columns and linked scrollbars
        self.global_table = ttk.Treeview(self.Detailsframe, 
                                columns=("id", "transaction_id", "date_created", "fullname", "mobile", "email", 
                                        "type_of_goods", "total_weight", "date_shipped", "total_cost", "status_of_goods"), 
                                xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)

        # Configure the scrollbars to work with the Treeview
        scroll_x.config(command=self.global_table.xview)
        scroll_y.config(command=self.global_table.yview)

        # Packing scrollbars
        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)
        
        # Treeview column headings
        self.global_table.heading("id", text="ID", anchor='w')
        self.global_table.heading("transaction_id", text="Transaction Id", anchor='w')
        self.global_table.heading("date_created", text="Created On", anchor='w')
        self.global_table.heading("fullname", text="Full Name", anchor='w')
        self.global_table.heading("mobile", text="Mobile", anchor='w')
        self.global_table.heading("email", text="Email", anchor='w')
        self.global_table.heading("type_of_goods", text="Type of Goods", anchor='w')
        self.global_table.heading("total_weight", text="Total Weight", anchor='w')
        self.global_table.heading("date_shipped", text="Date Shipped", anchor='w') 
        self.global_table.heading("total_cost", text="Total Cost", anchor='w')
        self.global_table.heading("status_of_goods", text="Status of Goods", anchor='w')

        # Set Treeview to show only headings (no tree-style display)
        self.global_table["show"] = "headings"

        # Pack Treeview widget inside the details frame
        self.global_table.pack(fill=BOTH, expand=1)
        
        self.global_table.column("id", width=50)
        self.global_table.column("transaction_id", width=100)
        self.global_table.column("date_created", width=100)
        self.global_table.column("fullname", width=150)
        self.global_table.column("mobile", width=100)
        self.global_table.column("email", width=150)
        self.global_table.column("type_of_goods", width=120)
        self.global_table.column("total_weight", width=100)
        self.global_table.column("date_shipped", width=100)
        self.global_table.column("total_cost", width=100)
        self.global_table.column("status_of_goods", width=120)
        
        self.displaying.bind_display_event()
        
    def bind_event(self):
        # Binds Focus in and out for placeholders in Entries
        entries = {
            self.sender_build_door_no_ent: "Building / Door No.", # widget : placeholder
            self.sender_street_road_ent: "Street / Road",
            self.sender_city_town_ent: "City / Town",
            self.sender_postcode_ent: "Postcode",
            self.dest_receiver_title_fullname_ent: "Title & Receiver's Full name",
            self.dest_first_line_of_address_ent: "Building/door-no street/road",
            self.dest_city_town_ent: "City / Town",
            self.dest_mobile_ent: "Mobile Number"
        }
        # Combobox placeholder
        self.dest_country.set("Select Country")
        self.dest_country.config(foreground="#787878")
        
        for entry, placeholder in entries.items():
            entry.insert(0, placeholder)
            entry.config(fg='#787878')  # Placeholder color
            entry.placeholder = placeholder  # Attach placeholder as custom attribute
            entry.bind("<FocusIn>", self.on_entry_click)
            entry.bind("<FocusOut>", self.on_focusout)   
            
            # You don't need to pass placeholder manually when binding self.on_entry_click to the Entry, 
            # because you're storing it directly in the widget as entry.placeholder.            
            # When Tkinter calls on_entry_click, it automatically passes the event object, and from that, 
            # you can access the Entry that triggered the event:
            
    def on_entry_click(self, event):
        """Remove placeholder text when entry gains focus."""
        entry = event.widget  # Get the widget that triggered the event
        if entry.get() == entry.placeholder:
            entry.delete(0, 'end')
            entry.config(fg='#003366')

    def on_focusout(self, event):
        """Restore placeholder text if entry is empty on losing focus."""
        entry = event.widget
        if entry.get() == '':
            entry.insert(0, entry.placeholder)
            entry.config(fg='gray')  # Placeholder color        
        
    
        