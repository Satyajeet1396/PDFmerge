import streamlit as st
from PyPDF2 import PdfReader, PdfWriter
from io import BytesIO

# Title of the app
st.title("PDF Binder Tool")
st.write("Upload multiple PDF files, and we'll combine their first pages into one PDF for download.")

# File uploader for multiple PDF files
uploaded_files = st.file_uploader("Upload PDF files", type="pdf", accept_multiple_files=True)

# Button to create binder
if st.button("Create Binder") and uploaded_files:
    # Initialize a PdfWriter object
    pdf_writer = PdfWriter()

    # Process each uploaded file
    for uploaded_file in uploaded_files:
        pdf_reader = PdfReader(uploaded_file)
        first_page = pdf_reader.pages[0]
        pdf_writer.add_page(first_page)

    # Save the result to an in-memory file
    binder_output = BytesIO()
    pdf_writer.write(binder_output)
    binder_output.seek(0)

    # Create a download button
    st.download_button(
        label="Download Binder PDF",
        data=binder_output,
        file_name="binder.pdf",
        mime="application/pdf"
    )

    st.success("Binder created successfully! Click the button to download.")
else:
    st.info("Upload PDF files and click 'Create Binder' to proceed.
    Created by Dr. Satyajeet Patil")
