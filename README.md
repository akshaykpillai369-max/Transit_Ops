# TransitOps – Fleet Management System

TransitOps is a simple fleet management system made using Streamlit and SQLite. It helps to manage vehicles, drivers, shipments, fuel expenses and vehicle maintenance in one place.
<img width="1527" height="655" alt="image" src="https://github.com/user-attachments/assets/0c970f15-3cdc-4587-87df-2af38e53376d" />


**Live Demo:** https://transitops.streamlit.app/

## Features

- **User Roles:** Three roles are available: Admin, Fleet Manager and Financial Analyst. Each role has different access.
- **Cargo Validation:** Prevents dispatching vehicles when the cargo weight exceeds the vehicle capacity.
- **Driver License Check:** Shows expired licenses and prevents those drivers from being selected for new dispatches.
- **Vehicle Maintenance:** Tracks vehicle status, repairs and maintenance costs.
- **Fuel Tracking:** Stores fuel usage and expenses.
- **Reports:** Shows fuel efficiency, estimated vehicle ROI and allows reports to be downloaded as CSV files.

## Login Credentials

| Role | Username | Password |
|---|---|---|
| Super Admin | `admin` | `superops123` |
| Fleet Manager | `manager` | `ops123` |
| Financial Analyst | `analyst` | `cash123` |

## Project Structure

- `app.py` – Handles login, navigation and dashboard.
- `database.py` – Manages the SQLite database and stored data.
- `menu.py` – Contains the interface, forms and tables.

## How to Run

- cd transitops-platform
- streamlit run app.py

That's it, now you deployed it locally

# License
This project is licensed under the [Akshay] License - see the LICENSE.md file for details
