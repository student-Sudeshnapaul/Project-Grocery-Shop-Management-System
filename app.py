import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import mysql.connector
import base64
import os
from fpdf import FPDF
from datetime import datetime


st.set_page_config(page_title="Grocery Management System", layout="wide")


def image_to_base64(image_path):
 
    if os.path.exists(image_path):
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    return ""


def get_db_connection():

    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="GROCERY_SHOP"
        )
        return conn
    except mysql.connector.Error as err:
        st.error(f"Error connecting to database: {err}")
        return None
def create_bill_pdf(customer_details, cart_items, totals):

    pdf = FPDF()
    pdf.add_page()
    
    # Header
    pdf.set_font('Helvetica', 'B', 20)
    pdf.cell(0, 10, 'INVOICE', 0, 1, 'C')
    pdf.ln(10)
    
    # Company Info
    pdf.set_font('Helvetica', 'B', 12)
    pdf.cell(0, 6, 'Your Grocery Shop', 0, 1, 'L')
    pdf.set_font('Helvetica', '', 12)
    pdf.cell(0, 6, 'College St Market, Kolkata', 0, 1, 'L')
    pdf.ln(5)
    bill_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    pdf.set_font('Helvetica', 'B', 12)
    pdf.cell(0, 6, f"Bill To: {customer_details['name']}", 0, 1, 'L')
    pdf.set_font('Helvetica', '', 12)
    pdf.cell(0, 6, f"Address: {customer_details['address']}", 0, 1, 'L')
    pdf.cell(0, 6, f"Email: {customer_details['email']}", 0, 1, 'L')
    pdf.cell(0, 6, f"Date: {bill_date}", 0, 1, 'L')
    pdf.ln(15)


    pdf.set_font('Helvetica', 'B', 12)
    pdf.set_fill_color(224, 235, 255) # Light blue
    pdf.cell(95, 10, 'Item Description', 1, 0, 'C', 1)
    pdf.cell(30, 10, 'Quantity', 1, 0, 'C', 1)
    pdf.cell(30, 10, 'Unit Price', 1, 0, 'C', 1)
    pdf.cell(35, 10, 'Total', 1, 1, 'C', 1)

    
    pdf.set_font('Helvetica', '', 12)
    for item in cart_items.values():
        total_price = item['qty'] * item['price']
        pdf.cell(95, 10, item['name'], 1, 0, 'L')
        pdf.cell(30, 10, str(item['qty']), 1, 0, 'C')
        pdf.cell(30, 10, f"${item['price']:.2f}", 1, 0, 'R')
        pdf.cell(35, 10, f"${total_price:.2f}", 1, 1, 'R')

    
    pdf.set_font('Helvetica', 'B', 12)
    pdf.cell(155, 10, 'Subtotal', 1, 0, 'R')
    pdf.cell(35, 10, f"${totals['subtotal']:.2f}", 1, 1, 'R')
    pdf.cell(155, 10, 'GST (15%)', 1, 0, 'R')
    pdf.cell(35, 10, f"${totals['gst']:.2f}", 1, 1, 'R')
    pdf.cell(155, 10, 'Grand Total', 1, 0, 'R')
    pdf.cell(35, 10, f"${totals['final']:.2f}", 1, 1, 'R')

    
    pdf.ln(10)
    pdf.set_font('Helvetica', 'I', 10)
    pdf.cell(0, 10, 'Thank you for your purchase!', 0, 1, 'C')

    
    return pdf.output(dest='S').encode('latin-1')


def clear_modes():

    st.session_state.add_mode = False
    st.session_state.delete_mode = False
    st.session_state.update_mode = False

st.markdown(
    """
    <style>
    h1 {
    text-align: center !important;
}

    .stApp {
        background-color: #000000;
        color: white !important;
    }
    section.main > div.block-container {
        background-color: rgba(0,0,0,0.5);   
    }
    label {
        color: #ffffff;
        font-weight: 500;
    }

   div.stButton > button {
   
    background: linear-gradient(to bottom, #87a0ce, #4e85c5);
    
   
    background-image: 
        linear-gradient(to bottom, rgba(255,255,255,0.6) 0%, rgba(255,255,255,0.1) 50%, rgba(255,255,255,0) 100%), 
        linear-gradient(to bottom, #87a0ce, #4e85c5);

    color: white !important;
    border: 1px solid #3c6695 !important; 
    border-radius: 50px !important; 
    font-size: 20px !important;
    font-weight: bold !important;
    padding: 0.6em 1.5em !important;
    text-shadow: 0 1px 1px rgba(0, 0, 0, 0.3) !important; 
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.3) !important; 
    transition: all 0.2s ease-in-out !important;
}

div.stButton > button:hover {
   
    background-image: 
        linear-gradient(to bottom, rgba(255,255,255,0.7) 0%, rgba(255,255,255,0.2) 50%, rgba(255,255,255,0) 100%), 
        linear-gradient(to bottom, #99b3e3, #6398d4);
        
    transform: translateY(-2px); 
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.4) !important; 
    cursor: pointer !important;
}

  
    div.stFormSubmitButton > button {
        background-color: green !important;
        color: white !important;
        border: 2px solid green !important;
        border-radius: 8px !important;
        font-weight: bold !important;
        padding: 0.5em 1em !important;
    }
    div.stFormSubmitButton > button:hover {
        background-color: rgba(0, 100, 0, 0.8) !important;
        color: white !important;
        border: 2px solid white !important;    
        cursor: pointer !important;
    }
    
    
    .square-image {
        width: 100% !important; 
        height: auto !important;
        aspect-ratio: 1 / 1 !important;
        object-fit: cover !important;
        border-radius: 15px !important;
        display: block !important;
        margin: auto !important; 
    }
    </style>
    """,
    unsafe_allow_html=True
)



st.title("Your Grocery Shop Management System")
st.markdown("<h3 style='color:white;'>Please select your role to proceed-</h3>", unsafe_allow_html=True)

modes = ["Select...", "Owner", "Customer"]
mode = st.selectbox("Choose your role", modes)

if mode == "Owner":
    st.write("\n")
    st.markdown("<h3 style='color:white;'>Welcome Owner! Please select an action to manage your shop:</h3>", unsafe_allow_html=True)
    st.write("\n")
    
    
    col1, col2, col3 = st.columns(3, gap="large")

    with col1:
        img_base64 = image_to_base64("show.png")
        if img_base64: st.markdown(f'<img src="data:image/png;base64,{img_base64}" class="square-image">', unsafe_allow_html=True)
        st.write("\n")

        st.write("\n")

        show_table = st.button("Show the items in My shop", use_container_width=True)

        st.markdown("---") 

        img_base64 = image_to_base64("add.png")
        if img_base64: st.markdown(f'<img src="data:image/png;base64,{img_base64}" class="square-image">', unsafe_allow_html=True)
        st.write("\n")

        st.write("\n")

        add_items = st.button("Add New Item", use_container_width=True)

    with col2:
        img_base64 = image_to_base64("update.jpg")
        if img_base64: st.markdown(f'<img src="data:image/jpeg;base64,{img_base64}" class="square-image">', unsafe_allow_html=True)
        st.write("\n")

        st.write("\n")

        update_table = st.button("Update Item", use_container_width=True)
        
        st.markdown("---") 

        img_base64 = image_to_base64("delete.png")
        if img_base64: st.markdown(f'<img src="data:image/png;base64,{img_base64}" class="square-image">', unsafe_allow_html=True)
        st.write("\n")

        st.write("\n")

        delete_items = st.button("Delete Item", use_container_width=True)

    with col3:
        img_base64 = image_to_base64("customer.png")
        if img_base64: st.markdown(f'<img src="data:image/png;base64,{img_base64}" class="square-image">', unsafe_allow_html=True)
        st.write("\n")

        st.write("\n")

        customer_data = st.button("Customer Table", use_container_width=True)

        st.markdown("---")

        img_base64 = image_to_base64("top.png")
        if img_base64: st.markdown(f'<img src="data:image/png;base64,{img_base64}" class="square-image">', unsafe_allow_html=True)
        st.write("\n")
        st.write("\n")
        top_items = st.button("Check your top-most selling items", use_container_width=True)

    
    if "update_mode" not in st.session_state: st.session_state.update_mode = False
    if "add_mode" not in st.session_state: st.session_state.add_mode = False
    if "delete_mode" not in st.session_state: st.session_state.delete_mode = False


    if add_items:
        st.session_state.add_mode = True
        st.session_state.delete_mode = False
        st.session_state.update_mode = False
        st.rerun()
    if delete_items:
        st.session_state.add_mode = False
        st.session_state.delete_mode = True
        st.session_state.update_mode = False
        st.rerun()
    if update_table:
        st.session_state.add_mode = False
        st.session_state.delete_mode = False
        st.session_state.update_mode = True
        st.rerun()
    
   

    if show_table:
        clear_modes()
        st.markdown("<h5 style='color:white;'>Showing Items of your shop...</h5>", unsafe_allow_html=True)
        conn = get_db_connection()
        if conn:
            df = pd.read_sql("SELECT * FROM ITEMS;", conn)
            conn.close()
            st.dataframe(df, use_container_width=True)
    
    if customer_data:
        clear_modes()
        st.markdown("<h5 style='color:white;'>Customer Data Table-</h5>", unsafe_allow_html=True)
        conn = get_db_connection()
        if conn:
            df = pd.read_sql("SELECT * FROM CUSTOMER;", conn)
            conn.close()
            st.dataframe(df, use_container_width=True)

    if top_items:
        clear_modes()
        st.markdown("<h5 style='color:white;'>Top 5 Selling Items...</h5>", unsafe_allow_html=True)
        q = """
            SELECT ITEMS.NAME_OF_ITEMS AS ITEM_NAME, SUM(SELL.NO_OF_UNIT_SOLD) AS TOTAL_SOLD
            FROM SELL JOIN ITEMS ON SELL.ITEM_ID = ITEMS.ID
            GROUP BY ITEMS.NAME_OF_ITEMS
            ORDER BY TOTAL_SOLD DESC LIMIT 5;
        """
        conn = get_db_connection()
        if conn:
            df_top = pd.read_sql(q, conn)
            conn.close()
            
            plt.style.use('dark_background')
            fig, ax = plt.subplots()
            ax.bar(df_top['ITEM_NAME'], df_top['TOTAL_SOLD'], color='#ff2a2a')
            ax.set_title("Top 5 Best-Selling Items", color='white')
            ax.set_xlabel("Item Name", color='white')
            ax.set_ylabel("Total Units Sold", color='white')
            ax.tick_params(axis='x', colors='white', rotation=45)
            ax.tick_params(axis='y', colors='white')
            st.pyplot(fig)



    if st.session_state.add_mode:
        st.markdown("<h5 style='color:white;'>Add New Item to your shop...</h5>", unsafe_allow_html=True)
        with st.form("add_item_form"):
            name = st.text_input("Enter Item Name")
            category = st.text_input("Enter the category")
            qty = st.number_input("Enter the Quantity", min_value=0)
            price = st.number_input("Enter Item Price per unit", min_value=0.0, format="%.2f")
            add = st.form_submit_button("Add Item")
            if add:
                if name and category:
                    conn = get_db_connection()
                    if conn:
                        try:
                            c = conn.cursor()
                            c.execute("INSERT INTO ITEMS (NAME_OF_ITEMS, CATEGORY, QUANTITY, PER_UNIT_PRICE) VALUES (%s, %s, %s, %s);", (name, category, qty, price))
                            conn.commit()
                            st.success("Item added successfully!")
                        except Exception as e:
                            conn.rollback()
                            st.error(f"Error adding item: {e}")
                        finally:
                            conn.close()
                else:
                    st.warning("Please fill in all required fields (Name and Category)")
        if st.button("Exit Add Mode"):
            clear_modes()
            st.rerun()

    if st.session_state.delete_mode:
        st.markdown("<h5 style='color:white;'>Delete an Item from your shop...</h5>", unsafe_allow_html=True)
        with st.form("delete_form"):
            item_id = st.text_input("Enter the Item ID to delete:")
            delete = st.form_submit_button("Delete Item")
            if delete:
                if item_id:
                    conn = get_db_connection()
                    if conn:
                        try:
                            c = conn.cursor()
                            c.execute("DELETE FROM ITEMS WHERE ID = %s;", (item_id,))
                            conn.commit()
                            if c.rowcount > 0:
                                st.success(f"Item with ID {item_id} deleted successfully!")
                            else:
                                st.warning(f"No item found with ID {item_id}.")
                        except Exception as e:
                            conn.rollback()
                            st.error(f"Error deleting item: {e}")
                        finally:
                            conn.close()
                else:
                    st.warning("Please enter an Item ID.")
        if st.button("Exit Delete Mode"):
            clear_modes()
            st.rerun()

    if st.session_state.update_mode:
        st.markdown("<h5 style='color:white;'>Update Item Details...</h5>", unsafe_allow_html=True)
        item_id = st.text_input("Enter the Item ID to update: ")
        new_qty = st.number_input("Enter New Quantity", min_value=0)
        new_cost = st.number_input("Enter New Price per unit", min_value=0.0, format="%.2f")
        if st.button("Update Item Details"):
            if item_id:
                conn = get_db_connection()
                if conn:
                    try:
                        c = conn.cursor()
                        c.execute("UPDATE ITEMS SET QUANTITY = %s, PER_UNIT_PRICE = %s WHERE ID = %s;", (new_qty, new_cost, item_id))
                        conn.commit()
                        if c.rowcount > 0:
                            st.success(f"Item with ID {item_id} updated successfully!")
                        else:
                            st.warning(f"No item found with ID {item_id}.")
                    except Exception as e:
                        conn.rollback()
                        st.error(f"Error updating item: {e}")
                    finally:
                        conn.close()
            else:
                st.warning("Please provide an Item ID to update.")
        if st.button("Exit Update Mode"):
            clear_modes()
            st.rerun()


elif mode == "Customer":
    st.markdown("<h3 style='color:white;'>Welcome Customer! Please enter your details and select items:</h3>", unsafe_allow_html=True)
    if 'pdf_data' not in st.session_state:
        st.session_state.pdf_data = None
        st.session_state.pdf_file_name = None

    with st.form("customer_form"):
        name = st.text_input("Name")
        phone = st.text_input("Phone Number")
        email = st.text_input("Email Address")
        address = st.text_area("Address")
        
        st.markdown("<h4 style='color:white;'>Available Items</h4>", unsafe_allow_html=True)
        conn = get_db_connection()
        if conn:
            df_items = pd.read_sql("SELECT ID, NAME_OF_ITEMS, CATEGORY, QUANTITY, PER_UNIT_PRICE FROM ITEMS WHERE QUANTITY > 0", conn)
            conn.close()
            
            cart = {}
            for index, row in df_items.iterrows():
                st.markdown(f"**{row['NAME_OF_ITEMS']}** ({row['CATEGORY']}) - Price: ${row['PER_UNIT_PRICE']:.2f} - Available: {row['QUANTITY']}")
                qty = st.number_input(f"Quantity for {row['NAME_OF_ITEMS']}", min_value=0, max_value=int(row['QUANTITY']), step=1, key=f"qty_{row['ID']}")
                if qty > 0:
                    cart[row['ID']] = {'qty': qty, 'price': row['PER_UNIT_PRICE'], 'name': row['NAME_OF_ITEMS']}
            
            purchase_button = st.form_submit_button("Confirm Purchase and Generate Bill")

            if purchase_button:
                if not name:
                    st.warning("Please enter your name.")
                elif not cart:
                    st.warning("Please select at least one item.")
                else:
                    total_amount = sum(item['qty'] * item['price'] for item in cart.values())
                    gst = total_amount * 0.15
                    final_amount = total_amount + gst
                    
                    conn = get_db_connection()
                    if conn:
                        try:
                            c = conn.cursor()
                            c.execute("INSERT INTO CUSTOMER (NAME, PHONE_NUMBER, EMAIL_ADDRESS, ADDRESS, TOTAL_PURCHASE, REGISTERED_DATE) VALUES (%s, %s, %s, %s, %s, NOW())", (name, phone, email, address, final_amount))
                            
                            for item_id, item_details in cart.items():
                                c.execute("UPDATE ITEMS SET QUANTITY = QUANTITY - %s WHERE ID = %s", (item_details['qty'], item_id))
                                c.execute("INSERT INTO SELL (ITEM_ID, NO_OF_UNIT_SOLD) VALUES (%s, %s)", (item_id, item_details['qty']))
                            
                            conn.commit()
                            st.success("Purchase successful! Your bill is ready to download below.")

                            
                            customer_details = {'name': name, 'address': address, 'email': email}
                            totals = {'subtotal': total_amount, 'gst': gst, 'final': final_amount}
                            
                            pdf_bytes = create_bill_pdf(customer_details, cart, totals)
                            st.session_state.pdf_data = pdf_bytes
                            st.session_state.pdf_file_name = f"bill_{name.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.pdf"

                        except Exception as e:
                            conn.rollback()
                            st.error(f"Error processing purchase: {e}")
                        finally:
                            conn.close()
    

    if st.session_state.pdf_data:
        st.download_button(
            label="Download Bill (PDF)",
            data=st.session_state.pdf_data,
            file_name=st.session_state.pdf_file_name,
            mime="application/pdf"
        )