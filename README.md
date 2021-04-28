![GitHub](https://img.shields.io/github/license/thevickypedia/iPhone_Locator) ![GitHub repo size](https://img.shields.io/github/repo-size/thevickypedia/iPhone_Locator) ![GitHub Repo stars](https://img.shields.io/github/stars/thevickypedia/iPhone_Locator) ![GitHub last commit](https://img.shields.io/github/last-commit/thevickypedia/iPhone_Locator)

# Stock Monitor
Your phone's location tracker using PyiCloudService including reverse geocoding

## Setup

1. Install necessary packages<br>
   `cd lib && pip3 install -r requirements.txt`

2. Make sure you add the following env variables
* `user` - Apple user id (registered email address)
* `pass` - iCloud password
* `SENDER` - sender email address (verified via AWS SES)
* `RECIPIENT` - receiver email address (verified via AWS SES)
* `DESIRED_LOCATION` - any desired location<br>

_Optional env vars_
* `ACCESS_KEY` - AWS access to authenticate into your AWS account
* `SECRET_KEY` - AWS secret key
* `REGION` - AWS region to access SES

`email = Emailer(sender, recipient, title, text)` can be replaced with any other sort of notification like `SMS via sockets` or `WhatsApp notification` using Twilio.

Learn more about [pyicloud](https://pypi.org/project/pyicloud/) and [geopy](https://pypi.org/project/geopy/)

## License & copyright

&copy; Vignesh Sivanandha Rao

Licensed under the [MIT License](LICENSE)
