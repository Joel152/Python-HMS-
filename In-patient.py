import mysql.connector
import tkinter as tk
from tkinter import ttk, messagebox

# Establish the MySQL connection
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="1234",
    database="hms"
)
cursor = conn.cursor()

# Create the In-Patient (Ward) table if it doesn't exist
cursor.execute('''
CREATE TABLE IF NOT EXISTS InPatientWard (
    patient_number INT AUTO_INCREMENT PRIMARY KEY,
    patient_id INT,
    adm_reason VARCHAR(255),
    block ENUM('Block-A', 'Block-B', 'Block-C', 'Block-D') NOT NULL,
    room_bed VARCHAR(255),
    status ENUM('ADMITTED', 'Billed') DEFAULT 'ADMITTED',
    admitted_on DATE NOT NULL,
    FOREIGN KEY (patient_id) REFERENCES Patients(patient_id)
)
''')

# Functions for In-Patient Management
def add_in_patient():
    patient_id = entry_patient_id.get()
    adm_reason = entry_adm_reason.get()
    block = block_var.get()
    room_bed = entry_room_bed.get()
    status = status_var.get()
    admitted_on = entry_admitted_on.get()

    if not patient_id or not adm_reason or not block or not room_bed or not admitted_on:
        messagebox.showwarning("Input Error", "Please fill all required fields.")
        return

    query = "INSERT INTO InPatientWard (patient_id, adm_reason, block, room_bed, status, admitted_on) VALUES (%s, %s, %s, %s, %s, %s)"
    values = (int(patient_id), adm_reason, block, room_bed, status, admitted_on)
    cursor.execute(query, values)
    conn.commit()
    messagebox.showinfo("Success", "In-Patient added successfully.")
    entry_patient_id.delete(0, tk.END)
    entry_adm_reason.delete(0, tk.END)
    entry_room_bed.delete(0, tk.END)
    entry_admitted_on.delete(0, tk.END)
    display_patients_in_block()

# Function to display patients based on selected block
def display_patients_in_block():
    selected_block = block_var.get()
    query = "SELECT * FROM InPatientWard WHERE block = %s"
    cursor.execute(query, (selected_block,))
    patients = cursor.fetchall()

    patient_text.delete("1.0", tk.END)  # Clear previous text
    if patients:
        for patient in patients:
            patient_text.insert(tk.END, f"Patient ID: {patient[1]}, Admission Reason: {patient[2]}, Block: {patient[3]}, "
                                      f"Room/Beds: {patient[4]}, Status: {patient[5]}, Admitted On: {patient[6]}\n")
    else:
        patient_text.insert(tk.END, "No patients in this block.")

# GUI setup
root = tk.Tk()
root.title("Hospital Management System")
root.geometry("900x700")

# Create Notebook (Tabs)
notebook = ttk.Notebook(root)
notebook.pack(fill="both", expand=True)

# Create the In-Patient Tab
in_patient_frame = ttk.Frame(notebook)
notebook.add(in_patient_frame, text="In-Patient")

# In-Patient Admission Section
in_patient_frame_inner = tk.LabelFrame(in_patient_frame, text="In-Patient Admission", padx=10, pady=10)
in_patient_frame_inner.grid(row=0, column=0, padx=10, pady=10, sticky="n")

tk.Label(in_patient_frame_inner, text="Patient ID:").grid(row=0, column=0, sticky="w", pady=2)
entry_patient_id = tk.Entry(in_patient_frame_inner, width=30)
entry_patient_id.grid(row=0, column=1, pady=2)

tk.Label(in_patient_frame_inner, text="Admission Reason:").grid(row=1, column=0, sticky="w", pady=2)
entry_adm_reason = tk.Entry(in_patient_frame_inner, width=30)
entry_adm_reason.grid(row=1, column=1, pady=2)

tk.Label(in_patient_frame_inner, text="Block:").grid(row=2, column=0, sticky="w", pady=2)
block_var = tk.StringVar()
block_options = ['Block-A', 'Block-B', 'Block-C', 'Block-D']
block_dropdown = ttk.Combobox(in_patient_frame_inner, textvariable=block_var, values=block_options, state="normal", width=30)
block_dropdown.grid(row=2, column=1, pady=2)

tk.Label(in_patient_frame_inner, text="Room/Bed:").grid(row=3, column=0, sticky="w", pady=2)
entry_room_bed = tk.Entry(in_patient_frame_inner, width=30)
entry_room_bed.grid(row=3, column=1, pady=2)

tk.Label(in_patient_frame_inner, text="Status:").grid(row=4, column=0, sticky="w", pady=2)
status_var = tk.StringVar()
status_options = ['ADMITTED', 'Billed']
status_dropdown = ttk.Combobox(in_patient_frame_inner, textvariable=status_var, values=status_options, state="normal", width=30)
status_dropdown.set('ADMITTED')  # Default value
status_dropdown.grid(row=4, column=1, pady=2)

tk.Label(in_patient_frame_inner, text="Admitted On:").grid(row=5, column=0, sticky="w", pady=2)
entry_admitted_on = tk.Entry(in_patient_frame_inner, width=30)
entry_admitted_on.grid(row=5, column=1, pady=2)

tk.Button(in_patient_frame_inner, text="Add In-Patient", command=add_in_patient).grid(row=6, column=1, pady=10)

# Display Patients Section (By Block)
display_frame = tk.LabelFrame(in_patient_frame, text="Patients in Block", padx=10, pady=10)
display_frame.grid(row=1, column=1, padx=10, pady=10, sticky="nw")

# Dropdown for Block selection
block_label = tk.Label(display_frame, text="Select Block:")
block_label.grid(row=0, column=0, pady=5)

block_dropdown_display = ttk.Combobox(display_frame, textvariable=block_var, values=block_options, state="normal", width=30)
block_dropdown_display.grid(row=0, column=1, pady=5)
block_dropdown_display.bind("<<ComboboxSelected>>", lambda event: display_patients_in_block())

# Text widget to show patient list
patient_text = tk.Text(display_frame, height=12, width=50, wrap="word")
patient_text.grid(row=1, column=0, columnspan=2, pady=10)

# Run the main loop
root.mainloop()

# Close the MySQL connection when the GUI window is closed
cursor.close()
conn.close()
