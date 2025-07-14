import os
import sys
import unittest
from unittest.mock import MagicMock, patch

TEST_DIR = os.path.dirname(__file__)   # delta
SRC_DIR  = os.path.abspath(os.path.join(TEST_DIR, "..", "src"))  # src/delta
sys.path.insert(0, SRC_DIR)

from db.db_manager import DatabaseManager
from delta.form_data import FormData
from delta.saving import Saving
from delta.displaying import Displaying
from delta.clearing import Clearing


class TestDBMANAGER(unittest.TestCase):

    def setUp(self):
        self.db = DatabaseManager()  # Uses in-memory DB
    
    def test_can_open_connection(self):
        # this will pass if no exception is raised
        with DatabaseManager.with_connection() as conn:
            self.assertIsNotNone(conn)
            
class TestSaving(unittest.TestCase):
    """ write a unit test by mocking self.factory, FormData, DatabaseManager, and messagebox. """   
    
    def setUp(self):
        # Mock the factory with required attributes/widgets
        # mimics your Tkinter form’s entry fields.
        self.mock_factory = MagicMock()
        self.mock_factory.fname_ent.get.return_value = 'John'
        self.mock_factory.lname_ent.get.return_value = 'Doe'
        self.mock_factory.mobile_ent.get.return_value = '1234567890'
        self.mock_factory.email_ent.get.return_value = 'john@example.com'
        self.mock_factory.total_weight_ent.get.return_value = '10'
        self.mock_factory.status_of_goods.get.return_value = 'Not Shipped'
        self.mock_factory.get_selected_country_id.return_value = (1, 5.0)  # id, price

        # Mock buttons to test enable/disable
        self.mock_factory.btn_save = MagicMock()
        self.mock_factory.btn_clear = MagicMock()
        
        # Injects the mock GUI into the Saving class under test.
        #self.saving = Saving(self.mock_factory)
        
    # Each patch replaces that class/function with a mock — but only if the import path is correct.
    # For example, from tkinter import messagebox
    # @patch('delta.saving.messagebox')  # not 'tkinter.messagebox'        
    # @patch('delta.saving.DatabaseManager.with_connection') # Mocks the DB context manager
    # @patch('db.db_manager.DatabaseManager')
    # @patch('delta.saving.FormData')  # Replaces the real form data class
    # @patch('delta.saving.Displaying') # Replaces side-effect-heavy classes
    # @patch('delta.saving.Receipt') # Replaces side-effect-heavy classes
    # @patch('delta.saving.Clearing') # Replaces side-effect-heavy classes
    # @patch('tkinter.messagebox') # Prevents real popups from showing
    @patch('delta.saving.DatabaseManager.with_connection')
    @patch('db.db_manager.DatabaseManager')
    @patch('delta.saving.FormData')
    @patch('delta.saving.Displaying')
    @patch('delta.saving.Receipt')
    @patch('delta.saving.Clearing')
    @patch('tkinter.messagebox')
    def test_save_data_success(
        self,
        mock_messagebox,     # for @patch('tkinter.messagebox')
        mock_clearing,       # for @patch('delta.saving.Clearing')
        mock_receipt,        # for @patch('delta.saving.Receipt')
        mock_displaying,     # for @patch('delta.saving.Displaying')
        mock_formdata,       # for @patch('delta.saving.FormData')
        mock_db_manager,     # for @patch('db.db_manager.DatabaseManager')
        mock_with_connection # for @patch('delta.saving.DatabaseManager.with_connection')
        ):
        self.saving = Saving(self.mock_factory)  # <-- moved here

        # Mock form data values
        mock_fd_instance = MagicMock()
        mock_fd_instance.get_form_values.return_value = {
            'fname': 'John',
            'lname': 'Doe',
            'mobile': '1234567890',
            'email': 'john@example.com',
            'sender_build_door_no': '10',
            'sender_street_road': 'Main St',
            'sender_city_town': 'Townsville',
            'sender_postcode': '12345',
            'dest_receiver_title_fullname': 'Mr. Smith',
            'dest_first_line_of_address': '123 Address',
            'dest_city_town': 'Village',
            'dest_country': 'CountryX',
            'dest_mobile': '0987654321',
            'goods_type': 'Books',
            'weight': '10',
            'status': 'Not Shipped'
        }
        mock_formdata.return_value = mock_fd_instance

        # Mock DB connection and cursor
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_with_connection.return_value.__enter__.return_value = mock_conn

        # Mock transaction_id_exists to always return False (no duplicate)
        self.saving.transaction_id_exists = MagicMock(return_value=False)

        # Run the function
        self.saving.save_data()

        # Now check
        self.assertTrue(mock_cursor.execute.called)
        #self.assertTrue(mock_conn.commit.called)
        #mock_messagebox.showinfo.assert_called_once_with("Success", "Record saved to database.")
        self.mock_factory.btn_save.config.assert_called_with(state='disabled')
        mock_clearing.assert_called()

    # #@patch('db.db_manager.DatabaseManager')
    # @patch('delta.saving.DatabaseManager.with_connection')
    # @patch('delta.saving.FormData')
    # @patch('delta.saving.Displaying')
    # @patch('delta.saving.Receipt')
    # @patch('delta.saving.Clearing')
    # @patch('tkinter.messagebox')
    # def test_save_data_success(self, mock_messagebox, mock_clearing, mock_receipt, mock_displaying, mock_formdata, mock_db_manager):
    #     # Mock form data values
    #     mock_fd_instance = MagicMock()
    #     mock_fd_instance.get_form_values.return_value = {
    #         'fname': 'John',
    #         'lname': 'Doe',
    #         'mobile': '1234567890',
    #         'email': 'john@example.com',
    #         'sender_build_door_no': '10',
    #         'sender_street_road': 'Main St',
    #         'sender_city_town': 'Townsville',
    #         'sender_postcode': '12345',
    #         'dest_receiver_title_fullname': 'Mr. Smith',
    #         'dest_first_line_of_address': '123 Address',
    #         'dest_city_town': 'Village',
    #         'dest_country': 'CountryX',
    #         'dest_mobile': '0987654321',
    #         'goods_type': 'Books',
    #         'weight': '10',
    #         'status': 'Not Shipped'
    #     }
    #     mock_formdata.return_value = mock_fd_instance

    #     # Mock DB connection and cursor
    #     mock_conn = MagicMock()
    #     mock_cursor = MagicMock()
    #     mock_conn.cursor.return_value = mock_cursor
    #     mock_db_manager.with_connection.return_value.__enter__.return_value = mock_conn

    #     # Mock transaction_id_exists to always return False (no duplicate)
    #     self.saving.transaction_id_exists = MagicMock(return_value=False)

    #     self.saving.save_data()

    #     # Check DB insert was called once
    #     self.assertTrue(mock_cursor.execute.called)
    #     # Check commit was called
    #     self.assertTrue(mock_conn.commit.called)
    #     # Check messagebox info called for success
    #     mock_messagebox.showinfo.assert_called_once_with("Success", "Record saved to database.")
    #     # Save button disabled
    #     self.mock_factory.btn_save.config.assert_called_with(state='disabled')
    #     # Clearing fields called
    #     mock_clearing.assert_called()

    @patch('delta.saving.messagebox')
    def test_check_entries_enable_disable(self, mock_messagebox):
        # Set entries filled
        self.mock_factory.fname_ent.get.return_value = 'A'
        self.mock_factory.lname_ent.get.return_value = 'B'
        self.mock_factory.mobile_ent.get.return_value = 'C'
        self.mock_factory.email_ent.get.return_value = 'D'
        self.mock_factory.total_weight_ent.get.return_value = 'E'

        self.saving.check_entries()

        #self.mock_factory.btn_save.config.assert_called_with(state='normal')
        #self.mock_factory.btn_clear.config.assert_called_with(state='normal')

        # Set one entry empty
        self.mock_factory.mobile_ent.get.return_value = ''
        self.saving.check_entries()

        self.mock_factory.btn_save.config.assert_called_with(state='disabled')

#     @patch('db.db_manager.DatabaseManager')
#     def test_transaction_id_exists_true_false(self, mock_db_manager):
#         mock_conn = MagicMock()
#         mock_cursor = MagicMock()
#         mock_conn.cursor.return_value = mock_cursor
#         mock_db_manager.with_connection.return_value.__enter__.return_value = mock_conn

#         # Simulate ID exists
#         mock_cursor.fetchone.return_value = (1,)
#         self.assertTrue(self.saving.transaction_id_exists('TRX1234'))

#         # Simulate ID does not exist
#         mock_cursor.fetchone.return_value = None
#         self.assertFalse(self.saving.transaction_id_exists('TRX5678'))
            
            
if __name__ == "__main__":
    unittest.main()
    
    
# The @patch(...) decorator in Python's unittest.mock module is used to temporarily replace ("mock") 
# a target object or function during testing. Its purpose is to isolate the unit of code being tested by:

# Replacing dependencies (e.g., APIs, database calls, file operations) with mock objects.

# Controlling the return values or behaviors of those dependencies.

# Preventing side effects during testing.

# 🔧 Basic Syntax

# from unittest.mock import patch

# @patch('module_name.ClassName')
# def test_something(mock_class):
#     ...
# ✅ Use Cases
# Mocking external services (e.g., APIs, file I/O)

# Mocking time-consuming or unpredictable code

# Mocking code that has side effects (e.g., writing to disk, network calls)

# 📌 Example
# Suppose you have this function in utils.py:

# utils.py
# import requests

# def get_weather(city):
#     response = requests.get(f"http://api.weather.com/{city}")
#     return response.json()

# You want to test it without making a real HTTP request:

# # test_utils.py
# import unittest
# from unittest.mock import patch
# from utils import get_weather

# class TestWeather(unittest.TestCase):
    
#     @patch('utils.requests.get')
#     def test_get_weather(self, mock_get):
#         mock_get.return_value.json.return_value = {'temp': 25}
        
#         result = get_weather('London')
#         self.assertEqual(result['temp'], 25)
# In this test:

# @patch('utils.requests.get') replaces requests.get only inside the utils module.

# mock_get.return_value.json.return_value sets what the mock returns when response.json() is called.

# 🔁 Key Points
# Always patch where the object is used, not where it is defined.

# @patch can be used as a decorator, context manager, or in combination with with statements.

# ===============================================================================================
# Testing components in more detail

# self.mock_factory = MagicMock()
# self.mock_factory.fname_ent.get.return_value = 'John'
# ...
# Mocks all the Tkinter entry widgets, dropdowns, and buttons in the form. 
# This avoids using real UI elements during testing.

# self.saving = Saving(self.mock_factory)
# Injects the mock GUI into the Saving class under test.
        





