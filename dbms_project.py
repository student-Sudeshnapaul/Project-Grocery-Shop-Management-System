import streamlit as st
import pandas as pd
import mysql.connector

st.title("Your Grocery Shop Management System")
st.write("Please select your role to proceed-")


# Connect to MySQL database

conn = mysql.connector.connect(
    host="localhost",      
    user="root",           
    password="",           
    database="GROCERY_SHOP"
)

modes=["Select...","Owner","Customer"]
mode=st.selectbox("Choose your role",modes)
if mode=="Owner":
   st.write("Welcome Owner! Please select an action to manage your shop:")
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
           cursor=conn.cursor()
           cursor.execute("SELECT * FROM ITEMS")
           data=cursor.fetchall()
           c= [i[0] for i in cursor.description]
           df= pd.DataFrame(data, columns=c)
           st.write("Items in your shop:")   
           st.table(df)
           cursor.close()  
