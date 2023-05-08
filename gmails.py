import smtplib, ssl, sys

port = 465  # For SSL
password = ""

# Create a secure SSL context
context = ssl.create_default_context()

with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
    server.login("", password)
    server.sendmail("", "", sys.argv[1])
