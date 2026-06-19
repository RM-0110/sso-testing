import os
import smtplib

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def send_email(
    subject,
    body,
):

    sender_email = "riddhimann@navya.care"

    recipient_list = ["riddhimann@navya.care", "kirana@navya.care"]

    password = os.getenv(
        "APP_PASSWORD"
    )

    msg = MIMEMultipart()

    msg["From"] = sender_email

    msg["To"] = ", ".join(
        recipient_list
    )

    msg["Subject"] = subject

    msg.attach(
        MIMEText(
            body,
            "plain",
        )
    )

    server = smtplib.SMTP(
        "smtp.gmail.com",
        587,
    )

    server.starttls()

    server.login(
        sender_email,
        password,
    )

    server.sendmail(
        sender_email,
        recipient_list,
        msg.as_string(),
    )

    server.quit()

    print(
        f"Email sent to {len(recipient_list)} recipients."
    )
