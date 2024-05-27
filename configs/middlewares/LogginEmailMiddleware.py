from django.utils.log import AdminEmailHandler

from django.core.mail import EmailMessage
import logging

logger = logging.Logger(__name__)

# def email_deliveri(self, subject, message):
#     mailer = EmailMessage(
#         subject, message, "oiarregoces@uniguajira.edu.co", ['oiarregoces@uniguajira.edu.co']
#     )
#     try:
#         mailer.send()
#     except Exception as e:
#         print(e)


# class CustomEmailHandler(AdminEmailHandler):
#     def send_mail(self, subject, message, *args, **kwargs):
#         email_deliveri(self,subject=subject, message=message)  # type:ignore


