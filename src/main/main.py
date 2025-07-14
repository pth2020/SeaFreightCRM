from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
from db.db_manager import DatabaseManager
from delta.delta import Delta  
import sys
import os


class Appcontroller(Tk):
    def __init__(self):
        super().__init__()
        self.title("Sea Freight Management System")
        self.geometry("1540x800+0+0")  
        self.overrideredirect(True)  # This removes the title bar (and all buttons)
        
        # Creates tables if the tables don't exist
        self.create_users_table()
        self.create_country_price_table()

        # To hold frames and add/remove from as needed during frame switching 
        self.frames = {}
        self.show_login()  # Start by showing the login screen
        
        # Adjust to current window screen (e.g. Ipad, laptop, desktop screen etc.)
        self.screen_width = self.winfo_screenwidth()
        self.screen_height = self.winfo_screenheight()
        
    def resource_path(self,relative_path):
        """ Get absolute path to resource, works for dev and for PyInstaller """
        try:
            base_path = sys._MEIPASS  # PyInstaller temporary folder
        except Exception:
            base_path = os.path.abspath(".")  # Running normally

        return os.path.join(base_path, relative_path)

        
        
    def create_users_table(self):
        """ Create Users' table if it doesn't exist"""
        try:
            with DatabaseManager.with_connection() as conn: # Database connection imported from db module
                cursor = conn.cursor()
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT NOT NULL,
                        password TEXT NOT NULL
                    );
                """)
                # Insert a default user if none exist
                cursor.execute("SELECT COUNT(*) FROM users")
                if cursor.fetchone()[0] == 0:
                    cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", ("admin", "admin123"))
                conn.commit()
            
        except DatabaseManager.with_connection().Error as e:
            messagebox.showerror("Database Error", f"Could not initialize user table: {e}")
            
    def create_country_price_table(self):
        """ Creates a country_price table if it doesn't exist"""
        try:
            with DatabaseManager.with_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS country_price (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        country TEXT NOT NULL UNIQUE,
                        price FLOAT NOT NULL
                    );
                """)
                
                conn.commit()
        except DatabaseManager.with_connection().Error as e:
            messagebox.showerror("Database Error", f"Could not initialize country price table: {e}")

    def show_login(self):
        """ First frame (login frame ) to be shown """
        # Remove any existing frames
        for frame in self.frames.values(): 
            frame.place_forget() # if self.frames {} dictionary has any values

        # Create and show the LoginFrame
        self.frames["Login"] = LoginFrame(self, self.show_main) # creates instance of LoginFrame class (call to LoginFrame)
        # Passed arguments to the Login constructor — self (an instance of AppController) and self.show_main, which is a 
        # frame to be shown after a successful login. This is assigned to self.show_main_callback in the Login class, 
        # to be used later for navigation to the Delta (main) frame.
        self.frames["Login"].pack(fill="both", expand=True)  # Display LoginFrame        


    def show_main(self): # from login to DeltaFrame
        """ Helps navigate to main frame (DeltaFrame) upon successful login """
        self.switch_frame("Delta", Delta, self, self.show_login, self.show_admin)
        
    def show_delta_frame(self): # DeltaFrame (2 navigation buttons - exit and Open Admin)
        """Raise the main Delta frame with login and admin callbacks."""
        self.switch_frame("Delta", Delta, self, self.show_login, self.show_admin) 
        
        # Explanation of arguments passed to switch_frame:
        
        # "Delta"- Key of the frame (DeltaFrame) to store in self.frames and is used to track current frame
        # Delta - Class to instantiate (e.g. DeltaFrame)
        # self - Appcontroller instance, passed as 'master' (parameter in DeltaFrame) - (Tk root window) to Delta.
        # self - Same Appcontroller instance, passed as 'controller' (allows Delta to call app-level methods like logout, show_admin, etc.).
        # self.show_login - Callback for showing the login screen (typically used to return to login page after logout)
        # self.show_admin - Callback for showing the admin screen (used for navigation to AdminFrame).
        
        # login_callback vs return_callback 
        # login_callback - used to navigate to the login screen - used by frames that 
        # need a way to log the user out or return them to the login page.
        # return_callback - Used to return to the previous screen, or a main/home screen (not necessarily login).
        
        # Inside DeltaFrame class there is a constructor __init__(...)
        # def __init__(self, master, login_callback, admin_callback):
        # self.login_callback = login_callback
        # self.admin_callback = admin_callback
        # The above switch_frame calls DeltaFrame by passing these arguments into the Delta frame constructor:
        # Delta(self, self.show_login, self.show_admin)
        
        # show_main(self) vs show_delta_frame(self)
        # The real difference is context and intent, not the actual code:
        # Method	Purpose / When it's Called	Typical Source
        # show_main(self)	Called after successful login — it’s the "main entry point" into the app post-login	LoginFrame.authenticate()
        # show_delta_frame(self)	Called from within the app — usually to return to the main Delta screen from elsewhere (e.g., settings, admin)	AdminFrame, SettingsFrame, etc.


    def show_delta_dashboard(self): # bring up delta_dashboard from admin
        """Raise Delta frame, passing login/admin callbacks for Delta’s own “dashboard” logic."""
        # It's intended to bring up the dashboard portion of the Delta frame, after exiting Admin.
        self.switch_frame("Delta", Delta, self, self.show_login, self.show_admin)              

    def show_admin(self):
        from admin.admin import AdminFrame
        self.switch_frame("Admin", AdminFrame, self, self.show_delta_dashboard) # callback show_delta_dashboard
    
    def show_settings(self):
        self.switch_frame("Delta", Delta, self, self.show_login, self.show_admin) # callback admin

    def show_report(self):
        self.switch_frame("Delta", Delta, self, self.show_login, self.show_admin)

    def show_statistics(self):
        self.switch_frame("Delta", Delta, self, self.show_login, self.show_admin)

    def show_notes(self):
        self.switch_frame("Delta", Delta, self, self.show_login, self.show_admin)
        
    def logout(self):
        self.show_login()
        
    def switch_frame(self, name, frame_class, *args):
        for frame in self.frames.values():
            frame.destroy()
        self.frames = {}
        self.frames[name] = frame_class(self, *args)
        self.frames[name].pack(fill="both", expand=True)        

class LoginFrame(Frame):
    """To create a login system with a background image and authenticate from a database."""
    def __init__(self, master, show_main_callback):
        super(LoginFrame, self).__init__(master)
        self.master = master # Stores the parent widget for later use (e.g., to place child widgets).
        self.show_main_callback = show_main_callback  # Store the callback to switch to Delta
        self.create_background()
        self.create_widgets()

    def create_background(self):
        # Load and set the background image
        # The image is stored as a PIL.Image.Image object in self.bg_image.
        # Uses Pillow (PIL) to open an image file.
        img_path = self.master.resource_path("images/background_image.jpg")
        self.bg_image = Image.open(img_path)
        self.bg_image = self.bg_image.resize((1540, 800), Image.Resampling.LANCZOS)
        # Uses Image.Resampling.LANCZOS, which is a high-quality downsampling filter — good for preserving detail when resizing.
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)
        # Converts the PIL.Image.Image object into a PhotoImage that Tkinter can use in a Label, Canvas, etc.
        # Stores it in self.bg_photo so it can be used to display the image in the frame.

        # Background label
        self.bg_label = Label(self.master, image=self.bg_photo)
        self.bg_label.place(relwidth=1, relheight=1)

        # Login Frame (placed on top of background)
        self.login_frame = Frame(self.master, bg="white", padx=20, pady=20, bd=5, relief=RIDGE)
        self.login_frame.place(relx=0.5, rely=0.5, anchor="center")

    def create_widgets(self):
        # Login label
        Label(self.login_frame, text="User Login", font=("Arial", 24, "bold"), bg="white", fg="#003366").grid(row=0, column=1, columnspan=2, pady=20, sticky=W)

        # Username
        Label(self.login_frame, text="Username:", font=("Arial", 14), bg="white").grid(row=1, column=0, padx=10, pady=10, sticky=W)
        self.username_ent = Entry(self.login_frame, font=("Arial", 14), width=25)
        self.username_ent.grid(row=1, column=1, columnspan=2, padx=10, pady=5)

        # Password
        Label(self.login_frame, text="Password:", font=("Arial", 14), bg="white").grid(row=2, column=0, padx=10, pady=10, sticky=W)
        self.password_ent = Entry(self.login_frame, show="*", font=("Arial", 14), width=25)
        self.password_ent.grid(row=2, column=1, columnspan=2, padx=10, pady=10)

        # Login button
        self.login_btn = Button(self.login_frame, text="Login", font=("Arial", 14), bg="#003366", fg="white", width=10, command=self.authenticate)
        self.login_btn.grid(row=3, column=1, pady=(5, 5))  # Adds a small vertical gap after the login button
        self.login_btn.config(state=DISABLED)

        # Exit button (below Login button)
        self.exit_btn = Button(self.login_frame, text="Exit", font=("Arial", 14), bg="darkred", fg="white", width=10, command=self.master.quit)
        self.exit_btn.grid(row=3, column=2, pady=(5, 5))  # Adds a small vertical gap before the exit button

        # Bind Entry events to check if entries are filled out
        key_release_event = "<KeyRelease>"
        self.username_ent.bind(key_release_event, self.check_entries)
        self.password_ent.bind(key_release_event, self.check_entries)

    def check_entries(self, event=None):
        # Check if both username and password are filled
        if self.username_ent.get().strip() != "" and self.password_ent.get().strip() != "":
            self.login_btn.config(state=NORMAL)
        else:
            self.login_btn.config(state=DISABLED)

    def authenticate(self):
        username = self.username_ent.get()
        password = self.password_ent.get()
        print(username, password)

        if self.verify_credentials(username, password):
            # messagebox.showinfo("Login Success", "Welcome!")
            self.show_main_callback()  # Transition to Delta only after successful login
        else:
            messagebox.showerror("Login Failed", "Invalid username or password.")
    

    def verify_credentials(self, username, password):
        try:
            with DatabaseManager.with_connection() as conn:
                cursor = conn.cursor()
                # Ensure the users table exists
                cursor.execute(""" 
                    CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT NOT NULL,
                        password TEXT NOT NULL
                    );
                """)

                # Check if the entered username and password match
                cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
                user = cursor.fetchone()  # Fetch the first result

                # Return True if user is found, otherwise False
                if user:
                    print(user)
                    return True
                else:
                    return False
        except DatabaseManager.with_connection().Error as e:
            messagebox.showerror("Database Error", f"An error occurred: {e}")
            return False

if __name__ == "__main__":
    app = Appcontroller()  # Create an instance of Appcontroller
    app.mainloop()  # Start the Tkinter main loop