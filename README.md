# TransitOps Platform 🚚

TransitOps is a comprehensive, production-ready Fleet Management and Logistics Orchestration system designed for transport providers. Built using **Streamlit** and **SQLite3**, the platform integrates real-time asset tracking, automated business validation rules, operational cost analysis, and strict Role-Based Access Control (RBAC).

---

## 🌟 Key Features & Business Logic

### 🔐 1. Role-Based Access Control (RBAC)
The application enforces strict access control matrices across three distinct user roles to ensure operational security:
*   **Super Admin:** Unrestricted master access across all control configurations, logs, and ledger metrics.
*   **Fleet Manager:** Focused strictly on field operations (Vehicle Registry, Driver Management, Dispatch Logistics, Workshop Repairs).
*   **Financial Analyst:** Focused strictly on operational cost reporting (Fuel Logging, Maintenance Expenses, Fleet Analytics).

### ⚖️ 2. Automated Cargo Validation
*   **Overload Protection:** Prevents asset damage and legal liabilities. When scheduling a new shipment route, the system checks the assigned payload against the vehicle's max capacity constraint and blocks the dispatch if exceeded.

### 🛡️ 3. Regulatory Driver Compliance Check
*   **Expired License Shield:** Dynamically evaluates registration records against the current date. The system drops warning indicators on non-compliant records in the directory and automatically filters expired drivers out of the dispatch selectbox entirely.

### ⛽ 4. Fuel & Workshop Expense Ledger
*   **Dynamic Asset Status Tracking:** Moving a vehicle to maintenance shifts its status to `In Shop` and pulls it from availability pools. Releasing it marks it back to `Available🟢`.
*   **Cost Accumulation:** Tracks fuel receipts (litres, total costs) and aggregates them alongside asset maintenance history for clear expense records.

### 📊 5. Financial Reporting & ROI Analytics
*   Calculates real-time performance indicators including fuel efficiency ratio mappings ($km/L$) and mock vehicle Return on Investment percentages ($ROI\%$).
*   **CSV Data Export:** Features a single-click download mechanism to immediately export processed performance logs into an uncompressed spreadsheet format.

---

## 🔑 Access Control Credentials

To demonstrate the security walls during evaluation, utilise the following testing credentials:

| Identity Profile | Username | Password | Permitted Views |
| :--- | :--- | :--- | :--- |
| **Super Admin 👑** | `admin` | `superops123` | *All Modules Available* |
| **Fleet Manager 🏗️** | `manager` | `ops123` | Dashboard, Vehicles, Drivers, Dispatch, Maintenance |
| **Financial Analyst 📈** | `analyst` | `cash123` | Dashboard, Fuel Expenses, Reports & Analytics |

---

## 🛠️ Architecture & Project File Structure

The project utilises a modular, decoupled Object-Oriented paradigm splitting UI rendering from database management layers:

*   **`app.py`**: The main execution engine. Manages user authentication states, session memory flags, granular routing stops, and the central KPI summary dashboard.
*   **`database.py`**: The localized relational persistence engine. Handles thread-safe `sqlite3` context operations, data definitions, insertions, and real-time analytical aggregating queries.
*   **`menu.py`**: The layout view layout container. Houses structural forms, interactive components, data tables, grid alignments, and UI feedback alerts.

---

## 🚀 Installation & Local Deployment

### Prerequisites
Ensure you have Python 3.8+ installed on your computer.

### Setup Instructions

1. **Clone or navigate to the project root directory:**
   ```bash
   cd transitops-platform
