from spaceone.core.manager import BaseManager
from spaceone.notification.connector.megazone_sms import MegazoneSMSConnector


class MegazoneSMSManager(BaseManager):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.mz_sms_connector: MegazoneSMSConnector = self.locator.get_connector('MegazoneSMSConnector')

    def set_connector(self, access_key, secret_key):
        self.mz_sms_connector.set_connector(access_key, secret_key)

    def request_send_sms(self, title, body, to, **kwargs):
        self.mz_sms_connector.request_send_message(title, body, to, **kwargs)
