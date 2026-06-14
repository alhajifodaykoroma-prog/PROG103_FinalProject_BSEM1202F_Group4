<h1 align="center">🏥 Sierra Leone Community Health Management System</h1>

<p align="center">
  <em>A desktop clinic management system for community health facilities — built to bring fast, reliable patient, consultation, and billing record-keeping to clinics in Sierra Leone.</em>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/GUI-Tkinter-0E7C7B" alt="Tkinter">
  <img src="https://img.shields.io/badge/Database-SQLite-003B57?logo=sqlite&logoColor=white" alt="SQLite">
  <img src="https://img.shields.io/badge/Dependencies-Zero%20(stdlib)-1E9E62" alt="No dependencies">
  <img src="https://img.shields.io/badge/SDG-3%20Good%20Health-DC2626" alt="SDG 3">
  <img src="https://img.shields.io/badge/License-MIT-blue" alt="License">
</p>

---

## 📖 Overview

The **Sierra Leone Community Health Management System** is an offline-first desktop
application that digitises the day-to-day operations of a community clinic:
registering patients, managing doctors, logging consultations, generating bills, and
producing live analytical reports.

It is aligned with **UN Sustainable Development Goal 3 — Good Health and Well-Being**,
and is designed to run on modest hardware with **no internet connection and no external
dependencies**, making it practical for low-resource clinical settings.

---

## 🖼️ Screenshots

### Secure Login
![Login screen](screenshots/login.png)

### Main Dashboard — Live Facility Analytics
![Dashboard](screenshots/dashboard.png)

### Clinical Analytics & Reports
![Reports](screenshots/reports.png)


---

## ✨ Features

- **🔐 Secure Login** — role-based access control with an administrator account.
- **👤 Patient Registration** — capture demographics, contact details, symptoms, and an auto-generated patient code (`PAT001`, `PAT002`, …).
- **🩺 Doctor Management** — register doctors with specialization, availability, and employment status; auto-generated doctor codes (`DOC001`, …).
- **📝 Consultation Desk** — link a patient to a doctor, record diagnosis and prescription, and auto-calculate a recommended revisit date based on the condition.
- **💳 Billing Operations** — itemised billing (consultation, medicine, treatment fees) with automatic total calculation, recorded in Sierra Leonean Leones (Le).
- **📂 Record Management** — search, edit, and update patient and doctor records, including status changes (Active, Discharged, Retired, Suspended, etc.).
- **📊 Reports & Analytics** — live facility metrics and a "Top Epidemiological Case Distributions" table that ranks the most frequent diagnoses.
- **⚡ Live Dashboard** — key statistics (patients, doctors, consultations, revenue) refresh instantly as records are saved.

---

## 🛠️ Tech Stack

| Layer        | Technology                                  |
|--------------|---------------------------------------------|
| Language     | Python 3.10+                                |
| GUI          | Tkinter / ttk (Python standard library)     |
| Database     | SQLite 3 (Python standard library)          |
| Typography   | [Lato](https://fonts.google.com/specimen/Lato) (recommended) |
| Dependencies | **None** — runs entirely on the standard library |

---

## 📁 Project Structure

```
ROBERTS/
├── login.py              # Entry point — secure login screen
├── main.py               # Main dashboard + consultation & billing desks
├── patients.py           # Patient registration window
├── doctors.py            # Doctor management window
├── consultations.py      # Standalone consultation module
├── billing.py            # Standalone billing module
├── manage_records.py     # Search / edit / update patient & doctor records
├── reports.py            # Analytics dashboard & epidemiology report
├── database.py           # Creates the SQLite schema + admin user
├── upgrade_database.py   # Legacy migration helper (status columns + backup)
├── seed_mock_data.py     # Loads realistic demo data for testing/demos
├── utils.py              # Patient/doctor code generators
├── screenshots/          # README images
├── README.md
├── LICENSE
└── .gitignore
```


---

## 🗄️ Database Schema

The application uses a single SQLite database file (`clinic.db`) with five tables:

| Table           | Key Columns                                                                 |
|-----------------|-----------------------------------------------------------------------------|
| `patients`      | patient_id, patient_code, full_name, age, gender, address, symptoms, registration_date, status, phone |
| `doctors`       | doctor_id, doctor_code, doctor_name, specialization, phone, availability, employment_status |
| `consultations` | consultation_id, patient_id → patients, doctor_id → doctors, symptoms, diagnosis, prescription, revisit_date |
| `billing`       | bill_id, patient_id → patients, consultation_fee, medicine_fee, treatment_fee, total_bill |
| `users`         | user_id, username, password, role                                           |

> Foreign keys link consultations and billing back to patients and doctors, keeping clinical records consistent.

---

## 🚀 Getting Started

### Prerequisites

- **Python 3.10 or newer**
- **Tkinter** — bundled with Python on Windows and macOS. On Debian/Ubuntu/Kali, install it with:
  ```bash
  sudo apt install python3-tk
  ```
- *(Optional, for best appearance)* the **Lato** font:
  ```bash
  sudo apt install fonts-lato
  ```

No `pip install` is required — the project uses only the Python standard library.

### Installation

```bash
# 1. Clone the repository
git clone <your-repo-url>
cd ROBERTS

# 2. Create the database, schema, and administrator account
python3 database.py

# 3. (Optional) Load realistic demo data for testing or demonstrations
python3 seed_mock_data.py

# 4. Launch the application
python3 login.py
```

### Default Login

| Username           | Password         | Role          |
|--------------------|------------------|---------------|
| `robertissackamara` | `Do3tors@veslives` | Administrator |

> ⚠️ **Security note:** credentials are stored for demonstration purposes. For any real deployment, change the default login and hash stored passwords.


---

## 📋 Usage Guide

1. **Log in** with the administrator account on the launch screen.
2. From the **dashboard**, use the *System Operations Menu* to open any module:
   - **Patient Registration** → add a new patient (name and phone are required).
   - **Doctor Management** → register a doctor and their specialization.
   - **Consultation Desk** → select a patient and doctor, record the diagnosis; a revisit date is suggested automatically.
   - **Billing Operations** → select a patient and enter fees; the total is calculated and saved.
   - **Record Management** → search and update existing patients or doctors, or change their status.
   - **Reports & Analytics** → view live counts, total revenue, and the most common diagnoses.
3. The **Live Facility Analytical Overview** cards refresh automatically whenever a record is saved, or on demand via **🔄 Recalculate Statistics**.

---

## 🧪 Demo Data

Running `python3 seed_mock_data.py` populates the system with a realistic sample
clinic dataset (Freetown-based patients, doctors across multiple specializations,
consultations, and bills) so every screen displays meaningful figures during a
demonstration. The script is **idempotent** — it safely clears and re-seeds the demo
tables on each run while preserving the login account.

---

## 🗺️ Roadmap

- [ ] Hash stored passwords (e.g. `bcrypt`) instead of plain text
- [ ] Multi-user roles (receptionist, nurse, doctor) with scoped permissions
- [ ] Export reports to PDF / CSV
- [ ] Appointment scheduling and revisit reminders
- [ ] Automated database backups

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome. Feel free to fork the
repository, create a feature branch, and open a pull request.

---

## 📄 License

This project is licensed under the terms described in the [LICENSE](LICENSE) file.

---

<p align="center">
  <sub>Built with ❤️ for community health in Sierra Leone · Aligned with SDG 3: Good Health & Well-Being</sub>
</p>
