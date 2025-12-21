import smtplib
from email.mime.text import MIMEText
from email.header import Header


def send_email(login: str, password: str, subject: str, recipient_mail: str, msg_text: str) -> None:
    """
    :param login: логин почты
    :param password: пароль (нужно получить пароль приложения)
    :param subject: тема сообщения
    :param recipient_mail: почта получателя
    :param msg_text: текст сообщения
    """


    msg = MIMEText(f'{msg_text}', 'plain', 'utf-8')
    msg['Subject'] = Header(f'{subject}', 'utf-8')
    msg['To'] = (recipient_mail)

    server = smtplib.SMTP('smtp.gmail.com', 587, timeout=10)
    
    try:
        server.starttls()
        server.login(login, password)
        server.sendmail(login, recipient_mail, msg.as_string())

    except Exception as ex:
        print(ex)
        raise ConnectionError("535")
    
    finally:
        server.quit()


