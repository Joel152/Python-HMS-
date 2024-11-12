def main(tab):
    import mysql.connector
    import tkinter as tk
    from tkinter import messagebox

    # Establish MySQL connection
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="1234",
        database="hms"
    )
    cursor = conn.cursor()

    # Functions
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

    # Treatment Section with Text widget and Scrollbar
    treatment_frame = tk.LabelFrame(tab, text="Treatment Information", padx=10, pady=10)
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


    # Doctors Section with Text widget and Scrollbar
    doctor_frame = tk.LabelFrame(tab, text="Doctors", padx=10, pady=10)
    doctor_frame.grid(row=0, column=1, padx=10, pady=10, sticky="n")

    doctor_text = tk.Text(doctor_frame, height=8, width=40, wrap="word")
    doctor_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    doctor_scroll = tk.Scrollbar(doctor_frame, command=doctor_text.yview)
    doctor_scroll.pack(side=tk.RIGHT, fill=tk.Y)
    doctor_text.config(yscrollcommand=doctor_scroll.set)

    tk.Button(doctor_frame, text="Show Doctors", command=show_doctors).pack(pady=5)

    # Close the MySQL connection when the tab is closed
    cursor.close()
    conn.close()
