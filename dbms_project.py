import streamlit as st


st.title("Your Grocery Shop Management System")
st.write("Please select your role to proceed-")

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

             
