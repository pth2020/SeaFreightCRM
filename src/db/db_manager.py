# # db_manager.py
# import sqlite3

# class DatabaseManager:
#     DB_PATH = "freight.db"

#     @staticmethod
#     def with_connection():
#         return sqlite3.connect(DatabaseManager.DB_PATH)  # works with "with" statement
    
import sqlite3
import os
import sys

# class DatabaseManager:
#     @staticmethod
#     def resource_path(relative_path):
#         """Get absolute path to resource (handles PyInstaller bundling)"""
#         try:
#             base_path = sys._MEIPASS  # Set by PyInstaller
#         except AttributeError:
#             base_path = os.path.abspath(".")
#         return os.path.join(base_path, relative_path)

#     DB_PATH = resource_path.__func__("src/db/freight.db")
#     #DB_PATH = resource_path.__func__("db/freight.db")

#     @staticmethod
#     def with_connection():
#         return sqlite3.connect(DatabaseManager.DB_PATH)
    
    
class DatabaseManager:
    DB_NAME = "freight.db"

    @staticmethod
    def get_database_path():
        # When bundled with PyInstaller, sys._MEIPASS is used for temp folder
        if hasattr(sys, '_MEIPASS'):
            # Access the database in the same directory as the .exe
            base_path = os.path.dirname(sys.executable)
        else:
            # Running from source (normal Python)
            base_path = os.path.dirname(__file__)
        
        return os.path.join(base_path, DatabaseManager.DB_NAME)

    @staticmethod
    def with_connection():
        db_path = DatabaseManager.get_database_path()
        return sqlite3.connect(db_path)