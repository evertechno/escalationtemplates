import streamlit as st
import google.generativeai as genai
from fpdf import FPDF

# Configure the API key securely from Streamlit's secrets
# Make sure to add GOOGLE_API_KEY in secrets.toml (for local) or Streamlit Cloud Secrets
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

# Streamlit App UI
st.title("Email Escalation Response Generator")
st.write("Use Generative AI to create email escalation response templates based on different scenarios.")

# Dropdown for selecting the scenario
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

# Button to generate the response
if st.button("Generate Template"):
    try:
        # Define a basic prompt structure to guide the AI generation based on the selected scenario
        prompt = f"Generate a professional email escalation response for the following scenario: {selected_scenario}."
        
        # Load and configure the model
        model = genai.GenerativeModel('gemini-1.5-flash')
        
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
            label="Download Template as PDF",
            data=pdf_output,
            file_name=f"email_escalation_{selected_scenario.replace(' ', '_').replace(',', '').lower()}.pdf",
            mime="application/pdf"
        )
    
    except Exception as e:
        st.error(f"Error: {e}")
