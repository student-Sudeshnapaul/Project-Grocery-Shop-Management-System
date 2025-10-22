import streamlit as st
from fpdf import FPDF
import base64

# Define a function to generate the PDF
def generate_pdf():
    pdf = FPDF()
    pdf.add_page()
    
    # Set margins (doing this first is often better)
    pdf.set_margins(left=10, top=10, right=10)
    
    # Set font
    pdf.set_font("Helvetica", size=12)

    # Add text
    pdf.cell(200, 10, txt="Hello, World!", ln=True, align="C")
    
    # Add a link
    pdf.cell(200, 10, txt="Visit our website", ln=True, align="C", link="https://google.com")
    
    # Note: The original image line is commented out.
    # For pdf.image() to work, you need a file named 'bg.png' in the same folder.
    # If you have an image, you can uncomment the line below.
    # pdf.image("bg.png", x=50, y=60, w=100)
    
    # Return the PDF as bytes
    return pdf.output(dest='S').encode('latin-1')


# --- Streamlit App ---

st.title("📄 PDF Generator using Streamlit")
st.write("Click the button below to generate and download your PDF.")

# Generate the PDF content
pdf_bytes = generate_pdf()

# Create a download button
st.download_button(
    label="Download PDF",
    data=pdf_bytes,
    file_name="basic_pdf.pdf",
    mime="application/pdf"
)

st.success("Your PDF is ready to be downloaded! 🎉")