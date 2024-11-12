import mysql.connector
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

# Establish the MySQL connection
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="1234",
    database="hms"
)
cursor = conn.cursor()

# Create the Staff table if it doesn't exist
cursor.execute('''
CREATE TABLE IF NOT EXISTS Staff (
    staff_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255),
    login_name VARCHAR(255),
    login_password VARCHAR(255),
    department VARCHAR(255),
    primary_role VARCHAR(255),
    additional_roles VARCHAR(255)
)
''')

# Predefined roles for the dropdown
high_level_roles = ["Medical Director (Head of Hospital)", "Chief of Staff", "Nursing Director", "Head of Departments (HoDs)", 
                    "Director of Patient Services", "Chief Financial Officer (CFO)"]
mid_level_roles = ["Resident Medical Officer (RMO)", "Nurse Supervisor", "Emergency Department Shift Lead", "Patient Admission Officer", 
                   "Lab Manager", "Pharmacy Supervisor"]
entry_level_roles = ["Staff Nurse", "Patient Care Assistant", "Receptionist", "Billing Officer", "Medical Records Clerk", "Housekeeping"]

# Department mapping based on roles
role_to_department = {
    "Staff Nurse": "Nursing",
    "Patient Care Assistant": "Nursing",
    "Receptionist": "Front Desk / Admissions",
    "Billing Officer": "Finance / Billing Department",
    "Medical Records Clerk": "Medical Records",
    "Housekeeping": "Facilities"
}

# Staff Management Functions
def add_staff():
    name = entry_staff_name.get()
    login_name = entry_login_name.get()
    login_password = entry_login_password.get()
    department = department_var.get()
    primary_role = primary_role_var.get()
    additional_roles = additional_roles_var.get()

    if not name or not login_name or not login_password or not department:
        messagebox.showwarning("Input Error", "Please fill all required fields.")
        return

    query = "INSERT INTO Staff (name, login_name, login_password, department, primary_role, additional_roles) VALUES (%s, %s, %s, %s, %s, %s)"
    values = (name, login_name, login_password, department, primary_role, additional_roles)
    cursor.execute(query, values)
    conn.commit()
    messagebox.showinfo("Success", "Staff added successfully.")
    entry_staff_name.delete(0, tk.END)
    entry_login_name.delete(0, tk.END)
    entry_login_password.delete(0, tk.END)

def view_all_staff():
    cursor.execute("SELECT * FROM Staff")
    staff_records = cursor.fetchall()
    staff_text.delete("1.0", tk.END)
    for staff in staff_records:
        staff_text.insert(tk.END, f"ID: {staff[0]}, Name: {staff[1]}, Login Name: {staff[2]}, Department: {staff[3]}, "
                                  f"Primary Role: {staff[4]}, Additional Roles: {staff[5]}\n")

# GUI setup
root = tk.Tk()
root.title("Hospital Management System")
root.geometry("900x700")

# Staff Management Section
staff_frame = tk.LabelFrame(root, text="Staff Management", padx=10, pady=10)
staff_frame.grid(row=0, column=1, padx=10, pady=10, sticky="n")

tk.Label(staff_frame, text="Name:").grid(row=0, column=0, sticky="w", pady=2)
entry_staff_name = tk.Entry(staff_frame, width=30)
entry_staff_name.grid(row=0, column=1, pady=2)

tk.Label(staff_frame, text="Login Name:").grid(row=1, column=0, sticky="w", pady=2)
entry_login_name = tk.Entry(staff_frame, width=30)
entry_login_name.grid(row=1, column=1, pady=2)

tk.Label(staff_frame, text="Login Password:").grid(row=2, column=0, sticky="w", pady=2)
entry_login_password = tk.Entry(staff_frame, width=30, show="*")  # Password entry (hidden text)
entry_login_password.grid(row=2, column=1, pady=2)

# Primary Role Dropdown with non-selectable category labels
tk.Label(staff_frame, text="Primary Role:").grid(row=4, column=0, sticky="w", pady=2)

primary_role_var = tk.StringVar()

# Merge the high, mid, and entry-level roles into one list with non-selectable placeholders
primary_role_options = ["High-Level Management Roles"] + high_level_roles + \
                        ["Mid-Level Roles"] + mid_level_roles + \
                        ["Entry-Level Roles"] + entry_level_roles

primary_role_dropdown = ttk.Combobox(staff_frame, textvariable=primary_role_var, values=primary_role_options, state="normal", width=40)
primary_role_dropdown.grid(row=4, column=1, pady=2)

# Add event to disable category items
def on_primary_role_select(event):
    selected_value = primary_role_var.get()
    if selected_value in ["High-Level Management Roles", "Mid-Level Roles", "Entry-Level Roles"]:
        primary_role_var.set("")  # Clear the selection if category label is selected
        messagebox.showwarning("Invalid Selection", "Please select a valid role under the categories.")
    else:
        # Automatically update the department based on the selected primary role
        department_var.set(role_to_department.get(selected_value, ""))

primary_role_dropdown.bind("<<ComboboxSelected>>", on_primary_role_select)

# Department Dropdown (automatically selected based on role)
tk.Label(staff_frame, text="Department:").grid(row=3, column=0, sticky="w", pady=2)

department_var = tk.StringVar()
department_options = ["Nursing", "Front Desk / Admissions", "Finance / Billing Department", "Medical Records", "Facilities"]
department_dropdown = ttk.Combobox(staff_frame, textvariable=department_var, values=department_options, state="readonly", width=40)
department_dropdown.grid(row=3, column=1, pady=2)

# Additional Roles Dropdown (similar to Primary Role)
tk.Label(staff_frame, text="Additional Roles:").grid(row=5, column=0, sticky="w", pady=2)

additional_roles_var = tk.StringVar()

additional_roles_options = ["High-Level Management Roles"] + high_level_roles + \
                           ["Mid-Level Roles"] + mid_level_roles + \
                           ["Entry-Level Roles"] + entry_level_roles

additional_roles_dropdown = ttk.Combobox(staff_frame, textvariable=additional_roles_var, values=additional_roles_options, state="normal", width=40)
additional_roles_dropdown.grid(row=5, column=1, pady=2)

# Add event to disable category items for Additional Roles
def on_additional_roles_select(event):
    selected_value = additional_roles_var.get()
    if selected_value in ["High-Level Management Roles", "Mid-Level Roles", "Entry-Level Roles"]:
        additional_roles_var.set("")  # Clear the selection if category label is selected
        messagebox.showwarning("Invalid Selection", "Please select a valid additional role under the categories.")

additional_roles_dropdown.bind("<<ComboboxSelected>>", on_additional_roles_select)

tk.Button(staff_frame, text="Add Staff", command=add_staff).grid(row=6, column=1, pady=10)

# Show All Staff Section
show_staff_frame = tk.LabelFrame(root, text="All Staff", padx=10, pady=10)
show_staff_frame.grid(row=1, column=1, padx=10, pady=10, sticky="nw")

staff_text = tk.Text(show_staff_frame, height=12, width=50, wrap="word")
staff_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
staff_scroll = tk.Scrollbar(show_staff_frame, command=staff_text.yview)
staff_scroll.pack(side=tk.RIGHT, fill=tk.Y)
staff_text.config(yscrollcommand=staff_scroll.set)

tk.Button(show_staff_frame, text="View All Staff", command=view_all_staff).pack(pady=5)

# Run the main loop
root.mainloop()

# Close the MySQL connection when the GUI window is closed
cursor.close()
conn.close()
