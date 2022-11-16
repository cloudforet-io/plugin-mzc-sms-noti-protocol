from spaceone.core.manager import BaseManager
from spaceone.notification.manager.megabird_manager import MegabirdManager


class NotificationManager(BaseManager):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def dispatch(self, access_key, title, body, receivers, **kwargs):
        megabird_mgr: MegabirdManager = self.locator.get_manager('MegabirdManager')
        megabird_mgr.set_connector(access_key)
        megabird_mgr.request_send_sms(title, body, receivers, **kwargs)
