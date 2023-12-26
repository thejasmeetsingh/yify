import smtplib
import traceback
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import config

logger = config.get_logger(name=__name__)


def create_multipart_message(
        sender: str,
        recipients: list,
        title: str,
        text: str = None,
        html: str = None
) -> MIMEMultipart:
    """
    Creates a MIME multipart message object.
    Uses only the Python `email` standard library.
    Emails, both sender and recipients, can be just the email string or have the format 'The Name <the_email@host.com>'.

    :param sender: The sender.
    :param recipients: List of recipients. Needs to be a list, even if only one recipient.
    :param title: The title of the email.
    :param text: The text version of the email body (optional).
    :param html: The html version of the email body (optional).
    :return: A `MIMEMultipart` to be used to send the email.
    """

    multipart_content_subtype = 'alternative' if text and html else 'mixed'
    msg = MIMEMultipart(multipart_content_subtype)
    msg['Subject'] = title
    msg['From'] = sender
    msg['To'] = ', '.join(recipients)

    # Record the MIME types of both parts - text/plain and text/html.
    # According to RFC 2046, the last part of a multipart message, in this case the HTML message, is best and preferred.
    if text:
        part = MIMEText(text, 'plain')
        msg.attach(part)
    if html:
        part = MIMEText(html, 'html')
        msg.attach(part)

    return msg


async def send_mail(
        title: str,
        text: str = None,
        html: str = None,
) -> bool:
    """
    Send email to recipient's, Using SMTP credentials.

    :param title: The title of the email.
    :param text: The text version of the email body (optional).
    :param html: The html version of the email body (optional).
    """

    # Use default email address to send free emails specifically while using AWS SES
    recipients = [config.DEFAULT_RECIPIENT_EMAIL]
    message = create_multipart_message(config.FROM_EMAIL, recipients, title, text, html)

    try:
        # Connect to the SMTP server
        with smtplib.SMTP(config.SMTP_SERVER, config.SMTP_PORT) as server:
            # Start TLS connection
            server.starttls()
            # Login to the SMTP server
            server.login(config.SMTP_USERNAME, config.SMTP_PASSWORD)
            # Send the email
            server.sendmail(config.FROM_EMAIL, recipients, message.as_string())

        logger.info("Email sent successfully!")
        return True

    except Exception as e:
        logger.error({
            "error": str(e),
            "traceback": traceback.format_exc()
        })
        return False
