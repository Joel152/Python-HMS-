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
def generate_bill():
    patient_id = int(entry_patient_id.get())
    treatment_id = int(entry_treatment_id.get())
    amount = float(entry_amount.get())
    payment_status = entry_payment_status.get()

    # Check if treatment_id exists in the treatments table
    cursor.execute("SELECT COUNT(*) FROM treatments WHERE treatment_id = %s", (treatment_id,))
    result = cursor.fetchone()
    
    if result[0] == 0:
        messagebox.showerror("Error", f"Treatment ID {treatment_id} does not exist.")
        return

    # Proceed to insert into the billing table if treatment_id is valid
    query = "INSERT INTO billing (patient_id, treatment_id, amount, payment_status) VALUES (%s, %s, %s, %s)"
    values = (patient_id, treatment_id, amount, payment_status)
    cursor.execute(query, values)
    conn.commit()
    messagebox.showinfo("Success", "Bill generated successfully.")

# GUI setup
root = tk.Tk()
root.title("Hospital Management System")
root.geometry("400x300")

# Billing Section
billing_frame = tk.LabelFrame(root, text="Billing", padx=10, pady=10)
billing_frame.grid(row=0, column=0, padx=10, pady=10, sticky="n")

tk.Label(billing_frame, text="Patient ID:").grid(row=0, column=0, sticky="w", pady=2)
entry_patient_id = tk.Entry(billing_frame, width=30)
entry_patient_id.grid(row=0, column=1, pady=2)

tk.Label(billing_frame, text="Treatment ID:").grid(row=1, column=0, sticky="w", pady=2)
entry_treatment_id = tk.Entry(billing_frame, width=30)
entry_treatment_id.grid(row=1, column=1, pady=2)

tk.Label(billing_frame, text="Amount:").grid(row=2, column=0, sticky="w", pady=2)
entry_amount = tk.Entry(billing_frame, width=30)
entry_amount.grid(row=2, column=1, pady=2)

tk.Label(billing_frame, text="Payment Status:").grid(row=3, column=0, sticky="w", pady=2)
entry_payment_status = tk.Entry(billing_frame, width=30)
entry_payment_status.grid(row=3, column=1, pady=2)

tk.Button(billing_frame, text="Generate Bill", command=generate_bill).grid(row=4, column=1, pady=10)

# Run the main loop
root.mainloop()

# Close the MySQL connection when the GUI window is closed
cursor.close()
conn.close()
