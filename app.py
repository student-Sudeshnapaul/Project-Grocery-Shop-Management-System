import streamlit as st
import pandas as pd
import mysql.connector
st.set_page_config(page_title="Grocery Management System",layout="wide")

st.markdown(
    """
    <style>
    /* Make main background black */
    .stApp {
        background-color: #000000 !important;
        color: white !important;
    }


    /* Transparent buttons with white border */
    div.stButton > button {
        background-color: pink !important;
        color: crimson !important;
        border: 2px solid crimson !important;
        border-radius: 8px !important;
        font-weight: bold !important;
        padding: 0.5em 1em !important;
    }

    /* Hover effect for buttons */
    div.stButton > button:hover {
        background-color: rgba(255, 255, 255, 0.2) !important;
        color: white !important;
        border: 2px solid white !important;
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
        background-color: rgba(255, 255, 255, 0.2) !important;
        color: white !important;
        border: 2px solid white !important;   

        cursor: pointer !important;
    }

  
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
             check_progress= st.button("Check your prot-loss")
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