import email.message
import os
import smtplib

from fastapi import HTTPException, status


def send_mail(_email, TOKEN):

    try:
        URL: str = os.environ["URL_RESET_PWD"]
        EMAIL: str = os.environ["MAIL_USERNAME"]
        PASSWORD: str = os.environ["MAIL_PASSWORD"]
    except:
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Problems in the internal settings to send the recovery email",
        )
    else:
        try:
            body_html = f""" 
            <h2>Reset Password</h2>
            <p>Follow this link to reset the password for your user:</p>
            <p><a href="{URL}{TOKEN}">Reset Password</a></p>
            """

            msg = email.message.Message()
            msg["Subject"] = "Recover Password - Fast-Flask-API"
            msg["From"] = EMAIL
            msg["To"] = _email

            msg.add_header("Content-Type", "text/html")
            msg.set_payload(body_html)

            s = smtplib.SMTP("smtp.gmail.com: 587")
            s.starttls()

            s.login(msg["From"], PASSWORD)
            s.sendmail(msg["From"], [msg["To"]], msg.as_string().encode("utf-8"))
        except:
            raise HTTPException(
                status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Connection to email server failed",
            )
