from mailjet_rest import Client
import os

from ..models import Claim


api_secret = os.environ.get("MJ_APIKEY_PRIVATE")
api_key = os.environ.get("MJ_APIKEY_PUBLIC")
emailFromSender = os.environ.get("EMAILFROMSENDER")

def verifyIfEmailToSendToClaimer(propertyId, propertyNumber):
	claimer = Claim.objects.filter(property=propertyId).all()
	if claimer:
		for i in claimer:
			sendEmailToClaimer(i.email, propertyNumber)


def sendEmailToClaimer(emailRecipient, number):
	mailjet = Client(auth=(api_key, api_secret), version='v3.1')
	data = {
	  'Messages': [
					{
							"From": {
									"Email": emailFromSender,
									"Name": "Me"
							},
							"To": [
									{
											"Email": emailRecipient,
											"Name": "You"
									}
							],
							"Subject": f"A new message related to {number}",
							"TextPart": "Hello!",
							"HTMLPart": f"<h3>Dear {emailRecipient},</h3><br /> there is a new message related to {number}"
					}
			]
	}
	result = mailjet.send.create(data=data)
	print(result.status_code)
	print(result.json())



{
  "Messages": [
    {
      "Status": "success",
      "To": [
        {
          "Email": "passenger@mailjet.com",
          "MessageID": "1234567890987654321",
          "MessageHref": "https://api.mailjet.com/v3/message/1234567890987654321"
        }
      ]
    }
  ]
}