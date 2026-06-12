# Project Overview

The Sierra Leone Community Health Management System is a desktop application developed using Python, Tkinter, and SQLite3 to digitize patient record management in local clinics.

The system replaces paper-based record keeping with a secure electronic database that enables faster patient registration, retrieval, billing, and medical follow-up tracking.

# Project Objectives

- Improve patient record management.
- Reduce loss of medical records.
- Improve retrieval speed of patient information.
- Automate follow-up scheduling.
- Generate financial reports for clinic management.
- Support healthcare delivery in rural and urban clinics.

# Technologies Used

| Technology | Purpose |
|------------|----------|
| Python | Application Development |
| Tkinter | Graphical User Interface |
| SQLite3 | Database Management |
| shutil | Database Backup System |
| datetime | Appointment Scheduling |
| ttk.Treeview | Data Visualization 

# Database Tables

## Patients
- Patient ID
- Full Name
- Age
- Gender
- Address
- Phone Number

## Visits
- Visit ID
- Patient ID
- Diagnosis
- Treatment
- Review Date

## Billing
- Invoice Number
- Consultation Fee
- Medicine Cost
- Total Cost

  # Key Features

✅ Patient Registration

✅ Patient Search and Retrieval

✅ Record Editing and Updating

✅ Automated Follow-Up Scheduling

✅ Billing and Invoice Generation

✅ Real-Time Dashboard Analytics

✅ Automatic Database Backup

✅ Disease Tracking (Malaria & Typhoid)

# Future Improvements

- Multi-user authentication system.
- Cloud database integration.
- SMS appointment reminders.
- PDF report generation.
- Mobile application support.
- Integration with national health records.

  # Community Impact

The system contributes to improved healthcare delivery by:

- Reducing patient waiting time.
- Improving medical record accuracy.
- Supporting disease surveillance.
- Enhancing clinic revenue tracking.
- Improving continuity of patient care.

# Sierra Leone Community Health Management System

An advanced, modular Graphical User Interface (GUI) digital clinic desktop platform engineered in Python and SQLite3. This system is designed specifically to solve the data retrieval bottlenecks, physical record degradation, and operational issues typical of paper-ledger medical tracking within regional public health clinics in Sierra Leone.

## 🌍 Sustainable Development Goal (SDG) 3 Alignment
This digital solution natively addresses **UN Sustainable Development Goal 3: Good Health and Well-being**:
* **Epidemiological Automation (Target 3.3):** Embeds tracking logic for endemic conditions (Malaria and Typhoid), dynamically computing strict 3-day and 7-day review intervals depending on diagnoses.
* **Financial Sustainability (Target 3c):** Prevents healthcare revenue leaks via structured consultation, medicine, and treatment billing invoice configurations.

## 🚀 System Architecture & Features
* **main.py:** The master orchestrator deploying a live, real-time administrative analytical dashboard displaying total metric aggregates (`COUNT`, `SUM`).
* **manage_records.py:** Advanced multi-record interface containing text matching queries (`LIKE %query%`) for responsive searches and interactive row hooks (`<<TreeviewSelect>>`) for inline detail alterations.
* **upgrade_database.py:** Schema updater containing a custom automated data redundancy mechanism (`shutil`) providing timestamped snapshots of `clinic.db` on startup.

## 🛠️ Installation & Execution Guidelines

1. **Clone the Repository:**
   ```bash
   git clone <your-github-repository-url>
   cd <repository-folder-name>
