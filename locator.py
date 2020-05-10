#! /usr/bin/env python3
"""/**
 * Author:  Vignesh Sivanandha Rao
 * Created:   04.24.2020
 *
 **/"""

import os
import ssl
import sys
from datetime import datetime

import certifi
import geopy.geocoders
from geopy.geocoders import Nominatim
from pyicloud import PyiCloudService

from lib.emailer import Emailer

ctx = ssl.create_default_context(cafile=certifi.where())
geopy.geocoders.options.default_ssl_context = ctx

u = os.getenv('user')
p = os.getenv('pass')

now = datetime.now()
dt_string = now.strftime("%B %d, %Y %I:%M %p")

api = PyiCloudService(u, p)

if api.requires_2sa:
    import click

    print("Two-step authentication required. Your trusted devices are:")

    devices = api.trusted_devices
    for i, device in enumerate(devices):
        print("  %s: %s" % (i, device.get('deviceName',
                                          "SMS to %s" % device.get('phoneNumber'))))

    device = click.prompt('Which device would you like to use?', default=0)
    device = devices[device]
    if not api.send_verification_code(device):
        print("Failed to send verification code")
        sys.exit(1)

    code = click.prompt('Please enter validation code')
    if not api.validate_verification_code(device, code):
        print("Failed to verify verification code")
        sys.exit(1)


def locate():
    # runs locator for 10 times as iCloud generally struggles to get the accurate location during initial attempts
    global current_location
    for locator in range(10):
        # GET YOUR PHONE'S LOCATION
        raw_location = (api.iphone.location())

        raw_lat = (raw_location['latitude'])
        raw_long = (raw_location['longitude'])

        geo_locator = Nominatim(scheme='http', user_agent='test/1', timeout=3)
        locator = geo_locator.reverse(f'{raw_lat}, {raw_long}')
        current_location = locator.address
    return current_location


def status():
    # GET YOUR DEVICE's STATUS
    stat = api.iphone.status()
    battery = stat['batteryLevel'] * 100
    bat_percent = round(battery, 2)
    device_model = stat['deviceDisplayName']
    status_code = stat['deviceStatus']
    phone_name = stat['name']
    phone_status = f'Battery Percentage: {bat_percent}%\nModel: {device_model}\nResponse Code: {status_code}\nPhone ' \
                   f'Name: {phone_name} '
    return phone_status


def send_email(data, context):
    location = locate()
    keyword = os.getenv('DESIRED_LOCATION')
    stat = status()
    if keyword in location:
        print(f'Within {keyword}, currently at: {location}\n\nPhone Status\n{stat}')
    else:
        print(f'Outside {keyword}, currently at: {location}\n\nPhone Status\n{stat}')
        footer_text = "\n----------------------------------------------------------------" \
                      "----------------------------------------\n" \
                      "Data pulled using PyiCloudService including reverse geocoding"
        sender = f"Location Monitor <{os.getenv('SENDER')}>"
        recipient = [os.getenv('RECIPIENT')]
        title = f'Location Alert as of {dt_string}'
        text = f'Outside {keyword}, currently at: {location}\n\nPhone Status\n{stat}\n\n{footer_text}'
        email = Emailer(sender, recipient, title, text)
        return email


if __name__ == '__main__':
    send_email("data", "context")
