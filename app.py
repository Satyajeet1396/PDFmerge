import streamlit as st
from PyPDF2 import PdfReader, PdfWriter
from io import BytesIO
import qrcode
import base64

# Title and description
st.title("PDF Binder Tool")
st.write("Upload multiple PDF files, and we'll combine their first pages into one PDF for download.")

# Initialize a session state key for the uploader if it doesn't exist.
if 'uploader_key' not in st.session_state:
    st.session_state['uploader_key'] = 0

# Clear / Reboot App button: Increment the uploader key to force reinitialization.
if st.button("Clear / Reboot App"):
    st.session_state['uploader_key'] += 1
    st.success("App state cleared.")

# Use the uploader key in the file uploader widget.
st.subheader("📄 Upload PDF Files")
st.write("Upload your PDF files to create a binder with the first pages of each file.")
uploaded_files = st.file_uploader(
    "Upload PDF files", 
    type="pdf", 
    accept_multiple_files=True, 
    key=f"file_uploader_{st.session_state['uploader_key']}"
)

# Function to create a PDF binder from the first pages of uploaded files.
def create_pdf_binder(files):
    pdf_writer = PdfWriter()
    for uploaded_file in files:
        try:
            pdf_reader = PdfReader(uploaded_file)
            if len(pdf_reader.pages) > 0:
                first_page = pdf_reader.pages[0]
                pdf_writer.add_page(first_page)
        except Exception as e:
            st.warning(f"Could not process file {uploaded_file.name}: {e}")
    return pdf_writer

# Auto-create binder when files are uploaded.
if uploaded_files:
    st.subheader("🛠️ Binder Preview")
    with st.spinner("Creating binder..."):
        pdf_writer = create_pdf_binder(uploaded_files)
    if pdf_writer.pages:
        binder_output = BytesIO()
        pdf_writer.write(binder_output)
        binder_output.seek(0)
        st.download_button(
            label="Download Binder PDF",
            data=binder_output,
            file_name="binder.pdf",
            mime="application/pdf"
        )
        st.success("Binder created successfully!")
    else:
        st.warning("No pages found in the uploaded PDF files.")
else:
    st.info("Upload PDF files to automatically create a binder.")

# Info section about the creator
st.info("Created by Dr. Satyajeet Patil")
st.info("For more cool apps like this visit: https://patilsatyajeet.wixsite.com/home/python")

# Support section in an expandable container
with st.expander("🤝 Support Our Research", expanded=False):
    st.markdown(
        """
        <div style='text-align: center; padding: 1rem; background-color: #f0f2f6; border-radius: 10px; margin: 1rem 0;'>
            <h3>🙏 Your Support Makes a Difference!</h3>
            <p>Your contribution helps us continue developing free tools for the research community.</p>
            <p>Every donation, no matter how small, fuels our research journey!</p>
        </div>
        """, unsafe_allow_html=True)

    # Two columns for QR code and Buy Me a Coffee button
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### UPI Payment")
        @st.cache_data
        def generate_qr_code(data):
            qr = qrcode.make(data)
            buffer = BytesIO()
            qr.save(buffer, format="PNG")
            buffer.seek(0)
            return buffer

        upi_url = "upi://pay?pa=satyajeet1396@oksbi&pn=Satyajeet Patil&cu=INR"
        buffer = generate_qr_code(upi_url)
        qr_base64 = base64.b64encode(buffer.getvalue()).decode()

        st.markdown("Scan to pay: **satyajeet1396@oksbi**")
        st.markdown(
            f"""
            <div style="display: flex; justify-content: center; align-items: center;">
                <img src="data:image/png;base64,{qr_base64}" width="200">
            </div>
            """, unsafe_allow_html=True
        )

    with col2:
        st.markdown("#### Buy Me a Coffee")
        st.markdown("Support through Buy Me a Coffee platform:")
        st.markdown(
            """
            <div style="display: flex; justify-content: center; align-items: center; height: 100%;">
                <a href="https://www.buymeacoffee.com/researcher13" target="_blank">
                    <img src="https://img.buymeacoffee.com/button-api/?text=Support our Research&emoji=&slug=researcher13&button_colour=FFDD00&font_colour=000000&font_family=Cookie&outline_colour=000000&coffee_colour=ffffff" alt="Support our Research"/>
                </a>
            </div>
            """, unsafe_allow_html=True
        )

st.info("A small donation from you can fuel our research journey, turning ideas into breakthroughs that can change lives!")
