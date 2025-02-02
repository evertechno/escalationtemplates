import streamlit as st
import google.generativeai as genai
from fpdf import FPDF
import zipfile
import io

# Configure the API key securely from Streamlit's secrets
# Make sure to add GOOGLE_API_KEY in secrets.toml (for local) or Streamlit Cloud Secrets
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

# Streamlit App UI
st.title("Email Escalation Response Generator")
st.write("Use Generative AI to create email escalation response templates based on different scenarios.")

# Define the model outside of the button logic to make it accessible throughout the app
model = genai.GenerativeModel('gemini-1.5-flash')

# Dropdown for selecting a single scenario
scenarios = [
    "Customer service issue",
    "Technical support escalation",
    "Delayed delivery apology",
    "Billing or payment issue",
    "General escalation",
    "Complaint about product quality",
    "Refund request escalation",
    "Shipping delay inquiry",
    "Software bug escalation",
    "Employee misconduct report",
    "Unresolved account issue",
    "Late payment reminder",
    "Urgent support request",
    "Dispute over charges",
    "Complaint about customer service",
    "Request for urgent assistance",
    "Request for account review",
    "Urgent delivery issue",
    "Product malfunction report",
    "Service disruption notification",
    "Data breach notification",
    "High-priority issue with contract terms",
    "Escalation of unresolved technical issue",
    "Request for account closure",
    "Escalation due to lack of response",
    "Rude customer interaction complaint",
    "Customer dissatisfaction with product",
    "Warranty claim escalation",
    "Feedback escalation regarding service",
    "Request for better support resolution"
]

selected_scenario = st.selectbox("Select an escalation scenario", scenarios)

# Button to generate a single PDF template
if st.button("Generate Single Template PDF"):
    try:
        # Define a basic prompt structure to guide the AI generation based on the selected scenario
        prompt = f"Generate a professional email escalation response for the following scenario: {selected_scenario}."
        
        # Generate response from the model
        response = model.generate_content(prompt)
        
        # Display response in Streamlit
        st.write("Generated Response:")
        email_content = response.text
        st.write(email_content)
        
        # Generate PDF of the email content
        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()
        
        # Set font for PDF
        pdf.set_font("Arial", size=12)
        
        # Add title to PDF
        pdf.cell(200, 10, txt=f"Email Escalation Template: {selected_scenario}", ln=True, align="C")
        pdf.ln(10)
        
        # Add the generated content to the PDF
        pdf.multi_cell(0, 10, txt=email_content)
        
        # Save PDF to a byte stream
        pdf_output = pdf.output(dest="S").encode("latin1")
        
        # Add a download button for the generated PDF
        st.download_button(
            label="Download Single Template as PDF",
            data=pdf_output,
            file_name=f"email_escalation_{selected_scenario.replace(' ', '_').replace(',', '').lower()}.pdf",
            mime="application/pdf"
        )
    
    except Exception as e:
        st.error(f"Error: {e}")


# Button to generate and download all 30 PDF templates at once
if st.button("Download All 30 Templates as ZIP"):
    try:
        # Create a byte stream to store the zip file in memory
        zip_buffer = io.BytesIO()
        
        # Create a ZIP file in memory
        with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
            for scenario in scenarios:
                # Generate the content for each scenario
                prompt = f"Generate a professional email escalation response for the following scenario: {scenario}."
                
                # Generate response from the model
                response = model.generate_content(prompt)
                email_content = response.text
                
                # Create PDF for this scenario
                pdf = FPDF()
                pdf.set_auto_page_break(auto=True, margin=15)
                pdf.add_page()
                pdf.set_font("Arial", size=12)
                pdf.cell(200, 10, txt=f"Email Escalation Template: {scenario}", ln=True, align="C")
                pdf.ln(10)
                pdf.multi_cell(0, 10, txt=email_content)
                
                # Save PDF to a byte stream
                pdf_output = pdf.output(dest="S").encode("latin1")
                
                # Add the PDF to the ZIP file
                zip_file.writestr(f"email_escalation_{scenario.replace(' ', '_').replace(',', '').lower()}.pdf", pdf_output)
        
        # Move the pointer to the start of the stream for downloading
        zip_buffer.seek(0)
        
        # Add a download button for the ZIP file
        st.download_button(
            label="Download All Templates as ZIP",
            data=zip_buffer,
            file_name="email_escalation_templates.zip",
            mime="application/zip"
        )
    
    except Exception as e:
        st.error(f"Error: {e}")
