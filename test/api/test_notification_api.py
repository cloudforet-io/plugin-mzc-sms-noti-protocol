import os
import logging

from spaceone.core import utils, config
from spaceone.tester import TestCase, print_json, to_json
from google.protobuf.json_format import MessageToDict

_LOGGER = logging.getLogger(__name__)

ACCESS_KEY = os.environ.get('ACCESS_KEY', None)
SECRET_KEY = os.environ.get('SECRET_KEY', None)
PHONE = os.environ.get('PHONE', None)
COUNTRY_CODE = os.environ.get('COUNTRY_CODE', None)


if ACCESS_KEY == None or SECRET_KEY == None:
    print("""
##################################################
# ERROR
#
# Configure your Slack Token first for test
##################################################
example)

export ACCESS_KEY=<MEGAZONE_MESSAGE_ACCESS_KEY>
export SECRET_KEY=<MEGAZONE_MESSAGE_SECRET_KEY>
""")
    exit


class TestVoiceCallNotification(TestCase):
    config = utils.load_yaml_from_file(
        os.environ.get('SPACEONE_TEST_CONFIG_FILE', './config.yml'))
    endpoints = config.get('ENDPOINTS', {})
    secret_data = {
        'access_key': ACCESS_KEY,
        'secret_key': SECRET_KEY,
    }
    channel_data = {
        'phone': PHONE,
    }

    def test_init(self):
        v_info = self.notification.Protocol.init({'options': {}})
        print_json(v_info)

    def test_verify(self):
        options = {}
        self.notification.Protocol.verify({'options': options, 'secret_data': self.secret_data})

    def test_dispatch(self):
        options = {}

        self.notification.Notification.dispatch({
            'options': options,
            'message': {
                'title': 'Alert 테스트',
                'description': '서버 장애가 발생하였습니다. SpaceONE 에서 자세한 정보를 확인해 주세요.',
                'tags': {
                    'project_id': 'project-xxxxx',
                    'project_name': '스페이스원 웹서버',
                    'resource_id': 'server-yyyyy',
                    'resource_name': 'web-server-001'
                },
                'callbacks': [{
                    'url': 'https://spaceone.console.doodle.spaceone.dev/monitoring/alert-system/alert/xxxxx'
                }
                ]
            },
            'notification_type': 'ERROR',
            'secret_data': self.secret_data,
            'channel_data': self.channel_data
        })
