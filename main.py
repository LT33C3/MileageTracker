import csv
import io
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.clock import Clock
from database import Database
from location_service import LocationService
from datetime import datetime
from config import EmailConfig

# Conditional import for smtplib
try:
    import smtplib
except ImportError:
    smtplib = None

class MileageTrackerApp(App):
    def build(self):
        self.db = Database()
        self.location_service = LocationService()
        self.layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Project selection
        self.project_spinner = Spinner(text='Select Project', values=('Project A', 'Project B', 'Project C'))
        self.layout.add_widget(self.project_spinner)
        
        # Start journey button
        self.start_button = Button(text='Start Journey', on_press=self.start_journey)
        self.layout.add_widget(self.start_button)
        
        # End journey button
        self.end_button = Button(text='End Journey', on_press=self.end_journey, disabled=True)
        self.layout.add_widget(self.end_button)
        
        # View all journeys button
        self.view_all_button = Button(text='View All Journeys', on_press=self.view_all_journeys)
        self.layout.add_widget(self.view_all_button)

        # Export to CSV button
        self.export_button = Button(text='Export to CSV', on_press=self.export_to_csv)
        self.layout.add_widget(self.export_button)

        # Email CSV button
        self.email_button = Button(text='Email CSV Report', on_press=self.email_csv_report)
        self.layout.add_widget(self.email_button)
        
        # Journey list
        self.journey_list = TextInput(readonly=True, size_hint_y=None, height=200)
        self.layout.add_widget(Label(text='Recent Journeys:'))
        self.layout.add_widget(self.journey_list)
        
        # Status label
        self.status_label = Label(text='Ready to start a new journey')
        self.layout.add_widget(self.status_label)
        
        self.load_journeys()
        return self.layout

    def start_journey(self, instance):
        if self.project_spinner.text == 'Select Project':
            self.status_label.text = 'Please select a project'
            return
        self.start_time = datetime.now()
        self.start_location = self.location_service.get_current_location()
        if not self.start_location:
            self.status_label.text = 'Failed to get start location. Please try again.'
            return
        self.status_label.text = f'Journey started at {self.start_time.strftime("%H:%M:%S")}'
        self.start_button.disabled = True
        self.end_button.disabled = False

    def end_journey(self, instance):
        end_time = datetime.now()
        end_location = self.location_service.get_current_location()
        if not end_location:
            self.status_label.text = 'Failed to get end location. Please try again.'
            return
        distance = self.location_service.calculate_distance(self.start_location, end_location)
        self.db.save_journey(
            start_time=self.start_time,
            end_time=end_time,
            start_location=self.start_location,
            end_location=end_location,
            distance=distance,
            project=self.project_spinner.text
        )
        self.status_label.text = f'Journey ended. Distance: {distance} km'
        self.load_journeys()
        self.reset_journey_inputs()

    def reset_journey_inputs(self):
        self.start_button.disabled = False
        self.end_button.disabled = True
        self.project_spinner.text = 'Select Project'

    def load_journeys(self):
        journeys = self.db.get_journeys()
        journey_texts = []
        for j in journeys[-5:]:  # Show only the last 5 journeys
            duration = j.end_time - j.start_time
            journey_texts.append(f"{j.start_time.strftime('%Y-%m-%d %H:%M')} | {j.start_location} to {j.end_location} | {j.distance:.2f} km | {duration} | {j.project}")
        self.journey_list.text = '\n'.join(journey_texts[::-1])  # Reverse order to show latest first

    def view_all_journeys(self, instance):
        journeys = self.db.get_journeys()
        journey_texts = []
        for j in journeys:
            duration = j.end_time - j.start_time
            journey_texts.append(f"{j.start_time.strftime('%Y-%m-%d %H:%M')} | {j.start_location} to {j.end_location} | {j.distance:.2f} km | {duration} | {j.project}")
        self.journey_list.text = '\n'.join(journey_texts[::-1])  # Reverse order to show latest first
        self.status_label.text = 'Displaying all journeys'

    def format_journey_for_csv(self, journey):
        return [
            journey.start_time.strftime('%Y-%m-%d %H:%M:%S'),
            journey.end_time.strftime('%Y-%m-%d %H:%M:%S'),
            journey.start_location,
            journey.end_location,
            f"{journey.distance:.2f}",
            journey.project
        ]

    def export_to_csv(self, instance):
        journeys = self.db.get_journeys()
        
        # Create a directory for reports if it doesn't exist
        reports_dir = 'mileage_reports'
        if not os.path.exists(reports_dir):
            os.makedirs(reports_dir)
        
        # Generate filename with timestamp
        filename = f'mileage_report_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
        filepath = os.path.join(reports_dir, filename)
        
        try:
            with open(filepath, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["Start Time", "End Time", "Start Location", "End Location", "Distance (km)", "Project"])
                for journey in journeys:
                    writer.writerow(self.format_journey_for_csv(journey))
            
            self.status_label.text = f'Report saved as {filename} in {reports_dir} folder'
        except Exception as e:
            self.status_label.text = f'Failed to save report: {str(e)}'

    def email_csv_report(self, instance):
        if smtplib is None:
            self.status_label.text = 'Email functionality not available on this platform'
            return

        journeys = self.db.get_journeys()
        
        # Create CSV in memory
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(["Start Time", "End Time", "Start Location", "End Location", "Distance (km)", "Project"])
        for journey in journeys:
            writer.writerow(self.format_journey_for_csv(journey))
        
        # Email setup
        msg = MIMEMultipart()
        msg['From'] = EmailConfig.SENDER_EMAIL
        msg['To'] = EmailConfig.RECEIVER_EMAIL
        msg['Subject'] = "Mileage Tracker Report"
        
        body = "Please find attached the mileage tracker report."
        msg.attach(MIMEText(body, 'plain'))
        
        # Attach CSV
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(output.getvalue().encode())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', "attachment; filename= mileage_report.csv")
        msg.attach(part)
        
        # Send email
        try:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(EmailConfig.SENDER_EMAIL, EmailConfig.EMAIL_PASSWORD)
            text = msg.as_string()
            server.sendmail(EmailConfig.SENDER_EMAIL, EmailConfig.RECEIVER_EMAIL, text)
            server.quit()
            self.status_label.text = 'Report sent to email successfully'
        except smtplib.SMTPAuthenticationError:
            self.status_label.text = 'Authentication failed. Check your email and password.'
        except smtplib.SMTPException as e:
            self.status_label.text = f'SMTP error occurred: {str(e)}'
        except Exception as e:
            self.status_label.text = f'An error occurred: {str(e)}'

if __name__ == '__main__':
    MileageTrackerApp().run()
