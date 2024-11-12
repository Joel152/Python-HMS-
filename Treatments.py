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
def show_treatments():
    patient_id = int(entry_patient_id.get())
    query = "SELECT treatment_id, diagnosis, medications, treatment_date FROM Treatments WHERE patient_id = %s"
    cursor.execute(query, (patient_id,))
    treatments = cursor.fetchall()

    treatment_text.delete("1.0", tk.END)
    for treatment in treatments:
        treatment_text.insert(tk.END, f"ID: {treatment[0]}, Diagnosis: {treatment[1]}, Medications: {treatment[2]}, Date: {treatment[3]}\n")
# GUI setup
root = tk.Tk()
root.title("Hospital Management System")
root.geometry("800x600")

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

# Run the main loop
root.mainloop()

# Close the MySQL connection when the GUI window is closed
cursor.close()
conn.close()
