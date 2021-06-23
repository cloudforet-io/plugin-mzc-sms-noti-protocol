import base64
import json
import requests
import logging
from spaceone.notification.conf.megazone_sms_conf import MEGAZONE_SMS_CONF

from spaceone.core.connector import BaseConnector

__all__ = ['MegazoneSMSConnector']
_LOGGER = logging.getLogger(__name__)


class MegazoneSMSConnector(BaseConnector):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.encode_key = None

    def set_connector(self, access_key, secret_key):
        # Encode Key to base64 encoding
        self.encode_key = self.string_to_base64(f'{access_key}:{secret_key}')

    def request_send_message(self, title, body, to, **kwargs):
        request_url = f'{MEGAZONE_SMS_CONF["endpoint"]}/sms/v1/messages'

        body = {
            'type': kwargs.get('flowId', MEGAZONE_SMS_CONF['default']['type']),
            'contentType': kwargs.get('contentType', MEGAZONE_SMS_CONF['default']['content_type']),
            'title': title,
            'body': body,
            'from': kwargs.get('from', MEGAZONE_SMS_CONF['default']['from']),
            'to': to
        }

        _LOGGER.debug(f'[SMS Params] {body}')
        res = requests.post(request_url, data=json.dumps(body), headers=make_header(self.encode_key))
        _LOGGER.debug(f'[Megazone Message Response] Status: {res.status_code} {res.reason}')

    @staticmethod
    def string_to_base64(string):
        base64_bytes = base64.b64encode(string.encode('utf-8'))
        return base64_bytes.decode("UTF-8")


def make_header(auth_key):
    return {
        'Authorization': f'Basic {auth_key}',
        'Content-Type': 'application/json'
    }
