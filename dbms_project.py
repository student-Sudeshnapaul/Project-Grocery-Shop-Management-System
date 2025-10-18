import streamlit as st
import pandas as pd
import mysql.connector
import base64
st.set_page_config(page_title="Grocery Management System", layout="wide")


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
         color: white;
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

    .stTextInput input {{
        color: white !important;
        height: 3.5em !important;
        background-color: rgba(0,0,0,0.1) !important;
        border: 1px solid white !important;
        border-radius: 10px !important;
        padding: 1em 1.5em !important;
        font-size: 24px !important;  /* 20px font size */
        font-weight: bold !important;  /* Bold text */
    }}

    .stTextInput label {{
        color: white !important;
        font-size: 18px !important;
    }}
    </style>
    """,
    unsafe_allow_html=True
)


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
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM ITEMS")
    data = cursor.fetchall()
    columns = [i[0] for i in cursor.description]
    df = pd.DataFrame(data, columns=columns)
    cursor.close()

    st.markdown(
        """
        <div style="background-color: rgba(0,0,0,0.6); padding: 20px; border-radius: 10px">
        <h3 style="color:white;">Items in your shop</h3>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.dataframe(df, use_container_width=True)  

   if delete_items:
        st.markdown(
             """
            <div style="
            background-color: rgba(0,0,0,0.6); padding: 20px; border-radius: 10px">
            <h3 style="color:white;">Delete an Item from your shop</h3>  </div>   
""",
            unsafe_allow_html=True
        )

        with st.form("delete_form") :
            
             item_id= st.text_input("Enter the Item ID to delete: ")
             st.markdown(
            """
            <style>
            div[data-testid="stFormSubmitButton"] > button {
                background-color: rgba(0,0,0,0) !important;
                color: white !important;
                border: 2px solid white !important;
                border-radius: 8px !important;
                padding: 0.5em 1em !important;
                font-weight: bold !important;
            }

            div[data-testid="stFormSubmitButton"] > button:hover {
                background-color: rgba(255,255,255,0.2) !important;
                color: white !important;
                border: 2px solid white !important;
                cursor: pointer !important;
            }
            </style>
            """,
            unsafe_allow_html=True
        )
             confirm = st.form_submit_button("Delete Item")
             if confirm :
                  cursor= conn.cursor()
                  cursor.execute("DELETE FROM ITEMS WHERE ID = %s", (item_id,))
                  conn.commit()
        st.markdown('</div>', unsafe_allow_html=True)
    

           
           
          
            
