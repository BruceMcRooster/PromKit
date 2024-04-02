import base64
import io
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from credentials import get_credentials

import pyqrcode


# Based of the Gmail API documentation (https://developers.google.com/gmail/api/guides/sending#sending_messages)
def send_email(to: list[str]) -> dict | None:
    ticket_id = to[0]
    name = to[1]
    email = to[2]

    if not to[4] == 'Yes':  # If the user hasn't paid
        return

    try:
        service = build('gmail', 'v1', credentials=get_credentials())

        create_message = {
            'raw': generate_email(email, name, ticket_id)
        }
        send_message = (service.users().messages().send(
            userId="me", body=create_message).execute())
        print(F'Message Id: {send_message["id"]}')
    except HttpError as error:
        print(F'An error occurred: {error}')
        send_message = None
    return send_message


def generate_email(email: str, name: str, ticket_id: str) -> str:
    message = MIMEMultipart()

    message['To'] = email
    message['From'] = 'me'  # Gets determined by authenticated account
    message['Subject'] = 'Your digital prom ticket is here!'

    mime_image = MIMEImage(generate_qrcode(ticket_id, name).getvalue(), name=F'promQR.png')
    mime_image.add_header('Content-ID', '<qrcode>')

    message.attach(
        MIMEText(
            # TODO: Configure this with your email form,
            '<!DOCTYPE html><html lang="en" xmlns:o="urn:schemas-microsoft-com:office:office" xmlns:v="urn:schemas-microsoft-com:vml"> <head> <title>See you in Vegas!</title> <meta content="text/html; charset=utf-8" http-equiv="Content-Type" /> <meta content="width=device-width, initial-scale=1.0" name="viewport" /> <!--[if mso ]><xml ><o:OfficeDocumentSettings ><o:PixelsPerInch>96</o:PixelsPerInch ><o:AllowPNG /></o:OfficeDocumentSettings></xml ><![endif]--> <style> * { box-sizing: border-box; } body { margin: 0; padding: 0; } a[x-apple-data-detectors] { color: inherit !important; text-decoration: inherit !important; } #MessageViewBody a { color: inherit; text-decoration: none; } p { line-height: inherit; } .desktop_hide, .desktop_hide table { mso-hide: all; display: none; max-height: 0px; overflow: hidden; } .image_block img + div { display: none; } @media (max-width: 620px) { .desktop_hide table.icons-inner { display: inline-block !important; } .icons-inner { text-align: center; } .icons-inner td { margin: 0 auto; } .row-content { width: 100% !important; } .mobile_hide { display: none; } .stack .column { width: 100%; display: block; } .mobile_hide { min-height: 0; max-height: 0; max-width: 0; overflow: hidden; font-size: 0px; } .desktop_hide, .desktop_hide table { display: table !important; max-height: none !important; } .row-1 .column-1 .block-3.heading_block h1 { text-align: center !important; } } </style> </head> <body style=" background-color: #d3d3d3; margin: 0; padding: 0; -webkit-text-size-adjust: none; text-size-adjust: none; " > <div class="preheader" style=" display: none; font-size: 1px; color: #333333; line-height: 1px; max-height: 0px; max-width: 0px; opacity: 0; overflow: hidden; " > Hi ' + name.split()[0] + ', here\'s your digital ticket for prom this year. See you in Vegas! From the entire class of 2024, we hope you enjoy the wonderful prom we have prepared. </div> <table border="0" cellpadding="0" cellspacing="0" class="nl-container" role="presentation" style=" mso-table-lspace: 0pt; mso-table-rspace: 0pt; background-color: #d3d3d3; " width="100%" > <tbody> <tr> <td> <table align="center" border="0" cellpadding="0" cellspacing="0" class="row row-1" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt" width="100%" > <tbody> <tr> <td> <table align="center" border="0" cellpadding="0" cellspacing="0" class="row-content stack" role="presentation" style=" mso-table-lspace: 0pt; mso-table-rspace: 0pt; background-color: #fff; border-radius: 0; color: #000000; width: 600px; " width="600" > <tbody> <tr> <td class="column column-1" style=" mso-table-lspace: 0pt; mso-table-rspace: 0pt; font-weight: 400; text-align: left; padding-bottom: 5px; padding-top: 5px; vertical-align: top; border-top: 0px; border-right: 0px; border-bottom: 0px; border-left: 0px; " width="100%" > <table border="0" cellpadding="10" cellspacing="0" class="paragraph_block block-2" role="presentation" style=" mso-table-lspace: 0pt; mso-table-rspace: 0pt; word-break: break-word; " width="100%" > <tbody> <tr> <td class="pad"> <div style=" color: #ba181b; direction: ltr; font-family: Tahoma, Verdana, Segoe, sans-serif; font-size: 16px; font-weight: 400; letter-spacing: 0px; line-height: 120%; text-align: center; mso-line-height-alt: 19.2px; " > <p style="margin: 0"> ♠ &nbsp; ♥ &nbsp; ♣ &nbsp; ♦ </p> </div> </td> </tr> </tbody> </table> <table border="0" cellpadding="10" cellspacing="0" class="heading_block block-3" role="presentation" style=" mso-table-lspace: 0pt; mso-table-rspace: 0pt; " width="100%" > <tbody> <tr> <td class="pad"> <h1 style=" margin: 0; color: #000000; direction: ltr; font-family: Tahoma, Verdana, Segoe, sans-serif; font-size: 38px; font-weight: 700; letter-spacing: normal; line-height: 120%; text-align: center; margin-top: 0; margin-bottom: 0; " > <span class="tinyMce-placeholder" >See You In Vegas</span > </h1> </td> </tr> </tbody> </table> <table border="0" cellpadding="10" cellspacing="0" class="paragraph_block block-4" role="presentation" style=" mso-table-lspace: 0pt; mso-table-rspace: 0pt; word-break: break-word; " width="100%" > <tbody> <tr> <td class="pad"> <div style=" color: #101112; direction: ltr; font-family: Tahoma, Verdana, Segoe, sans-serif; font-size: 14px; font-weight: 400; letter-spacing: 0px; line-height: 120%; text-align: center; mso-line-height-alt: 16.8px; " > <p style="margin: 0; margin-bottom: 12px"> [DATE], [TIME] </p> <p style="margin: 0"> [ADDRESS] </p> </div> </td> </tr> </tbody> </table> </td> </tr> </tbody> </table> </td> </tr> </tbody> </table> <table align="center" border="0" cellpadding="0" cellspacing="0" class="row row-2" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt" width="100%" > <tbody> <tr> <td> <table align="center" border="0" cellpadding="0" cellspacing="0" class="row-content stack" role="presentation" style=" mso-table-lspace: 0pt; mso-table-rspace: 0pt; background-color: #f5f5f5; border-bottom: 5px solid #ba181b; border-radius: 0; border-top: 5px solid #ba181b; color: #000000; width: 600px; " width="600" > <tbody> <tr> <td class="column column-1" style=" mso-table-lspace: 0pt; mso-table-rspace: 0pt; font-weight: 400; text-align: left; padding-bottom: 5px; padding-top: 5px; vertical-align: top; border-top: 0px; border-right: 0px; border-bottom: 0px; border-left: 0px; " width="100%" > <table border="0" cellpadding="10" cellspacing="0" class="paragraph_block block-1" role="presentation" style=" mso-table-lspace: 0pt; mso-table-rspace: 0pt; word-break: break-word; " width="100%" > <tbody> <tr> <td class="pad"> <div style=" color: #101112; direction: ltr; font-family: Tahoma, Verdana, Segoe, sans-serif; font-size: 16px; font-weight: 400; letter-spacing: 0px; line-height: 120%; text-align: left; mso-line-height-alt: 19.2px; " > <p style="margin: 0"> Hi ' + name.split()[0] + ', so excited to see you at prom this year! We know you\'re going to love it! </p> </div> </td> </tr> </tbody> </table> <table border="0" cellpadding="0" cellspacing="0" class="image_block block-2" role="presentation" style=" mso-table-lspace: 0pt; mso-table-rspace: 0pt; " width="100%" > <tbody> <tr> <td class="pad" style=" width: 100%; padding-right: 0px; padding-left: 0px; " > <div align="center" class="alignment" style="line-height: 10px" > <img src="cid:qrcode" style=" display: block; height: auto; border: 0; width: 330px; max-width: 100%; " width="330" /> </div> </td> </tr> </tbody> </table> <table border="0" cellpadding="10" cellspacing="0" class="paragraph_block block-3" role="presentation" style=" mso-table-lspace: 0pt; mso-table-rspace: 0pt; word-break: break-word; " width="100%" > <tbody> <tr> <td class="pad"> <div style=" color: #101112; direction: ltr; font-family: Tahoma, Verdana, Segoe, sans-serif; font-size: 12px; font-weight: 400; letter-spacing: 0px; line-height: 120%; text-align: center; mso-line-height-alt: 14.399999999999999px; " > <p style="margin: 0"> <strong>ID ' + ticket_id + '</strong> </p> </div> </td> </tr> </tbody> </table> <table border="0" cellpadding="10" cellspacing="0" class="paragraph_block block-4" role="presentation" style=" mso-table-lspace: 0pt; mso-table-rspace: 0pt; word-break: break-word; " width="100%" > <tbody> <tr> <td class="pad"> <div style=" color: #101112; direction: ltr; font-family: Tahoma, Verdana, Segoe, sans-serif; font-size: 16px; font-weight: 400; letter-spacing: 0px; line-height: 120%; text-align: left; mso-line-height-alt: 19.2px; " > <p style="margin: 0"> Here\'s your personalized QR Code to enter. Please have it ready at the door. </p> </div> </td> </tr> </tbody> </table> </td> </tr> </tbody> </table> </td> </tr> </tbody> </table> <table align="center" border="0" cellpadding="0" cellspacing="0" class="row row-3" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt" width="100%" > <tbody> <tr> <td> <table align="center" border="0" cellpadding="0" cellspacing="0" class="row-content stack" role="presentation" style=" mso-table-lspace: 0pt; mso-table-rspace: 0pt; background-color: #fff; border-radius: 0; color: #000000; width: 600px; " width="600" > <tbody> <tr> <td class="column column-1" style=" mso-table-lspace: 0pt; mso-table-rspace: 0pt; font-weight: 400; text-align: left; padding-bottom: 5px; padding-top: 5px; vertical-align: top; border-top: 0px; border-right: 0px; border-bottom: 0px; border-left: 0px; " width="100%" > <table border="0" cellpadding="10" cellspacing="0" class="paragraph_block block-2" role="presentation" style=" mso-table-lspace: 0pt; mso-table-rspace: 0pt; word-break: break-word; " width="100%" > <tbody> <tr> <td class="pad"> <div style=" color: #101112; direction: ltr; font-family: Tahoma, Verdana, Segoe, sans-serif; font-size: 14px; font-weight: 400; letter-spacing: 0px; line-height: 120%; text-align: center; mso-line-height-alt: 16.8px; " > <p style="margin: 0"> You can order pictures <a href="https://www.geskusprint.com" style=" text-decoration: underline; color: #ba181b; " target="_blank" title="geskusprint.com" >here</a > with the unique code <strong style=" color: #ba181b; "> Y7KWBBYS </strong> </p> </div> </td> </tr> </tbody> </table> <table border="0" cellpadding="10" cellspacing="0" class="paragraph_block block-1" role="presentation" style=" mso-table-lspace: 0pt; mso-table-rspace: 0pt; word-break: break-word; " width="100%" > <tbody> <tr> <td class="pad"> <div style=" color: #101112; direction: ltr; font-family: Tahoma, Verdana, Segoe, sans-serif; font-size: 16px; font-weight: 400; letter-spacing: 0px; line-height: 120%; text-align: center; mso-line-height-alt: 19.2px; " > <p style="margin: 0"> <strong>Questions?</strong> </p> </div> </td> </tr> </tbody> </table> <table border="0" cellpadding="10" cellspacing="0" class="paragraph_block block-2" role="presentation" style=" mso-table-lspace: 0pt; mso-table-rspace: 0pt; word-break: break-word; " width="100%" > <tbody> <tr> <td class="pad"> <div style=" color: #101112; direction: ltr; font-family: Tahoma, Verdana, Segoe, sans-serif; font-size: 14px; font-weight: 400; letter-spacing: 0px; line-height: 120%; text-align: center; mso-line-height-alt: 16.8px; " > <p style="margin: 0"> Please get in touch with [NAME] (<a href="mailto:[EMAIL]" rel="noopener" style=" text-decoration: underline; color: #ba181b; " target="_blank" title="[EMAIL]" >[EMAIL]</a >) or [NAME] (<a href="mailto:[EMAIL]" rel="noopener" style=" text-decoration: underline; color: #ba181b; " target="_blank" title="[EMAIL]" >[EMAIL]</a >) with any questions. </p> </div> </td> </tr> </tbody> </table> <table border="0" cellpadding="10" cellspacing="0" class="paragraph_block block-3" role="presentation" style=" mso-table-lspace: 0pt; mso-table-rspace: 0pt; word-break: break-word; " width="100%" > <tbody> <tr> <td class="pad"> <div style=" color: #ba181b; direction: ltr; font-family: Tahoma, Verdana, Segoe, sans-serif; font-size: 16px; font-weight: 400; letter-spacing: 0px; line-height: 120%; text-align: center; mso-line-height-alt: 19.2px; " > <p style="margin: 0"> ♠ &nbsp; ♥ &nbsp; ♣ &nbsp; ♦ </p> </div> </td> </tr> </tbody> </table> </td> </tr> </tbody> </table> </td> </tr> </tbody> </table> </td> </tr> </tbody> </table> <!-- End --> </body></html>'
            , 'html'
        )
    )
    message.attach(mime_image)

    encoded_message = base64.urlsafe_b64encode(message.as_bytes()) \
        .decode()

    return encoded_message


def generate_qrcode(ticket_id: str, name: str) -> io.BytesIO:
    buffer = io.BytesIO()  # In-memory buffer
    qr = pyqrcode.create(F'{ticket_id}&{name}', error='Q')
    qr.png(buffer, scale=10, module_color=[186, 24, 27, 255], background=[245, 245, 245, 255])

    return buffer


if __name__ == "__main__":
    send_email(['0TP', 'Test Person', '', '12', 'Yes', 'N/A', 'No']) # TODO: Set up test email
