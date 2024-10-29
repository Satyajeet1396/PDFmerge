import streamlit as st
from PyPDF2 import PdfReader, PdfWriter
from io import BytesIO
import qrcode

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
        if pdf_reader.num_pages > 0:  # Check if there's at least one page
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
    st.info("Upload PDF files and click 'Create Binder' to proceed.")

st.info("Created by Dr. Satyajeet Patil")
st.info("For more cool apps like this visit: https://patilsatyajeet.wixsite.com/home/python")

# Title of the section
st.title("UPI Payment")
st.write("Scan the QR code below to make a payment to: satyajeet1396@oksbi")

# Generate the UPI QR code
upi_url = "upi://pay?pa=satyajeet1396@oksbi&pn=Satyajeet Patil&cu=INR"
qr = qrcode.make(upi_url)

# Save the QR code image to a BytesIO object
buffer = BytesIO()
qr.save(buffer, format="PNG")
buffer.seek(0)

# Display the QR code image in Streamlit
st.image(buffer, width=200)  # Adjust the width if needed


# Display the "Buy Me a Coffee" button as an image link
st.markdown(
    """
    <div style="text-align: center; margin-top: 20px;">
        <a href="https://www.buymeacoffee.com/researcher13" target="_blank">
            <img src="https://img.buymeacoffee.com/button-api/?text=Support our Research&emoji=&slug=researcher13&button_colour=FFDD00&font_colour=000000&font_family=Cookie&outline_colour=000000&coffee_colour=ffffff" alt="Support our Research"/>
        </a>
    </div>
    """,
    unsafe_allow_html=True
)
