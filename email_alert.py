import smtplib
from email.message import EmailMessage


def email_alert(subject: str, body: str, to: str, file_data: bytes, file_name: str):
    msg = EmailMessage()
    msg.set_content(body)
    msg['subject'] = subject
    msg['to'] = to
    msg.add_attachment(file_data, maintype='application', subtype='octet-stream', filename=file_name)

    user = "email.test.578.g4"
    msg['from'] = user
    password = "xjizmwppxcpntuiz"

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(user, password)
    server.send_message(msg)

    server.quit()


if __name__ == '__main__':
    email_alert("Hey", "What is up fam!?", "pcuesta0902@sdsu.edu")
