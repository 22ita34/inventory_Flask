# 📦 Inventory Management System

A Flask-based web application to manage warehouse locations. Allows users to add, view, and edit warehouse data such as name, address, city, state, country, and postal code.


## 🚀 Features

- Add new warehouse locations 🏗️
- View all locations in a table 🗂️
- Edit existing location details ✏️
- Clean UI with form validation
- Connected to SQL database (PostgreSQL/MySQL)

---

## 🛠️ Tech Stack

- **Backend:** Flask (Python)
- **Frontend:** HTML5, CSS3, Jinja2
- **Database:** PostgreSQL or MySQL (via custom `db_conn()` function)
- **Tools:** Postman for testing


---

## ⚙️ Setup Instructions

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/warehouse-location-management.git
   cd warehouse-location-management
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

pip install -r requirements.txt


#requirements
Flask==2.3.3
Jinja2==3.1.3
psycopg2-binary==2.9.9  # For PostgreSQL, remove if you're using MySQL
# OR use this for MySQL:
# mysql-connector-python==8.3.0


To run this app

python app.py



