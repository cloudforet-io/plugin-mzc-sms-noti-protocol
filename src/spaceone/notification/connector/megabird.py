import base64
import json
import requests
import logging
from spaceone.notification.conf.megabird_conf import *

from spaceone.core.connector import BaseConnector

__all__ = ['MegabirdConnector']
_LOGGER = logging.getLogger(__name__)


class MegabirdConnector(BaseConnector):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.headers = {}

    def set_connector(self, access_key):
        self.headers = make_header(access_key)

    def request_send_message(self, title, body, receivers, **kwargs):
        request_url = f'{ENDPOINT_URL}/v1/openapi/sms/send'

        if title is None:
            title = TITLE

        body = {
            'svcKndCd': TYPE,
            'msgTtl': title,
            'msgCotn': body,
            'adIncluYn': 'N',
            'snPhnum': SENDER,
            'messageReceiverList': self.set_message_receiver_list(receivers)
        }

        _LOGGER.debug(f'[MMS Params] {body}')
        res = requests.post(request_url, data=json.dumps(body), headers=self.headers)
        _LOGGER.debug(f'[Megabird Response] Status: {res.status_code} {res.reason}')

    @staticmethod
    def set_message_receiver_list(receivers):
        return [{'mbnum': receiver} for receiver in receivers]

def make_header(access_key):
    return {
        'Authorization': access_key,
        'Content-Type': 'application/json'
    }
