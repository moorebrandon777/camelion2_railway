from django.core.mail import EmailMessage

def email_message_send(subject, message,receiver):
    email = EmailMessage(
        subject,
        message,
        'Camelion Inc <customerservice@hmb-online.com>',
        [receiver],
        )
    email.content_subtype = "html"
    email.fail_silently = False
    email.send()
    return message