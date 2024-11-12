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

# Functions
def add_patient():
    name = entry_name.get()
    age = entry_age.get()
    contact_info = entry_contact.get()
    medical_history = entry_history.get()

    if not name or not age or not contact_info:
        messagebox.showwarning("Input Error", "Please fill all required fields.")
        return

    query = "INSERT INTO Patients (name, age, contact_info, medical_history) VALUES (%s, %s, %s, %s)"
    values = (name, int(age), contact_info, medical_history)
    cursor.execute(query, values)
    conn.commit()
    messagebox.showinfo("Success", "Patient added successfully.")
    entry_name.delete(0, tk.END)
    entry_age.delete(0, tk.END)
    entry_contact.delete(0, tk.END)
    entry_history.delete(0, tk.END)

def show_doctors():
    cursor.execute("SELECT doctor_id, name, specialization FROM Doctors")
    doctors = cursor.fetchall()
    doctor_text.delete("1.0", tk.END)
    for doc in doctors:
        doctor_text.insert(tk.END, f"ID: {doc[0]}, Name: {doc[1]}, Specialization: {doc[2]}\n")

def assign_doctor():
    patient_id = int(entry_patient_id.get())
    doctor_id = int(entry_doctor_id.get())
    diagnosis = entry_diagnosis.get()
    medications = entry_medications.get()

    if not diagnosis or not medications:
        messagebox.showwarning("Input Error", "Please fill all required fields.")
        return

    query = "INSERT INTO Treatments (patient_id, doctor_id, diagnosis, medications, treatment_date) VALUES (%s, %s, %s, %s, NOW())"
    values = (patient_id, doctor_id, diagnosis, medications)
    cursor.execute(query, values)
    conn.commit()
    messagebox.showinfo("Success", "Doctor assigned and treatment created successfully.")

def show_treatments():
    patient_id = int(entry_patient_id.get())
    query = "SELECT treatment_id, diagnosis, medications, treatment_date FROM Treatments WHERE patient_id = %s"
    cursor.execute(query, (patient_id,))
    treatments = cursor.fetchall()

    treatment_text.delete("1.0", tk.END)
    for treatment in treatments:
        treatment_text.insert(tk.END, f"ID: {treatment[0]}, Diagnosis: {treatment[1]}, Medications: {treatment[2]}, Date: {treatment[3]}\n")

def generate_bill():
    patient_id = int(entry_patient_id.get())
    treatment_id = int(entry_treatment_id.get())
    amount = float(entry_amount.get())
    payment_status = entry_payment_status.get()

    query = "INSERT INTO Billing (patient_id, treatment_id, amount, payment_status) VALUES (%s, %s, %s, %s)"
    values = (patient_id, treatment_id, amount, payment_status)
    cursor.execute(query, values)
    conn.commit()
    messagebox.showinfo("Success", "Bill generated successfully.")

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

tk.Label(patient_frame, text="Medical History:").grid(row=3, column=0, sticky="w", pady=2)
entry_history = tk.Entry(patient_frame, width=30)
entry_history.grid(row=3, column=1, pady=2)

tk.Button(patient_frame, text="Add Patient", command=add_patient).grid(row=4, column=1, pady=10)

# Doctors Section with Text widget and Scrollbar
doctor_frame = tk.LabelFrame(root, text="Doctors", padx=10, pady=10)
doctor_frame.grid(row=0, column=1, padx=10, pady=10, sticky="n")

doctor_text = tk.Text(doctor_frame, height=8, width=40, wrap="word")
doctor_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
doctor_scroll = tk.Scrollbar(doctor_frame, command=doctor_text.yview)
doctor_scroll.pack(side=tk.RIGHT, fill=tk.Y)
doctor_text.config(yscrollcommand=doctor_scroll.set)

tk.Button(doctor_frame, text="Show Doctors", command=show_doctors).pack(pady=5)

# Treatment Section with Text widget and Scrollbar
treatment_frame = tk.LabelFrame(root, text="Treatment Information", padx=10, pady=10)
treatment_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nw")

tk.Label(treatment_frame, text="Patient ID:").grid(row=0, column=0, sticky="w", pady=2)
entry_patient_id = tk.Entry(treatment_frame, width=30)
entry_patient_id.grid(row=0, column=1, pady=2)

tk.Label(treatment_frame, text="Doctor ID:").grid(row=1, column=0, sticky="w", pady=2)
entry_doctor_id = tk.Entry(treatment_frame, width=30)
entry_doctor_id.grid(row=1, column=1, pady=2)

tk.Label(treatment_frame, text="Diagnosis:").grid(row=2, column=0, sticky="w", pady=2)
entry_diagnosis = tk.Entry(treatment_frame, width=30)
entry_diagnosis.grid(row=2, column=1, pady=2)

tk.Label(treatment_frame, text="Medications:").grid(row=3, column=0, sticky="w", pady=2)
entry_medications = tk.Entry(treatment_frame, width=30)
entry_medications.grid(row=3, column=1, pady=2)

tk.Button(treatment_frame, text="Assign Doctor and Treatment", command=assign_doctor).grid(row=4, column=1, pady=10)

# Show Treatments Section with Text widget and Scrollbar
show_treatments_frame = tk.LabelFrame(root, text="Treatments", padx=10, pady=10)
show_treatments_frame.grid(row=1, column=1, padx=10, pady=10, sticky="nw")

treatment_text = tk.Text(show_treatments_frame, height=8, width=40, wrap="word")
treatment_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
treatment_scroll = tk.Scrollbar(show_treatments_frame, command=treatment_text.yview)
treatment_scroll.pack(side=tk.RIGHT, fill=tk.Y)
treatment_text.config(yscrollcommand=treatment_scroll.set)

tk.Button(show_treatments_frame, text="Show Treatments", command=show_treatments).pack(pady=5)

# Billing Section
billing_frame = tk.LabelFrame(root, text="Billing", padx=10, pady=10)
billing_frame.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky="n")

tk.Label(billing_frame, text="Treatment ID:").grid(row=0, column=0, sticky="w", pady=2)
entry_treatment_id = tk.Entry(billing_frame, width=30)
entry_treatment_id.grid(row=0, column=1, pady=2)

tk.Label(billing_frame, text="Amount:").grid(row=1, column=0, sticky="w", pady=2)
entry_amount = tk.Entry(billing_frame, width=30)
entry_amount.grid(row=1, column=1, pady=2)

tk.Label(billing_frame, text="Payment Status:").grid(row=2, column=0, sticky="w", pady=2)
entry_payment_status = tk.Entry(billing_frame, width=30)
entry_payment_status.grid(row=2, column=1, pady=2)

tk.Button(billing_frame, text="Generate Bill", command=generate_bill).grid(row=3, column=1, pady=10)

# Run the main loop
root.mainloop()

# Close the MySQL connection when the GUI window is closed
cursor.close()
conn.close()
