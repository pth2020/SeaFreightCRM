from tkinter import *

class Clearing:
    """ Clearing fields """
    
    def __init__(self, factory):
        self.factory = factory    
    
    def clear_fields(self):
        """ Clearing all fields """
        
        self.factory.fname_ent.delete(0, END)
        self.factory.lname_ent.delete(0, END)
        self.factory.mobile_ent.delete(0, END)
        self.factory.email_ent.delete(0, END)
        self.factory.sender_build_door_no_ent.delete(0, END)
        self.factory.sender_street_road_ent.delete(0, END)
        self.factory.sender_city_town_ent.delete(0, END)
        self.factory.sender_postcode_ent.delete(0, END)
        self.factory.dest_receiver_title_fullname_ent.delete(0, END)
        self.factory.dest_first_line_of_address_ent.delete(0, END)
        self.factory.dest_city_town_ent.delete(0, END)
        self.factory.dest_country.delete(0, END)
        self.factory.dest_mobile_ent.delete(0, END)
        self.factory.total_weight_ent.delete(0, END)
        self.factory.status_of_goods.set("Collected")
        self.factory.type_of_goods.set("Perishable")
        self.factory.receipt_text.delete("1.0", END)
        
        # Disable Clear button
        self.factory.btn_clear.config(state=DISABLED)
        # Disable Save button
        self.factory.btn_save.config(state=DISABLED) 
        # binding fields - displaying hints
        self.factory.bind_event()   
        
#Highlights
#Encapsulation: Separating clearing logic into its own class is excellent for maintainability and testing.
# Usage of self.factory: You're accessing widgets via self.factory, assuming the factory holds references 
# to all widgets — which is great.
# Setting default values: e.g., resetting status_of_goods and type_of_goods with .set(...) 
# shows you're working with StringVar, which is correct.

