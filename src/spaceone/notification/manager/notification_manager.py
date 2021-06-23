from spaceone.core.manager import BaseManager
from spaceone.notification.manager.megazone_sms_manager import MegazoneSMSManager


class NotificationManager(BaseManager):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def dispatch(self, access_key, secret_key, title, body, to, **kwargs):
        mz_sms_mgr: MegazoneSMSManager = self.locator.get_manager('MegazoneSMSManager')
        mz_sms_mgr.set_connector(access_key, secret_key)
        mz_sms_mgr.request_send_sms(title, body, to, **kwargs)