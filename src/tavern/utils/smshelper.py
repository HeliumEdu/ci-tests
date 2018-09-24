import datetime
import os
import time

import pytz
import requests
from tavern.util.exceptions import TestFailError
from twilio.rest import Client

__author__ = 'Alex Laird'
__copyright__ = 'Copyright 2018, Helium Edu'
__version__ = '1.4.26'

_RETRIES = 20

_RETRY_DELAY = 3


def get_verification_code(response, phone, retry=0):
    client = Client(os.environ.get('PLATFORM_TWILIO_ACCOUNT_SID'), os.environ.get('PLATFORM_TWILIO_AUTH_TOKEN'))

    latest_message = None
    for message in client.messages.list(to=phone):
        if not latest_message or message.date_created > latest_message.date_created:
            latest_message = message

    now = datetime.datetime.now(pytz.utc)
    in_test_window = now - datetime.timedelta(
        seconds=30 + (retry * _RETRY_DELAY)) <= latest_message.date_created <= now + datetime.timedelta(
        seconds=30 + (retry * _RETRY_DELAY))
    if not latest_message or not in_test_window or 'Enter this verification code' not in latest_message.body:
        if retry < _RETRIES:
            time.sleep(_RETRY_DELAY)

            return get_verification_code(response, phone, retry + 1)
        else:
            raise TestFailError("The verification SMS was not received after {} retries.".format(retry))

    verification_code = int(latest_message.body.split('Helium\'s "Settings" page: ')[1])

    return {"sms_verification_code": verification_code}


def verify_reminder_marked_sent(response, env_api_host, token, reminder_id, retry=0):
    response = requests.get('{}/planner/reminders/{}/'.format(env_api_host, reminder_id),
                             headers={'Authorization': "Token " + token},
                             verify=False)

    if not (response.status_code == 200 and response.json()["sent"]):
        if retry < _RETRIES:
            time.sleep(_RETRY_DELAY)

            return verify_reminder_marked_sent(response, env_api_host, token, reminder_id, retry + 1)
        else:
            raise TestFailError("The reminder was not marked as \"sent\" after {} retries.".format(retry))

    return {}


def verify_reminder_received(response, phone, retry=0):
    client = Client(os.environ.get('PLATFORM_TWILIO_ACCOUNT_SID'), os.environ.get('PLATFORM_TWILIO_AUTH_TOKEN'))

    latest_message = None
    for message in client.messages.list(to=phone):
        if not latest_message or message.date_created > latest_message.date_created:
            latest_message = message

    now = datetime.datetime.now(pytz.utc)
    in_test_window = now - datetime.timedelta(
        seconds=30 + (retry * _RETRY_DELAY)) <= latest_message.date_created <= now + datetime.timedelta(
        seconds=30 + (retry * _RETRY_DELAY))
    if not latest_message or not in_test_window or 'CI Test Homework in American History' not in latest_message.body:
        if retry < _RETRIES:
            time.sleep(_RETRY_DELAY)

            return verify_reminder_received(response, phone, retry + 1)
        else:
            raise TestFailError("The reminder SMS was not received after {} retries.".format(retry))

    assert latest_message.body == '(CI Test Homework in American History on Tue, Apr 17 at 09:00 PM) CI test reminder message'

    return {}
