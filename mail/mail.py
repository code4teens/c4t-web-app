from models import Email
from database import db_session
import re

def parse_email(email):
	response = {}
	regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

	email = str(email)
	email = email[2:-1]
	print(email)
	if (Email.query.filter_by(email=email).first()):
		response["response"] = 400
		response["message"] = "This email is already subscribed!"

	elif (re.fullmatch(regex, email)):
		response["response"] = 200
		response["message"] = "Thank you for subscribing!"
		mail = Email(email=email)
		db_session.add(mail)
		db_session.commit()

	else:
		response["response"] = 400
		response["message"] = "Invalid Email!"
	
	return response
