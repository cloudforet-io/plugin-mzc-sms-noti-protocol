import logging
from spaceone.core.service import *

_LOGGER = logging.getLogger(__name__)


@authentication_handler
class ProtocolService(BaseService):

    def __init__(self, metadata):
        super().__init__(metadata)

    @check_required(['options'])
    def init(self, params):
        """ init plugin by options
        """
        return {'metadata': {
            'data_type': 'PLAIN_TEXT',
            'data': {
                'schema': {
                    'properties': {
                        'phone_number': {
                            'description': 'The phone number to receive alerts. Must insert the cell phone numbers format without special characters.',
                            'minLength': 10,
                            'title': 'Phone Number',
                            'type': 'string',
                            'pattern': '^(01([0|1|6|7|8|9]?)\d{7,8}(, |,|$))*',
                            'examples': ['0104445566, 01077778888']
                        }
                    },
                    'required': [
                        'phone_number'
                    ],
                    'type': 'object'
                }
            }
        }}

    @transaction
    @check_required(['options'])
    def verify(self, params):
        """
        Args:
              params:
                - options
                - secret_data
        """
        options = params['options']
        secret_data = params.get('secret_data', {})

        return {}
