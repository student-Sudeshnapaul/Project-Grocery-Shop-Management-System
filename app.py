import streamlit as st
import pandas as pd
import mysql.connector
import base64
st.set_page_config(page_title="Grocery Management System",layout="wide")

def get_base64_of_image(image_file):
    with open(image_file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

image_path = "bg.png"

encoded_image = get_base64_of_image(image_path)

st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url("data:image/png;base64,{encoded_image}");
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
        color: white !important;
    }}
    section.main > div.block-container {{
        background-color: rgba(0,0,0,0.5);  /* optional overlay for readability */
    }}
    div.stButton > button {{
        background-color: rgba(0,0,0,0);  /* transparent background */
        color: white;                     /* text color */
        border: 2px solid white;          /* border color */
        border-radius: 8px;               /* rounded corners */
        padding: 0.5em 1em;
        font-weight: bold;
    }}


    div.stButton > button:hover {{
        background-color: rgba(255,255,255,0.2); /* semi-transparent hover */
        color: white;
        border: 2px solid white;
        cursor: pointer;
    }}
    div.stFormSubmitButton > button {{
        background-color: green !important;
        color: white !important;
        border: 2px solid green !important;
        border-radius: 8px !important;
        font-weight: bold !important;
        padding: 0.5em 1em !important;
    }}
    div.stFormSubmitButton > button:hover {{
        background-color: rgba(255, 255, 255, 0.2) !important;
        color: white !important;
        border: 2px solid white !important;   
        cursor: pointer !important;
    }}
    label {{
        color: #ffffff;
        font-weight: 500;
    }}
    </style>
    """,
    unsafe_allow_html=True
)


st.title("Your Grocery Shop Management System")
st.markdown("<h3 style='color:white;'>Please select your role to proceed-</h3>", unsafe_allow_html=True)


conn = mysql.connector.connect(
    host="localhost",      
    user="root",           
    password="",           
    database="GROCERY_SHOP"
)
modes=["Select...","Owner","Customer"]
mode=st.selectbox("Choose your role",modes)

if mode=="Owner":
   st.write("\n")
   st.markdown("<h3 style='color:white;'>Welcome Owner! Please select an action to manage your shop:</h3>", unsafe_allow_html=True)
   st.write("\n")
   st.write("\n")
   col1, col2= st.columns(2)
   
   with col1:
      
             show_table= st.button("Show the items in My shop")
             add_items= st.button("Add New Item")
             update_table= st.button("Update Item")
   with col2:
             delete_items= st.button("Delete Item")
             customer_data= st.button("Customer Table")
             top_items= st.button("Check your top-most selling items")
  
   if show_table:
       st.write("\n")
       st.markdown("<h5 style='color:white;'>Showing Items of your shop...</h5>", unsafe_allow_html=True)
       c= conn.cursor()
       df= pd.read_sql("SELECT * FROM ITEMS;",conn)
       st.dataframe(df)
       conn.close()
   if add_items:
           st.write("\n")
           st.markdown("<h5 style='color:white;'>Add New Item to your shop...</h5>", unsafe_allow_html=True)
    
           with st.form("add_item_form"):
                  col3, col4 = st.columns(2)
                  with col3:
                    st.markdown("<h6 style='color:white;'>Enter Item Name</h6>", unsafe_allow_html=True)
                    name = st.text_input("", key="name_input")
                    st.markdown("<h6 style='color:white;'>Enter the category</h6>", unsafe_allow_html=True)
                    category = st.text_input("", key="category_input")
        
                  with col4:
                       st.markdown("<h6 style='color:white;'>Enter the Quantity</h6>", unsafe_allow_html=True)
                       qty = st.number_input("", 0, key="qty_input")
                       st.markdown("<h6 style='color:white;'>Enter Item Price per unit</h6>", unsafe_allow_html=True)
                       price = st.number_input("", 0.0, key="price_input")
                       st.write("\n")
        
                       add = st.form_submit_button("Add Item")
        
                       if add:
                            if name and category:
                                         try:
                                               c = conn.cursor()
                                               c.execute("INSERT INTO ITEMS (NAME, CATEGORY, QUANTITY, PRICE) VALUES (%s, %s, %s, %s);", 
                             (name, category, qty, price))
                                               conn.commit()
                                               st.success("Item added successfully!")
                                               conn.close()
                                         except Exception as e:
                                                  conn.rollback()
                                                  st.error(f"Error adding item: {e}")
                       else:
                              st.warning("Please fill in all required fields (Name and Category)")
   if delete_items :
        st.write("\n")
        st.markdown("<h5 style='color:white;'>Delete an Item from your shop...</h5>", unsafe_allow_html=True)

        with st.form("delete_form") :
               col5, col6 = st.columns(2)
               with col5:
                      st.markdown("<h6 style='color:white;'>Enter the Item ID to delete:</h6>", unsafe_allow_html=True)
                      item_id= st.text_input("", key="delete_item_id")
               with col6:
                        st.write("\n")
                        st.write("\n")
                        st.write("\n")
                        st.write("\n")
                        delete = st.form_submit_button("Delete Item")
                        if delete :
                               if item_id :
                                       try :
                                             c=conn.cursor()
                                             c.execute("DELETE FROM ITEMS WHERE ID= %s;",item_id)
                                             conn.commit()
                                             st.success("Item deleted successfully!")  
                                             st.conn.close()
                                       except Exception as e :
                                                conn.rollback()
                                                st.error(f"Error deleting item: {e}")  
   if customer_data :
              st.write("\n")
              st.markdown("<h5 style== 'color:white;'>Customer Data Table-</h5>", unsafe_allow_html=True)
              c= conn.cursor()
              df= pd.read_sql("SELECT * FROM CUSTOMER;", conn)
              st.dataframe(df)
              conn.close()



if mode == "Customer":
    st.write("\n")
    st.markdown("<h3 style='color:white;'>Welcome Customer! Please enter your details and select items:</h3>", unsafe_allow_html=True)

    # Customer details
    st.markdown("<h6 style='color:white;'>Name</h6>", unsafe_allow_html=True)
    name = st.text_input("", key="customer_name")
    st.markdown("<h6 style='color:white;'>Phone Number</h6>", unsafe_allow_html=True)
    phone = st.text_input("", key="customer_phone")
    st.markdown("<h6 style='color:white;'>Email Address</h6>", unsafe_allow_html=True)
    email = st.text_input("", key="customer_email")
    st.markdown("<h6 style='color:white;'>Address</h6>", unsafe_allow_html=True)
    address = st.text_input("", key="customer_address")

    # Fetch available items
    df_items = pd.read_sql("SELECT ID, NAME_OF_ITEMS, CATEGORY, QUANTITY, PER_UNIT_PRICE FROM ITEMS", conn)
    st.markdown("<h4 style='color:white;'>Available Items</h4>", unsafe_allow_html=True)

    # Cart selection
    cart = []
    for index, row in df_items.iterrows():
        st.markdown(
            f"<span style='color:white; font-weight:500;'>{row['NAME_OF_ITEMS']} ({row['CATEGORY']}) - Price: {row['PER_UNIT_PRICE']} - Available: {row['QUANTITY']}</span>",
            unsafe_allow_html=True
        )
        qty = st.number_input("", min_value=0, max_value=int(row['QUANTITY']), step=1, key=f"qty_{row['ID']}")
        if qty > 0:
            cart.append((row['ID'], qty, row['PER_UNIT_PRICE'], row['NAME_OF_ITEMS']))

    # Confirm purchase button
    if st.button("Confirm Purchase"):
        if not name:
            st.warning("Please enter your name.")
        elif not cart:
            st.warning("Please select at least one item.")
        else:
            try:
                total_amount = 0
                bill_lines = []
                c = conn.cursor()

                # Calculate total
                for item_id, qty, price, item_name in cart:
                    line_total = qty * price
                    total_amount += line_total
                    bill_lines.append(f"{item_name} x {qty} = {line_total:.2f}")
                
                gst = total_amount * 0.15  # 15% GST
                final_amount = total_amount + gst

                # Show bill
                st.markdown("<h4 style='color:white;'>Bill Summary</h4>", unsafe_allow_html=True)
                for line in bill_lines:
                    st.write(line)
                st.write(f"Subtotal: {total_amount:.2f}")
                st.write(f"GST (15%): {gst:.2f}")
                st.write(f"Total Amount: {final_amount:.2f}")

                # Insert customer data
                c.execute("""
                    INSERT INTO CUSTOMER (NAME, PHONE_NUMBER, EMAIL_ADDRESS, ADDRESS, TOTAL_PURCHASE, REGISTERED_DATE)
                    VALUES (%s, %s, %s, %s, %s, NOW())
                """, (name, phone, email, address, final_amount))
                customer_id = c.lastrowid

                # Update ITEMS and SELL tables
                for item_id, qty, price, _ in cart:
                    c.execute("UPDATE ITEMS SET QUANTITY = QUANTITY - %s WHERE ID = %s", (qty, item_id))
                    c.execute("INSERT INTO SELL (ITEM_ID, NO_OF_UNIT_SOLD) VALUES (%s, %s)", (item_id, qty))

                conn.commit()
                st.success("Purchase successful! Your customer data and order have been recorded.")

            except Exception as e:
                conn.rollback()
                st.error(f"Error processing purchase: {e}")
