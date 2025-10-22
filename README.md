````markdown
# 🛒 Grocery Shop Management System (Streamlit + MySQL)

<p align="center">
<img src="DBMS.gif" alt="Project Demo" width="700"/>
</p>

A comprehensive **Grocery Management System** built with **Streamlit** and **MySQL**, offering dual interfaces for owners and customers.

## 👥 User Roles

* **🧑‍💼 Owners:** Manage inventory, track sales, and view customer data.
* **🛍️ Customers:** Purchase items and generate downloadable PDF invoices.

## ✨ Features

### 👨‍💼 Owner Dashboard

* **📋 View Inventory:** Display all items in a clean, organized table.
* **➕ Add New Items:** Add new products to the database (Name, Category, Quantity, Price).
* **✏️ Update Items:** Modify quantity or price of existing products using item ID.
* **❌ Delete Items:** Remove products from the inventory.
* **👥 View Customer Data:** See customer details and purchase history.
* **📊 Sales Analytics:** Visualize top 5 best-selling products using bar charts.

### 🧑‍🛒 Customer Portal

* **🛒 Browse Products:** View available items with real-time price and stock details.
* **➕ Add to Cart:** Select multiple products and desired quantities.
* **🧾 Checkout Form:** Fill in personal details (Name, Phone, Email, Address) to confirm purchase.
* **🔄 Live Inventory Update:** Automatically updates stock after purchase confirmation.
* **📑 PDF Invoice Generation:** Generates detailed purchase invoices (via FPDF).
* **💾 Download Bill:** Instantly download the generated invoice as a PDF.

## 🧰 Technologies Used

| Technology | Purpose |
| :--- | :--- |
| **Python** | Core programming language |
| **Streamlit** | Interactive web UI framework |
| **MySQL** | Backend database (`mysql-connector-python`) |
| **Pandas** | Data manipulation and display |
| **Matplotlib** | Sales chart and data visualization |
| **FPDF (`pyfpdf`)** | PDF invoice generation |

## 🚀 Setup & Installation

### 1️⃣ Clone the Repository

```bash
git clone [https://github.com/your-username/your-repository-name.git](https://github.com/your-username/your-repository-name.git)
cd your-repository-name
````

### 2️⃣ Install Dependencies

**(Make sure you have a `requirements.txt` file)**

```bash
pip install -r requirements.txt
```

*If you don't have one, create `requirements.txt` and add:*

```text
streamlit
pandas
matplotlib
mysql-connector-python
fpdf
```

### 3️⃣ Set Up Database

1.  **Install MySQL** (e.g., via XAMPP, WAMP, or MySQL Community Server).
2.  **Start** your MySQL service.
3.  **Run the SQL queries** from the `.sql` file (or from the previous `README` version) to create the `GROCERY_SHOP` database and all the required tables (`ITEMS`, `CUSTOMER`, `SELL`).
4.  **Update your database credentials** (host, user, password) in the `get_db_connection()` function in your Python script.

### 4️⃣ Run the Streamlit App

```bash
streamlit run your_app_name.py
```

*(Replace `your_app_name.py` with the name of your script)*

## 📜 License

This project is open-source and available under the [MIT License](https://opensource.org/licenses/MIT).

```
```
