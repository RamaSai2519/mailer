import os
import time
import smtplib
import traceback
from email import encoders
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from playwright.sync_api import sync_playwright
from config import sender_email, sender_password, prusers_collection


class EmailSender:
    def __init__(self, image_url: str) -> None:
        self.image = image_url
        self.smtp_port = 587
        self.sender_email = sender_email
        self.smtp_server = "smtp.gmail.com"
        self.sender_password = sender_password

    def generate_pdf(self, user: dict) -> str | None:
        try:
            url = f"https://gitam-prerana.vercel.app/ticket?name={user.get('name', '')}&email={user.get('email', '')}&phone={user.get('phoneNumber', '')}&gitam={'GITAM Student' if user.get('gitamite', '') else 'Non-GITAM Student'}&image={self.image}"
            url = url.replace(" ", "%20")
            user_email = user.get('email').replace(".", "_").replace("@", "_")

            pdf_filename = f"ticket_{user_email}.pdf"
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)
                page = browser.new_page()
                page.goto(url)
                time.sleep(5)

                page.pdf(
                    path=pdf_filename,
                    format="Legal",
                    landscape=True,
                    print_background=False,
                    display_header_footer=False,
                    scale=1
                )
                browser.close()

            return pdf_filename
        except Exception as e:
            print(traceback.format_exc())
            print(f"Failed to generate PDF: {e}")
            return None

    def send_email(self, user: dict, recipient_email: str) -> bool:
        msg = MIMEMultipart()
        msg['Subject'] = "Prerana Fest 2024 Pass"
        msg['To'] = recipient_email
        msg['From'] = self.sender_email

        pdf_filename = self.generate_pdf(user)

        if pdf_filename:
            msg.attach(MIMEText("Please find the attached PDF for your Prerana Fest 2024 pass."))

            with open(pdf_filename, "rb") as pdf_file:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(pdf_file.read())
                encoders.encode_base64(part)
                part.add_header(
                    'Content-Disposition',
                    f'attachment; filename={pdf_filename}',
                )
                msg.attach(part)

            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.sender_email, self.sender_password)
            text = msg.as_string()
            server.sendmail(self.sender_email, recipient_email, text)
            os.remove(pdf_filename)
            prusers_collection.update_one({"email": user.get("email")}, {"$set": {"email_sent": True}})
            server.quit()
            return True
        else:
            return False
