import ssl
from datetime import datetime
from difflib import SequenceMatcher
from typing import Union, Dict, NoReturn

import certifi
import gmailconnector as gc
from geopy.exc import GeocoderUnavailable, GeopyError
from geopy.geocoders import Nominatim, options
from pyicloud import PyiCloudService
from pyicloud.exceptions import PyiCloudAPIResponseException
from pyicloud.services.findmyiphone import AppleDevice

from config import env, LOGGER

options.default_ssl_context = ssl.create_default_context(cafile=certifi.where())
geo_locator = Nominatim(scheme="http", user_agent="test/1", timeout=3)

icloud_api = PyiCloudService(apple_id=env.apple_id, password=env.password)


def device_selector(phrase: str) -> AppleDevice:
    """Selects a device using the received input string.

    Args:
        phrase: Takes the phrase spoken as an argument.

    Returns:
        AppleDevice:
        Returns the selected device from the class ``AppleDevice``
    """
    devices = [device for device in icloud_api.devices]
    devices_str = [{str(device).split(":")[0].strip(): str(device).split(":")[1].strip()} for device in devices]
    closest_match = [
        (SequenceMatcher(a=phrase, b=key).ratio() + SequenceMatcher(a=phrase, b=val).ratio()) / 2
        for device in devices_str for key, val in device.items()
    ]
    index = closest_match.index(max(closest_match))
    return icloud_api.devices[index]


def get_location_from_coordinates(coordinates: tuple) -> Dict:
    """Uses the latitude and longitude information to get the address information.

    Args:
        coordinates: Takes the latitude and longitude as a tuple.

    Returns:
        dict:
        Location address.
    """
    try:
        locator = geo_locator.reverse(coordinates, language="en")
        return locator.raw["address"]
    except (GeocoderUnavailable, GeopyError) as error:
        LOGGER.error(error)
        return {}


def location(device: AppleDevice) -> Union[None, dict]:
    """Gets the current location of an Apple device.

    Args:
        device: Particular Apple device that has to be located.

    Returns:
        dict:
        Dictionary of location information.
    """
    try:
        if raw_location := device.location():
            return get_location_from_coordinates(coordinates=(raw_location["latitude"], raw_location["longitude"]))
        else:
            LOGGER.error("Unable to retrieve location for the device: '%s'", device)
            return
    except PyiCloudAPIResponseException as error:
        LOGGER.error("Unable to retrieve location for the device: '%s'", device)
        LOGGER.error(error)
        return


def status(device: AppleDevice) -> str:
    """Queries the status of the device.

    Args:
        device: Takes the Apple device object as an argument.

    Returns:
        str:
        Returns the stringified version of the device status.
    """
    stat = device.status()
    return f"Battery Percentage: {round(stat.get('batteryLevel', 0) * 100, 2)}%\n" \
           f"Model: {stat.get('deviceDisplayName')}\n" \
           f"Response Code: {stat.get('deviceStatus')}\n" \
           f"Device Name: {stat.get('name')}"


def send_email(device_location: Dict[str, str], device_status: str) -> NoReturn:
    """Sends email in case the device is outside the location referred in env vars.

    Args:
        device_location: Location of the device in a dictionary.
        device_status: Status of the device.
    """
    LOGGER.info(device_status)
    if env.location in device_location.values():
        LOGGER.info("Within '%s', currently at: %s", env.location, device_location)
    else:
        LOGGER.warning("Outside '%s', currently at: %s", env.location, device_location)
        device_location = '\n'.join(device_location.values())
        text = f"Outside {env.location}, currently at: {device_location}\n\nPhone Status\n{device_status}"
        email_obj = gc.SendEmail(gmail_user=env.gmail_user, gmail_pass=env.gmail_pass)
        response = email_obj.send_email(subject=f"Location Alert as of {datetime.now().strftime('%B %d, %Y %I:%M %p')}",
                                        recipient=env.recipient, body=text,
                                        sender="Location Monitor")
        if response.ok:
            LOGGER.info(response.body)
        else:
            LOGGER.error(response.json())


def locate(phrase: str = env.device) -> NoReturn:
    """Initiate device location search and call appropriate functions.

    Args:
        phrase: Device name/identifier as a string.
    """
    if phrase:
        device = device_selector(phrase=phrase)
    else:
        device = icloud_api.iphone
    LOGGER.info("Device chosen: %s", device)
    device_location = location(device=device)
    device_status = status(device=device)
    send_email(device_location=device_location, device_status=device_status)


if __name__ == '__main__':
    locate(phrase='Macbook Pro 16"')
