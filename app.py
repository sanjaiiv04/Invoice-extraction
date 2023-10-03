import streamlit as st
import pandas as pd
from io import StringIO
import pdfplumber
import base64
import re
uploaded_file = st.file_uploader("Choose a file",type='pdf')
if uploaded_file is not None:
    base64_pdf = base64.b64encode(uploaded_file.read()).decode('utf-8')
    pdf_display = f'<embed src="data:application/pdf;base64,{base64_pdf}" width="700" height="1000" type="application/pdf">' 
    st.markdown(pdf_display, unsafe_allow_html=True)
    pdf=pdfplumber.open(uploaded_file)
    lines=[]
    for line in pdf.pages[0].extract_text().splitlines():
      lines.append(line)

# Define regular expressions for extracting specific information
    name_pattern = r'BILLED TO: (.+)'
    address_pattern = r'PAY TO: (.+)'
    phone_pattern = r'(\d{3}-\d{3}-\d{4})'
    email_pattern = r'[\w\.-]+@[\w\.-]+'
    total_pattern = r'TOTAL (\$\d+\.\d{2})'
    # Initialize variables to store extracted information
    name = None
    address = None
    phone = None
    email = None
    total = None
    # Iterate through the text list and use regex to extract information
    for line in lines:
        if not name:
            match = re.search(name_pattern, line)
            if match:
                name = match.group(1)

        if not address:
            match = re.search(address_pattern, line)
            if match:
                address = match.group(1)

        if not phone:
            match = re.search(phone_pattern, line)
            if match:
                phone = match.group(1)

        if not email:
            match = re.search(email_pattern, line)
            if match:
                email = match.group()
        if not total:
            match = re.search(total_pattern,line)
            if match:
              total=match.group()


    # Print the extracted information
    data={}
    st.write("Name of the company:", name)
    st.write("Address:", address)
    st.write("Phone No:", phone)
    st.write("Email:", email)
    st.write(total)
        
