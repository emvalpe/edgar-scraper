import smtplib, ssl, sys

port = 465  # For SSL
password = ""

message = ""
for i in range(len(sys.argv)):
    if i != 0:
        message = message + " " + sys.argv[i]


# Create a secure SSL context
context = ssl.create_default_context()

with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
    server.login("", password)
    server.sendmail("", "", message)
