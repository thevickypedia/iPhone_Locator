# Stock Monitor
Your phone's location tracker using PyiCloudService including reverse geocoding

## Setup

1. git clone this repository

2. Run this command in your terminal to install necessary packages<br/>cd pyicloud/lib && pip3 install -r requirements.txt

2. Make sure you add the following env variables
* user - Apple user id (registered email address)
* pass - iCloud password
* SENDER - sender email address (verified via AWS SES)
* RECIPIENT - receiver email address (verified via AWS SES)
* DESIRED_LOCATION - any desired location (street name preferably, eg: Creek Vale Way)
* ACCESS_KEY - AWS access to authenticate into your AWS account
* SECRET_KEY - AWS secret key
* REGION=us-west-2

Note: The code was built from the scratch but it was built with an intention to share knowledge and for educational purpose.<br/>Parts of the code can be easily hard coded but left as env to increase reusability.<br/>The script is extremely customizable so remove/add parts of code where ever unnecessary.

Click to learn more about [pyicloud](https://pypi.org/project/pyicloud/) and [geopy](https://pypi.org/project/geopy/)