# 🏥 Sierra Leone Community Health Management System

![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python) ![SQLite](https://img.shields.io/badge/Database-SQLite3-lightgrey?logo=sqlite) ![Tkinter](https://img.shields.io/badge/GUI-Tkinter-green) ![License](https://img.shields.io/badge/License-MIT-yellow)

> **PROG103 Final Project — BSEM1202F Group 4**
> A desktop clinic management application built to modernize healthcare record-keeping in Sierra Leone.

---

## 📋 Table of Contents

- [Project Overview](#project-overview)
- [Project Objectives](#project-objectives)
- [Technologies Used](#technologies-used)
- [System Architecture & Features](#-system-architecture--features)
- [Database Tables](#database-tables)
- [Key Features](#key-features)
- [Installation & Execution](#️-installation--execution)
- [Future Improvements](#future-improvements)
- [Community Impact](#community-impact)
- [SDG 3 Alignment](#-sustainable-development-goal-sdg-3-alignment)

---

## 📌 Project Overview

The **Sierra Leone Community Health Management System** is a desktop application developed using **Python**, **Tkinter**, and **SQLite3** to digitize patient record management in local clinics.

The system replaces paper-based record keeping with a secure electronic database that enables faster patient registration, retrieval, billing, and medical follow-up tracking — significantly improving healthcare delivery in rural and urban clinics across Sierra Leone.

---

## 🎯 Project Objectives

- ✔️ Improve patient record management
- ✔️ Reduce loss of medical records
- ✔️ Improve retrieval speed of patient information
- ✔️ Automate follow-up scheduling
- ✔️ Generate financial reports for clinic management
- ✔️ Support healthcare delivery in rural and urban clinics

---

## 🛠️ Technologies Used

| Technology     | Purpose                    |
|----------------|----------------------------|
| Python         | Application Development    |
| Tkinter        | Graphical User Interface   |
| SQLite3        | Database Management        |
| shutil         | Database Backup System     |
| datetime       | Appointment Scheduling     |
| ttk.Treeview   | Data Visualization         |

---

## 🏗️ System Architecture & Features

| Module                  | Description |
|-------------------------|-------------|
| `main.py`               | Master orchestrator — deploys a live, real-time administrative dashboard displaying total metric aggregates (`COUNT`, `SUM`) |
| `manage_records.py`     | Advanced multi-record interface with text-matching queries (`LIKE %query%`) for responsive searches and interactive row hooks (`<<TreeviewSelect>>`) for inline record edits |
| `upgrade_database.py`   | Schema updater with an automated data redundancy mechanism (`shutil`) that creates timestamped snapshots of `clinic.db` on startup |

---

## 🗄️ Database Tables

### 👤 Patients
| Field         | Description              |
|---------------|--------------------------|
| Patient ID    | Unique identifier        |
| Full Name     | Patient's full name      |
| Age           | Patient's age            |
| Gender        | Patient's gender         |
| Address       | Residential address      |
| Phone Number  | Contact number           |

### 🏨 Visits
| Field        | Description                  |
|--------------|------------------------------|
| Visit ID     | Unique visit identifier      |
| Patient ID   | Linked patient reference     |
| Diagnosis    | Medical diagnosis            |
| Treatment    | Treatment administered       |
| Review Date  | Scheduled follow-up date     |

### 💵 Billing
| Field             | Description                 |
|-------------------|-----------------------------|
| Invoice Number    | Unique billing reference    |
| Consultation Fee  | Fee for consultation        |
| Medicine Cost     | Cost of prescribed medicine |
| Total Cost        | Total amount charged        |

---

## ✅ Key Features

| Feature                              | Status  |
|--------------------------------------|---------|
| Patient Registration                 | ✅ Done |
| Patient Search and Retrieval         | ✅ Done |
| Record Editing and Updating          | ✅ Done |
| Automated Follow-Up Scheduling       | ✅ Done |
| Billing and Invoice Generation       | ✅ Done |
| Real-Time Dashboard Analytics        | ✅ Done |
| Automatic Database Backup            | ✅ Done |
| Disease Tracking (Malaria & Typhoid) | ✅ Done |

---

## 🚀 Installation & Execution

### Prerequisites

- Python 3.x installed on your machine
- No additional pip packages required (uses Python standard library only)

### Steps

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/alhajifodaykoroma-prog/PROG103_FinalProject_BSEM1202F_Group4.git
   cd PROG103_FinalProject_BSEM1202F_Group4
   ```

2. **Run the Application:**
   ```bash
   python main.py
   ```

3. **On first run**, `upgrade_database.py` will automatically initialize and back up the database.

---

## 🔮 Future Improvements

- [ ] Multi-user authentication system
- [ ] Cloud database integration
- [ ] SMS appointment reminders
- [ ] PDF report generation
- [ ] Mobile application support
- [ ] Integration with national health records

---

## 🌍 Community Impact

The system contributes to improved healthcare delivery by:

- 🕐 Reducing patient waiting time
- 📄 Improving medical record accuracy
- 🦠 Supporting disease surveillance
- 💰 Enhancing clinic revenue tracking
- 🔄 Improving continuity of patient care

---

## 🌐 Sustainable Development Goal (SDG) 3 Alignment

This digital solution natively addresses **UN Sustainable Development Goal 3: Good Health and Well-being**:

- **Epidemiological Automation (Target 3.3):** Embeds tracking logic for endemic conditions (Malaria and Typhoid), dynamically computing strict 3-day and 7-day review intervals depending on diagnoses.
- **Financial Sustainability (Target 3c):** Prevents healthcare revenue leaks via structured consultation, medicine, and treatment billing invoice configurations.

---

## 👥 Group 4 — BSEM1202F

> PROG103 Final Project | Submitted in partial fulfillment of the course requirements.

---

*Made with ❤️ for better healthcare in Sierra Leone*
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

