# -*- coding: utf-8
import email
import smtplib


def send_mail(p_to,
              p_subject,
              p_content,
              p_from = "noreply@localhost",
              p_host = "localhost",
              p_port = 25):
    l_data = email.mime.text.MIMEText(p_content, "plain", "UTF-8")
    l_data["Subject"] = p_subject
    l_data["From"] = p_from
    l_data["To"] = p_to
    l_smtp = smtplib.SMTP(p_host, p_port)
    l_smtp.sendmail(p_from, [p_to], l_data.as_string())
    l_smtp.quit()
