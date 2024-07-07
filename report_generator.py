from fpdf import FPDF
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

def generate_report(journeys):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Mileage Report", ln=1, align='C')
    
    for journey in journeys:
        pdf.cell(200, 10, txt=f"{journey.start_time} to {journey.end_time}: {journey.distance:.2f} km ({journey.project})", ln=1)

    pdf_file = "mileage_report.pdf"
    pdf.output(pdf_file)
    return pdf_file

def send_email(config, attachment):
    message = MIMEMultipart()
    message["From"] = config.SENDER_EMAIL
    message["To"] = config.RECEIVER_EMAIL
    message["Subject"] = "Mileage Report"

    body = "Please find attached the mileage report."
    message.attach(MIMEText(body, "plain"))

    with open(attachment, "rb") as attachment:
        part = MIMEApplication(attachment.read(), Name="mileage_report.pdf")
    
    part['Content-Disposition'] = f'attachment; filename="mileage_report.pdf"'
    message.attach(part)

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(config.SENDER_EMAIL, config.EMAIL_PASSWORD)
            server.sendmail(config.SENDER_EMAIL, config.RECEIVER_EMAIL, message.as_string())
        print("Email sent successfully")
    except Exception as e:
        print(f"Error sending email: {e}")