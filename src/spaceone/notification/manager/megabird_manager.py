from spaceone.core.manager import BaseManager
from spaceone.notification.connector.megabird import MegabirdConnector


class MegabirdManager(BaseManager):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.megabird_connector: MegabirdConnector = self.locator.get_connector('MegabirdConnector')

    def set_connector(self, access_key):
        self.megabird_connector.set_connector(access_key)

    def request_send_sms(self, body, receivers, **kwargs):
        self.megabird_connector.request_send_message(body, receivers, **kwargs)
