import os
import yagmail
from dotenv import load_dotenv
import status_logger

load_dotenv()

# Variables
FROM = os.getenv('FROM_ADDRESS')
FROM_PASS = os.getenv('FROM_PASS')
TO = os.getenv('TO_ADDRESS')

try:
  status_logger.logger.info("Testing Yagmail module. Sending test email.")
  yag = yagmail.SMTP(FROM, FROM_PASS)

  subject = 'Can you read me?'
  body = "If so, then Yagmail is working with email & app password."

  yag.send(TO, subject, body)
  status_logger.logger.info("No errors encountered. Email sent. Check your inbox.")
except Exception as e:
  status_logger.logger.exception("Exception occured")
  print(e)