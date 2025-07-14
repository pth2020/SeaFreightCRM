





# To write a test for inserting data into a SQLite database using Python, you typically want to:

# Set up an in-memory database (so you don’t write to disk).

# Create the schema (tables).

# Insert test data.

# Verify the data was inserted correctly.

# Tear down the connection cleanly.

# ✅ Example: Let's Say You Have This Insert Function

# import sqlite3

# def insert_user(conn, name, email):
#     cursor = conn.cursor()
#     cursor.execute("INSERT INTO users (name, email) VALUES (?, ?)", (name, email))
#     conn.commit()
# 🧪 Unit Test for insert_user
# python
# Copy
# Edit
# import unittest
# import sqlite3
# from your_module import insert_user  # replace with your actual module name

# class TestDatabaseInsert(unittest.TestCase):
#     def setUp(self):
#         # Create an in-memory SQLite database
#         self.conn = sqlite3.connect(":memory:")
#         self.create_table()

#     def create_table(self):
#         cursor = self.conn.cursor()
#         cursor.execute("""
#             CREATE TABLE users (
#                 id INTEGER PRIMARY KEY AUTOINCREMENT,
#                 name TEXT NOT NULL,
#                 email TEXT NOT NULL
#             )
#         """)
#         self.conn.commit()

#     def test_insert_user(self):
#         insert_user(self.conn, "Alice", "alice@example.com")

#         cursor = self.conn.cursor()
#         cursor.execute("SELECT * FROM users WHERE name = ?", ("Alice",))
#         result = cursor.fetchone()

#         self.assertIsNotNone(result)
#         self.assertEqual(result[1], "Alice")
#         self.assertEqual(result[2], "alice@example.com")

#     def tearDown(self):
#         self.conn.close()

# if __name__ == "__main__":
#     unittest.main()
# 💡 Notes
# :memory:: This creates a temporary database in RAM — fast and disposable.

# setUp / tearDown: These ensure your tests are isolated and clean.

# fetchone(): Used to confirm that the row exists and contains the correct data.