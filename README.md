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