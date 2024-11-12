import mysql.connector
import tkinter as tk
from tkinter import messagebox

# Establish the MySQL connection
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="1234",
    database="hms"
)
cursor = conn.cursor()

# Create the Patients table if it doesn't exist
cursor.execute('''
CREATE TABLE IF NOT EXISTS Patients (
    patient_id INT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    age INT NOT NULL,
    contact_info VARCHAR(255) NOT NULL,
    medical_history TEXT
);
''')

# Functions
def add_patient():
    name = entry_name.get()
    age = entry_age.get()
    contact_info = entry_contact.get()
    patient_id = entry_patient_id.get()
    medical_history = entry_history.get()

    if not name or not age or not contact_info or not patient_id:
        messagebox.showwarning("Input Error", "Please fill all required fields.")
        return

    query = "INSERT INTO Patients (patient_id, name, age, contact_info, medical_history) VALUES (%s, %s, %s, %s, %s)"
    values = (int(patient_id), name, int(age), contact_info, medical_history)
    cursor.execute(query, values)
    conn.commit()
    messagebox.showinfo("Success", "Patient added successfully.")
    
    # Clear the fields after adding the patient
    entry_name.delete(0, tk.END)
    entry_age.delete(0, tk.END)
    entry_contact.delete(0, tk.END)
    entry_history.delete(0, tk.END)
    entry_patient_id.delete(0, tk.END)

# GUI setup
root = tk.Tk()
root.title("Hospital Management System")
root.geometry("800x600")

# Patient Information Section
patient_frame = tk.LabelFrame(root, text="Patient Information", padx=10, pady=10)
patient_frame.grid(row=0, column=0, padx=10, pady=10, sticky="n")

tk.Label(patient_frame, text="Patient Name:").grid(row=0, column=0, sticky="w", pady=2)
entry_name = tk.Entry(patient_frame, width=30)
entry_name.grid(row=0, column=1, pady=2)

tk.Label(patient_frame, text="Age:").grid(row=1, column=0, sticky="w", pady=2)
entry_age = tk.Entry(patient_frame, width=30)
entry_age.grid(row=1, column=1, pady=2)

tk.Label(patient_frame, text="Contact Info:").grid(row=2, column=0, sticky="w", pady=2)
entry_contact = tk.Entry(patient_frame, width=30)
entry_contact.grid(row=2, column=1, pady=2)

tk.Label(patient_frame, text="Patient ID:").grid(row=3, column=0, sticky="w", pady=2)
entry_patient_id = tk.Entry(patient_frame, width=30)
entry_patient_id.grid(row=3, column=1, pady=2)

tk.Label(patient_frame, text="Medical History:").grid(row=4, column=0, sticky="w", pady=2)
entry_history = tk.Entry(patient_frame, width=30)
entry_history.grid(row=4, column=1, pady=2)

tk.Button(patient_frame, text="Add Patient", command=add_patient).grid(row=5, column=1, pady=10)

# Run the main loop
root.mainloop()

# Close the MySQL connection when the GUI window is closed
cursor.close()
conn.close()
