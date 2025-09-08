import smtplib
from email.mime.text import MIMEText

def send_email(recipient_email, subject, body):
    sender_email = "your_email@gmail.com"  # Replace with your email
    sender_password = "your_app_password"  # Replace with your app password

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = recipient_email

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(sender_email, sender_password)
            smtp.send_message(msg)
        print("Email sent successfully!")
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False

if __name__ == "__main__":
    # Example usage:
    # recipient = "i.anwar2004@gmail.com"
    # subject = "Product Change Notification"
    # body = "This is a test email for product changes."
    # send_email(recipient, subject, body)
    pass


