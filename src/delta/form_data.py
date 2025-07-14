class FormData:
    """ Collect all form values or data from the GUI widgets """

    def __init__(self, factory):
        self.factory = factory

    def get_form_values(self):
        """ Collect all current values from the form widgets.
            Returns:
            dict: A dictionary with form field names as keys and current widget values as values.
        """
        return {
            "fname": self.factory.fname_ent.get(),
            "lname": self.factory.lname_ent.get(),
            "mobile": self.factory.mobile_ent.get(),
            "email": self.factory.email_ent.get(),
            "sender_build_door_no": self.factory.sender_build_door_no_ent.get(),
            "sender_street_road": self.factory.sender_street_road_ent.get(),
            "sender_city_town": self.factory.sender_city_town_ent.get(),
            "sender_postcode": self.factory.sender_postcode_ent.get(),
            "dest_receiver_title_fullname": self.factory.dest_receiver_title_fullname_ent.get(),
            "dest_first_line_of_address": self.factory.dest_first_line_of_address_ent.get(),
            "dest_city_town": self.factory.dest_city_town_ent.get(),
            "dest_country": self.factory.dest_country.get(),
            "dest_mobile": self.factory.dest_mobile_ent.get(),
            "goods_type": self.factory.type_of_goods.get(),
            "weight": self.factory.total_weight_ent.get(),
            "status": self.factory.status_of_goods.get()      
        }
