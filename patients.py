import sqlite3
from tkinter import *
from tkinter import ttk, messagebox
from utils import generate_patient_code


# ---------------- Database Engine Reader ----------------
def get_db_connection():
    conn = sqlite3.connect("clinic.db")
    conn.execute("PRAGMA foreign_keys=ON")
    return conn


# ---------------- Open Patient Window ----------------
def open_patient_window():

    root = Toplevel()
    root.title("Patient Registration Desk")
    root.geometry("600x550")
    root.config(bg="#F2F4F4")

    # Variables
    name_var = StringVar()
    age_var = StringVar()
    phone_var = StringVar()
    address_var = StringVar()
    symptoms_var = StringVar()


    # ---------------- Save Patient Action ----------------
    def save_patient():

        patient_code = generate_patient_code()

        full_name = name_var.get().strip()
        age = age_var.get().strip()
        gender = gender_combo.get().strip()
        phone = phone_var.get().strip()
        address = address_var.get().strip()
        symptoms = symptoms_var.get().strip()

        if not full_name or not phone:
            messagebox.showerror(
                "Validation Error",
                "Full Name and Phone Number are required."
            )
            return

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM patients WHERE phone=?",
            (phone,)
        )

        if cursor.fetchone():
            messagebox.showerror(
                "Duplicate Record",
                "Patient with this phone already exists."
            )
            conn.close()
            return

        try:
            cursor.execute(
                """
                INSERT INTO patients
                (
                patient_code,
                full_name,
                age,
                gender,
                phone,
                address,
                symptoms,
                registration_date,
                status
                )

                VALUES
                (?, ?, ?, ?, ?, ?, ?, date('now'),?)
                """,
                (
                    patient_code,
                    full_name,
                    age,
                    gender,
                    phone,
                    address,
                    symptoms,
                    "Active"
                )
            )

            conn.commit()

            messagebox.showinfo(
                "Success",
                f"Patient saved successfully!\nPatient ID: {patient_code}"
            )

            root.destroy()

        except sqlite3.Error as err:
            messagebox.showerror(
                "Database Error",
                str(err)
            )

        finally:
            conn.close()


    # Header
    Label(
        root,
        text="PATIENT REGISTRATION FORM",
        font=("Arial",14,"bold"),
        bg="#0B1F3A",
        fg="white",
        pady=10
    ).pack(fill=X)

    frame = Frame(
        root,
        bg="white",
        padx=20,
        pady=20
    )

    frame.pack(pady=20)


    Label(frame,text="Full Name *",bg="white").grid(row=0,column=0,pady=10,sticky=W)
    Entry(frame,textvariable=name_var,width=30).grid(row=0,column=1)

    Label(frame,text="Age",bg="white").grid(row=1,column=0,pady=10,sticky=W)
    Entry(frame,textvariable=age_var,width=30).grid(row=1,column=1)

    Label(frame,text="Gender",bg="white").grid(row=2,column=0,pady=10,sticky=W)

    gender_combo=ttk.Combobox(
        frame,
        values=["Male","Female","Other"],
        width=27,
        state="readonly"
    )

    gender_combo.set("Male")
    gender_combo.grid(row=2,column=1)

    Label(frame,text="Phone Number *",bg="white").grid(row=3,column=0,pady=10,sticky=W)
    Entry(frame,textvariable=phone_var,width=30).grid(row=3,column=1)

    Label(frame,text="Address",bg="white").grid(row=4,column=0,pady=10,sticky=W)
    Entry(frame,textvariable=address_var,width=30).grid(row=4,column=1)

    Label(frame,text="Symptoms",bg="white").grid(row=5,column=0,pady=10,sticky=W)
    Entry(frame,textvariable=symptoms_var,width=30).grid(row=5,column=1)

    Button(
        root,
        text="Save Patient Record",
        command=save_patient,
        bg="#0B1F3A",
        fg="white",
        font=("Arial",11,"bold")
    ).pack(pady=15)



# Run only for testing directly
if __name__ == "__main__":
    test_root = Tk()
    test_root.withdraw()
    open_patient_window()
    test_root.mainloop()