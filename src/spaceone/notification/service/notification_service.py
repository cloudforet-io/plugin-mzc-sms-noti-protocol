import logging

from spaceone.core.service import *
from spaceone.core.utils import parse_endpoint
from spaceone.notification.manager.notification_manager import NotificationManager
from spaceone.notification.conf.megazone_sms_conf import MEGAZONE_SMS_CONF

_LOGGER = logging.getLogger(__name__)


@authentication_handler
class NotificationService(BaseService):

    def __init__(self, metadata):
        super().__init__(metadata)

    @transaction
    @check_required(['options', 'message', 'notification_type'])
    def dispatch(self, params):
        """
        Args:
            params:
                - options
                - message
                    - title
                    - description
                    - tags (list)
                        - key
                        - value
                        - options
                    - callbacks (list)
                        - url
                        - options
                - notification_type
                - secret_data:
                    - access_key
                    - secret_key
                - channel_data
                    - phone
        """

        secret_data = params.get('secret_data', {})
        channel_data = params.get('channel_data', {})
        notification_type = params['notification_type']
        params_message = params['message']

        access_key = secret_data.get('access_key')
        secret_key = secret_data.get('secret_key')
        phone_number = channel_data.get('phone_number')
        kwargs = {}

        body = self.make_sms_body(params_message, notification_type)

        noti_mgr: NotificationManager = self.locator.get_manager('NotificationManager')
        noti_mgr.dispatch(access_key, secret_key,
                          params_message.get('title', MEGAZONE_SMS_CONF['default']['title']),
                          body,
                          phone_number,
                          **kwargs)

    @staticmethod
    def make_sms_body(message, notification_type):
        body = f'알림 타입: {notification_type}\n\n{message.get("description", "")}\n'

        for tag in message.get('tags', []):
            tag_message = f'- {tag.get("key", "")}: {tag.get("value", "")}'

            body = f'{body}\n{tag_message}'

        # if 'callbacks' in message:
        #     callback_msg = ''
        #     for callback in message['callbacks']:
        #         callback_msg = f'{callback_msg}\n{callback.get("url")}'
        #
        #     body = f'{body}\n{callback_msg}'

        return body
