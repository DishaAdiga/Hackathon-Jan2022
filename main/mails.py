import smtplib
from email.message import EmailMessage

def send_mail(price,name_1,name_2):
    msg = EmailMessage()

    my_msg = f"""Dear customer your ride is confirmed with {name_2} , Your ride payment {price}Rs is pending please click the below link to proceed
    link
    """
    msg.set_content(my_msg)
    msg['Subject'] = 'Carpool, Your ride'

    msg['From'] = "pran19cs@cmrit.ac.in"
    msg['To'] = "rakshith1553@gmail.com"
    print(msg)

    # Send the message via our own SMTP server.
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.login("pran19cs@cmrit.ac.in", "password_here")
    server.send_message(msg)
    server.quit()

send_mail(100,"prashanth","Disha")