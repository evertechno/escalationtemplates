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
    "Request for better support resolution",
    "Escalation due to missing features",
    "Request for better product customization",
    "Escalation for unsatisfactory repair service",
    "Complaint about employee professionalism",
    "Order misplacement escalation",
    "Urgent product replacement request",
    "Complaint about delayed response time",
    "Request for higher priority resolution",
    "Escalation of unresolved refund request",
    "Complaint about misleading advertising",
    "Urgent issue with product compatibility",
    "Escalation of unresolved service contract dispute",
    "Complaint about billing discrepancy",
    "Request for immediate issue resolution",
    "Escalation due to faulty customer service",
    "Complaint about website functionality",
    "Delayed payment dispute escalation",
    "Complaint about poor customer experience",
    "Escalation of broken product warranty claim",
    "Request for change in service plan",
    "Unresolved service request escalation",
    "Complaint about unsatisfactory delivery",
    "Request for expedited service",
    "Escalation of unsolved network issue",
    "Product defect escalation",
    "Urgent concern about data privacy",
    "Escalation regarding service outage",
    "Complaint about hidden fees",
    "Escalation of unresolved technical issue",
    "Escalation for lack of proactive communication",
    "Complaint about overcharging",
    "Request for immediate product recall",
    "Escalation due to unresponsive sales team",
    "Complaint about substandard service level",
    "Escalation about unresolved dispute over terms",
    "Complaint about product underperformance",
    "Escalation for lack of technical expertise",
    "Request for urgent technical assistance",
    "Escalation regarding delayed contract approval",
    "Complaint about incorrect billing charges",
    "Escalation about unauthorized charge",
    "Request for timely account review",
    "Urgent escalation for lost customer data",
    "Complaint about incomplete order fulfillment",
    "Request for expedited product exchange",
    "Escalation due to communication breakdown",
    "Complaint about missing customer service follow-up",
    "Request for clearer contract terms",
    "Escalation regarding false advertising claims",
    "Complaint about poor product instructions",
    "Escalation regarding shipping discrepancies",
    "Escalation due to unresolved warranty issue",
    "Complaint about repeated service failure",
    "Request for higher service tier",
    "Escalation for unsatisfactory product demo",
    "Complaint about unaddressed technical issue",
    "Escalation regarding delay in product launch",
    "Complaint about software not meeting needs",
    "Request for faster resolution time",
    "Escalation due to unresolved invoice issues",
    "Complaint about excessive service downtime",
    "Request for resolution of faulty installation",
    "Escalation regarding poor product packaging",
    "Complaint about poor customer support follow-up",
    "Escalation regarding unexpected product failure",
    "Request for updated service terms",
    "Escalation due to misleading product information",
    "Complaint about defective product delivery",
    "Request for resolution of employee behavior",
    "Escalation about inconsistent service levels",
    "Complaint about suboptimal product functionality",
    "Request for immediate assistance with urgent matter",
    "Request for refund for poor service",
    "Complaint about inconsistent billing",
    "Escalation for faulty online payment gateway",
    "Request for update on unresolved support ticket",
    "Complaint about unresponsive customer support",
    "Escalation about security breach",
    "Complaint about poor refund process",
    "Escalation regarding software compatibility issue",
    "Complaint about missing support documentation",
    "Escalation about poor training resources",
    "Request for resolution of misleading warranty information",
    "Escalation due to unresolved technical service issue",
    "Request for urgent update on product status",
    "Escalation due to poor after-sales service",
    "Complaint about unprofessional behavior from support staff",
    "Escalation due to unresolved maintenance request",
    "Complaint about inaccurate product descriptions",
    "Escalation regarding unresolved server downtime",
    "Request for expedited order fulfillment",
    "Escalation about long wait times for support",
    "Complaint about incorrect shipping address",
    "Escalation about poor user interface design",
    "Complaint about incorrect product recommendation",
    "Request for faster account verification",
    "Escalation regarding lack of communication on support tickets",
    "Complaint about outdated product features",
    "Request for improved service uptime",
    "Escalation due to unresolved customer service issues",
    "Complaint about customer service's lack of empathy",
    "Escalation regarding unmet service level agreement",
    "Request for compensation for poor service",
    "Escalation of payment error dispute",
    "Complaint about missing product components",
    "Escalation due to lack of product availability",
    "Request for better service experience",
    "Escalation about recurring issues with service",
    "Complaint about billing mischarges",
    "Escalation regarding product recall update",
    "Request for clarification on contract renewal terms",
    "Complaint about poor technical support follow-up",
    "Escalation about failure to meet delivery expectations",
    "Request for refund due to service interruption",
    "Complaint about lack of product customization options",
    "Escalation regarding ongoing account access issues",
    "Complaint about misleading advertising in promotions",
    "Request for resolution of feature incompatibilities",
    "Escalation regarding slow website performance",
    "Complaint about incorrect order processing",
    "Request for expedited delivery of replacement item",
    "Escalation regarding non-functional product features",
    "Complaint about defective installation of service",
    "Request for improvement in service process",
    "Escalation about lack of support for existing product",
    "Request for account reactivation",
    "Complaint about inefficient service resolution",
    "Escalation regarding poor customer feedback handling",
    "Complaint about product not as advertised",
    "Escalation about incorrect customer account details",
    "Request for clarification on payment plan options",
    "Complaint about unresolved technical issue with service",
    "Escalation regarding lack of updates on request status",
    "Complaint about unexpected service charges",
    "Request for alternative product recommendation",
    "Escalation due to unresolved software issue",
    "Complaint about missing item in delivery",
    "Escalation for slow response to technical problem",
    "Request for updated service protocol",
    "Escalation regarding incorrect tracking information",
    "Complaint about failure to meet product specifications",
    "Request for better resolution time for complaints",
    "Escalation due to delayed order processing",
    "Complaint about inaccurate customer support advice",
    "Request for alternative compensation options",
    "Escalation about vendor communication breakdown",
    "Complaint about difficulty reaching support",
    "Request for status update on project",
    "Escalation due to lack of proactive issue resolution",
    "Complaint about unclear terms and conditions",
    "Request for faster technical troubleshooting",
    "Escalation regarding delayed software update",
    "Complaint about poor quality control",
    "Request for direct communication with management",
    "Escalation due to incorrect product features",
    "Complaint about unnotified service outages",
    "Request for urgent resolution on technical issues",
    "Escalation due to repeated service failures",
    "Complaint about lost data recovery attempt",
    "Request for clarification on refund policies",
    "Escalation regarding customer service mistakes",
    "Complaint about delayed warranty processing",
    "Request for more detailed product specifications",
    "Escalation regarding unresolved dispute",
    "Complaint about inefficient technical support team",
    "Request for higher support escalation",
    "Escalation about product non-compliance",
    "Complaint about unsatisfactory product demo experience",
    "Request for updates on incomplete order",
    "Escalation for failure to provide requested service",
    "Complaint about unresolved service feedback",
    "Request for support with installation issue"
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
