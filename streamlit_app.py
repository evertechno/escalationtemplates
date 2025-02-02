import streamlit as st
import google.generativeai as genai
from fpdf import FPDF

# Configure the API key securely from Streamlit's secrets
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

# Streamlit App UI
st.title("Email Escalation Response Generator")
st.write("Use Generative AI to create email escalation response templates based on different scenarios.")

# Category Dropdown
categories = [
    "Investigation Update", 
    "Issue Resolved", 
    "General Issues"
]
selected_category = st.selectbox("Select a category", categories)

# Define scenarios for each category
investigation_update_scenarios = [
    "Software bug escalation",
    "Escalation of unresolved technical issue",
    "Escalation regarding delayed contract approval",
    "Escalation regarding service outage",
    "Escalation due to unresolved software issue",
    "Escalation about unresolved server downtime",
    "Escalation regarding ongoing account access issues",
    "Escalation due to lack of proactive issue resolution",
    "Escalation regarding slow website performance"
]

issue_resolved_scenarios = [
    "Technical support escalation",
    "Billing or payment issue",
    "Complaint about product quality",
    "Request for urgent assistance",
    "Escalation due to faulty customer service",
    "Complaint about misleading advertising",
    "Escalation of broken product warranty claim",
    "Request for expedited product exchange",
    "Escalation about incorrect customer account details",
    "Complaint about suboptimal product functionality"
]

general_issues_scenarios = [
    "Customer service issue",
    "Delayed delivery apology",
    "Refund request escalation",
    "Shipping delay inquiry",
    "Employee misconduct report",
    "Late payment reminder",
    "Dispute over charges",
    "Request for account review",
    "Product malfunction report",
    "Complaint about customer service"
]

# Scenario selection based on category
if selected_category == "Investigation Update":
    selected_scenario = st.selectbox("Select an escalation scenario", investigation_update_scenarios)
elif selected_category == "Issue Resolved":
    selected_scenario = st.selectbox("Select an escalation scenario", issue_resolved_scenarios)
else:
    selected_scenario = st.selectbox("Select an escalation scenario", general_issues_scenarios)

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
