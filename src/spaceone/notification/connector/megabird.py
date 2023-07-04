import json
import requests
import logging

from spaceone.notification.conf import TITLE, SENDER, ENDPOINT_URL, TYPE
from spaceone.core.connector import BaseConnector

__all__ = ['MegabirdConnector']
_LOGGER = logging.getLogger(__name__)


class MegabirdConnector(BaseConnector):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.headers = {}

    def set_connector(self, access_key):
        self.headers = make_header(access_key)

    def request_send_message(self, title, notification_type, body, receivers, **kwargs):
        request_url = f'{ENDPOINT_URL}/v1/openapi/sms/send'

        msg_title = title if title else TITLE

        body = {
            'svcKndCd': TYPE,
            'msgTtl': f'{msg_title} - {notification_type}' if notification_type else msg_title,
            'msgCotn': body,
            'adIncluYn': 'N',
            'snPhnum': kwargs.get('sender', SENDER),
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
