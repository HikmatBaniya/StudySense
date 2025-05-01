import pdfplumber 
import docx 
import streamlit as st


def extract_text_from_pdf(file_path):
    text = ""
    with pdfplumber.open(file_path) as pdf: 
        for page in pdf.pages:
            text += page.extract_text()
    return text 

def extract_text_from_docx(file_path):
    doc = docx.Document(file_path)
    text = '\n'.join([para.text for para in doc.paragraphs])
    return text 

def extract_text_from_txt(file_path):
    text = ""
    with open(file_path,'r',encoding='utf-8') as file: 
        text = file.read()
    return text


# Streamlit UI 
st.title("File Extracter")
st.write("Upload a PDF, DOCX, or TXT file to extract its text content")

# File uploader 
uploaded_file = st.file_uploader("Choose a file",type = ['pdf','docx','txt'])

if uploaded_file is not None: 
    #Save and upload file temporarily 
    with open(uploaded_file.name,"wb") as f: 
        f.write(uploaded_file.getbuffer())

    # Extract text based on file type 
    try: 
        if uploaded_file.name.endswith('.pdf'):
            extracted_text = extract_text_from_pdf(uploaded_file.name)
        elif uploaded_file.name.endswith('.docx'):
            extracted_text = extract_text_from_docx(uploaded_file.name)
        elif uploaded_file.name.endswith('.txt'):
            extracted_text = extract_text_from_txt(uploaded_file.name)
        else: 
            extracted_text = "Unsupported file format"

        st.subheader("Extracted text: ")
        st.text_area("Text Output",extracted_text,height = 300)

    except Exception as e: 
        st.error(f"Error processing file: {e}")


    # Clean up temporary files 
    import os 
    os.remove(uploaded_file.name)