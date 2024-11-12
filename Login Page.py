import mysql.connector
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

# Establish MySQL connection
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="1234",
    database="hms"
)
cursor = conn.cursor()

# Function to validate login credentials
def validate_login():
    username = entry_username.get()
    password = entry_password.get()

    # Validate if the username and password fields are not empty
    if not username or not password:
        messagebox.showwarning("Input Error", "Please enter both username and password.")
        return

    # Query to check if username and password exist in the database
    query = "SELECT * FROM Staff WHERE login_name = %s AND login_password = %s"
    cursor.execute(query, (username, password))
    result = cursor.fetchone()

    if result:
        messagebox.showinfo("Login Successful", "Welcome to the Hospital Management System.")
        root.destroy()  # Close the login window
        open_main_app(result[4])  # Pass primary_role to open the main app based on the role
    else:
        messagebox.showerror("Login Failed", "Invalid username or password.")

# Function to open the main app after successful login
def open_main_app(role):
    main_app = tk.Tk()
    main_app.title("Hospital Management System")

    # Create tabs using a notebook widget (for a multi-tab layout)
    notebook = ttk.Notebook(main_app)
    notebook.pack(fill="both", expand=True)

    # Example of different tabs based on the role
    if role == "Medical Director (Head of Hospital)":
        medical_director_tab = ttk.Frame(notebook)
        notebook.add(medical_director_tab, text="Medical Director")
        tk.Label(medical_director_tab, text="Medical Director Panel").pack(pady=20)

    elif role == "Chief of Staff":
        chief_of_staff_tab = ttk.Frame(notebook)
        notebook.add(chief_of_staff_tab, text="Chief of Staff")
        tk.Label(chief_of_staff_tab, text="Chief of Staff Panel").pack(pady=20)

    # Add common tabs (for all users)
    staff_management_tab = ttk.Frame(notebook)
    notebook.add(staff_management_tab, text="Staff Management")
    tk.Label(staff_management_tab, text="Manage Staff").pack(pady=20)

    patient_management_tab = ttk.Frame(notebook)
    notebook.add(patient_management_tab, text="Patient Management")
    tk.Label(patient_management_tab, text="Manage Patients").pack(pady=20)

    # Additional common tabs, such as for billing, appointments, etc.

    main_app.geometry("900x700")
    main_app.mainloop()

# Create login window
root = tk.Tk()
root.title("Hospital Management System - Login")
root.geometry("400x300")

# Username and Password fields
tk.Label(root, text="Username:").pack(pady=10)
entry_username = tk.Entry(root, width=30)
entry_username.pack(pady=5)

tk.Label(root, text="Password:").pack(pady=10)
entry_password = tk.Entry(root, show="*", width=30)
entry_password.pack(pady=5)

# Login button
tk.Button(root, text="Login", command=validate_login).pack(pady=20)

# Run the login window
root.mainloop()

# Close the MySQL connection when the application is closed
cursor.close()
conn.close()
