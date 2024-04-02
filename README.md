Warning: I haven't used this in a while. Its current state is unknown, but it worked in 2023.

# PromKit

This is a simple tool I created in 2023 to run our prom.
It enables a completely self-hosted prom ticketing system that uses emails and QR codes, making it suitable for use within school districts that have restrictions on emails from outside the district.

## Two Parts
RegistrationEngine registers users using a handy-dandy UI. Check-in-gine uses the device camera to scan QR codes and check in users.

## Setup
Setup consist of 3 parts

## Install dependencies
I recommend a pip virtual environment. I think you'll need:
* `google-api-python-client`, `google-auth-httplib2`, and `google-auth-oauthlib` for the google API
* `pyqrcode` for QR Code generation
* `playsound` for playing confirmation sounds in Check-in-gine
* `PySimpleGUI` for UI
* `opencv-python` for QR code scanning, though it might be the community edition. Can't remember

This is not comprehensive because I haven't used this in a while. If something needs installation while you're setting this up, open an issue. I'd love to make this more comprehensive

### Set up Google Cloud APIs
Get a token. I managed to do this without having to publish a project by adding any email addresses that would send emails or read the Google Sheet as test users.
Also, you need to configure your project to be able to access the Gmail and Google Sheets APIs.

### Create Email
Use some tool to create an HTML document for your email. Check out the current email set up in [registration_email.py](/RegistrationEngine/registration_email.py) on line 52.
The two important things are to change the image tag you include the QR Code in for creating (I would recommend you have an example when developing the email: the email generates at size 330x330) to have `src="cid:qrcode"` instead. This references the QR Code that is included to show it in the message. Also, you will need to insert the name and ID for the email. Again, see the example.

Sorry I'm not more help because I haven't used this in a while, but good luck!