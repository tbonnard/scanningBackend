# from mailjet_rest import Client
import os

import smtplib, ssl
from email.message import EmailMessage

from ..models import Claim


api_secret = os.environ.get("MJ_APIKEY_PRIVATE")
api_key = os.environ.get("MJ_APIKEY_PUBLIC")
emailFromSender = os.environ.get("EMAILFROMSENDER")

email_gmail = os.environ.get("email_gmail")
pwd_gmail = os.environ.get("pwd_gmail")
pwd_gmailAppPassword = os.environ.get("pwd_gmailAppPassword")


def verifyIfEmailToSendToClaimer(propertyId, propertyNumber):
	claimer = Claim.objects.filter(property=propertyId).all()
	print(claimer)
	if claimer:
		for i in claimer:
			sendEmailGmail(i.email, propertyNumber)


def sendEmailGmail(emailRecipient, number):
	port = 465  # For SSL
	smtp_server = "smtp.gmail.com"
	sender_email = email_gmail
	receiver_email = emailRecipient
	password = pwd_gmailAppPassword

	msg = EmailMessage()
	msg.set_content("You have received a new message related to your number. Open the website to check it!")
	msg['Subject'] = f"A new message related to {number}"
	msg['From'] = sender_email
	msg['To'] = receiver_email

	context = ssl.create_default_context()
	with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
		server.login(sender_email, password)
		server.send_message(msg, from_addr=sender_email, to_addrs=receiver_email)
		print('email sent')



#
#
# NOT USED
# def sendEmailToClaimer(emailRecipient, number):
# 	mailjet = Client(auth=(api_key, api_secret), version='v3.1')
# 	data = {
# 	  'Messages': [
# 					{
# 							"From": {
# 									"Email": emailFromSender,
# 									"Name": "Me"
# 							},
# 							"To": [
# 									{
# 											"Email": emailRecipient,
# 											"Name": "You"
# 									}
# 							],
# 							"Subject": f"A new message related to {number}",
# 							"TextPart": "Hello!",
# 							"HTMLPart": f"<h3>Dear {emailRecipient},</h3><br /> there is a new message related to {number}"
# 					}
# 			]
# 	}
# 	result = mailjet.send.create(data=data)
# 	print(result.status_code)
# 	print(result.json())
#
#

# {
#   "Messages": [
#     {
#       "Status": "success",
#       "To": [
#         {
#           "Email": "passenger@mailjet.com",
#           "MessageID": "1234567890987654321",
#           "MessageHref": "https://api.mailjet.com/v3/message/1234567890987654321"
#         }
#       ]
#     }
#   ]
# }



