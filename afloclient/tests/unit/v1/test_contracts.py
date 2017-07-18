#  Licensed under the Apache License, Version 2.0 (the "License"); you may
#  not use this file except in compliance with the License. You may obtain
#  a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#  WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#  License for the specific language governing permissions and limitations
#  under the License.

from afloclient.tests.unit import utils
from afloclient.v1 import contracts
from datetime import datetime
from six.moves.urllib import parse
import testtools

CONTRACT_ID_101 = 'ea0a4146-fd07-414b-aa5e-dedbeef00101'
CONTRACT_ID_102 = 'ea0a4146-fd07-414b-aa5e-dedbeef00102'
CONTRACT_ID_103 = 'ea0a4146-fd07-414b-aa5e-dedbeef00103'
CONTRACT_ID_104 = 'ea0a4146-fd07-414b-aa5e-dedbeef00104'
CONTRACT_ID_105 = 'ea0a4146-fd07-414b-aa5e-dedbeef00105'
CONTRACT_ID_106 = 'ea0a4146-fd07-414b-aa5e-dedbeef00106'
CONTRACT_ID_107 = 'ea0a4146-fd07-414b-aa5e-dedbeef00107'
CONTRACT_ID_108 = 'ea0a4146-fd07-414b-aa5e-dedbeef00108'

contract_101 = \
    {
        'contract_id': 'ea0a4146-fd07-414b-aa5e-dedbeef00001',
        'project_id': 'project_id_101',
        'region_id': 'region_id_101',
        'status': 'applied_101',
        'project_name': 'project_name_101',
        'catalog_id': 'catalog_id_101',
        'catalog_name': 'catalog_name_101',
        'num': 101,
        'parent_ticket_template_id': 'parent_ticket_template_id_101',
        'ticket_template_id': 'ticket_template_id_101',
        'parent_ticket_template_name': 'parent_ticket_template_name_101',
        'parent_application_kinds_name': 'parent_application_kinds_name_101',
        'application_kinds_name': 'application_kinds_name_101',
        'cancel_application_id': 'cancel_application_id_101',
        'application_id': 'application_id_101',
        'ticket_template_name': 'ticket_template_name_101',
        'application_name': 'application_name_101',
        'application_date': datetime(2015, 6, 1, 0, 0, 0, 0),
        'parent_contract_id': 'parent_contract_id_101',
        'lifetime_start': datetime(2015, 7, 1, 0, 0, 0, 0),
        'lifetime_end': datetime(2015, 8, 1, 0, 0, 0, 0),
        'created_at': datetime(2015, 7, 30, 1, 2, 3, 4),
        'updated_at': datetime(2015, 7, 30, 1, 2, 3, 4),
        'deleted_at': None,
        'deleted': False,
        'expansions': {'expansion_key1': 'expansion_key1',
                       'expansion_key2': 'expansion_key2',
                       'expansion_key3': 'expansion_key3',
                       'expansion_key4': 'expansion_key4',
                       'expansion_key5': 'expansion_key5',
                       },
        'expansions_text': {'expansion_text': 'expansion_text'}
    }

contract_list_101 = \
    {
        'contract_id': CONTRACT_ID_101,
        'region_id': 'region_id_101',
        'project_id': 'project_id_101',
        'status': 'applied_101',
        'project_name': 'project_name_101',
        'catalog_id': 'catalog_id_101',
        'catalog_name': 'catalog_name_101',
        'num': 101,
        'parent_ticket_template_id': 'parent_ticket_template_id_101',
        'ticket_template_id': 'ticket_template_id_101',
        'parent_ticket_template_name': 'parent_ticket_template_name_101',
        'parent_application_kinds_name': 'parent_application_kinds_name_101',
        'application_kinds_name': 'application_kinds_name_101',
        'cancel_application_id': 'cancel_application_id_101',
        'application_id': 'application_id_101',
        'ticket_template_name': 'ticket_template_name_101',
        'application_name': 'application_name_101',
        'application_date': datetime(2015, 6, 1, 0, 0, 0, 0),
        'parent_contract_id': 'parent_contract_id_101',
        'lifetime_start': '2015-07-01',
        'lifetime_end': '2015-08-01',
        'created_at': datetime.now(),
        'updated_at': None,
        'updated_at': None,
        'deleted': False,
        'expansions': {'expansion_key1': 'expansion_key1',
                       'expansion_key2': 'expansion_key2',
                       'expansion_key3': 'expansion_key3',
                       'expansion_key4': 'expansion_key4',
                       'expansion_key5': 'expansion_key5'},
        'expansions_text': {'expansion_text': 'expansion_text'}
    }

contract_list_102 = \
    {
        'contract_id': CONTRACT_ID_102,
        'region_id': 'region_id_101',
        'project_id': 'project_id_101',
        'status': 'applied_102',
        'project_name': 'project_name_102',
        'catalog_id': 'catalog_id_102',
        'catalog_name': 'catalog_name_102',
        'num': 102,
        'parent_ticket_template_id': 'parent_ticket_template_id_102',
        'ticket_template_id': 'ticket_template_id_102',
        'parent_ticket_template_name': 'parent_ticket_template_name_102',
        'parent_application_kinds_name': 'parent_application_kinds_name_102',
        'application_kinds_name': 'application_kinds_name_102',
        'cancel_application_id': 'cancel_application_id_102',
        'application_id': 'application_id_102',
        'ticket_template_name': 'ticket_template_name_102',
        'application_name': 'application_name_102',
        'application_date': datetime(2015, 6, 2, 0, 0, 0, 0),
        'parent_contract_id': 'parent_contract_id_102',
        'lifetime_start': '2015-07-02',
        'lifetime_end': '2015-08-02',
        'created_at': datetime.now(),
        'updated_at': datetime.now(),
        'deleted_at': None,
        'deleted': False,
        'expansions': {'expansion_key1': 'expansion_key1',
                       'expansion_key2': 'expansion_key2',
                       'expansion_key3': 'expansion_key3',
                       'expansion_key4': 'expansion_key4',
                       'expansion_key5': 'expansion_key5'},
        'expansions_text': {'expansion_text': 'expansion_text'}
    }

contract_list_103 = \
    {
        'contract_id': CONTRACT_ID_103,
        'region_id': 'region_id_101',
        'project_id': 'project_id_101',
        'status': 'applied_103',
        'project_name': 'project_name_101',
        'catalog_id': 'catalog_id_103',
        'catalog_name': 'catalog_name_103',
        'num': 103,
        'parent_ticket_template_id': 'parent_ticket_template_id_103',
        'ticket_template_id': 'ticket_template_id_103',
        'parent_ticket_template_name': 'parent_ticket_template_name_103',
        'parent_application_kinds_name': 'parent_application_kinds_name_103',
        'application_kinds_name': 'application_kinds_name_103',
        'cancel_application_id': 'cancel_application_id_103',
        'application_id': 'application_id_103',
        'ticket_template_name': 'ticket_template_name_103',
        'application_name': 'application_name_103',
        'application_date': datetime(2015, 6, 3, 0, 0, 0, 0),
        'parent_contract_id': 'parent_contract_id_103',
        'lifetime_start': '2015-07-03',
        'lifetime_end': '2015-08-03',
        'created_at': datetime.now(),
        'updated_at': datetime.now(),
        'deleted_at': None,
        'deleted': False,
        'expansions': {'expansion_key1': 'expansion_key1',
                       'expansion_key2': 'expansion_key2',
                       'expansion_key3': 'expansion_key3',
                       'expansion_key4': 'expansion_key4',
                       'expansion_key5': 'expansion_key5'},
        'expansions_text': {'expansion_text': 'expansion_text'}
    }

contract_list_104 = \
    {
        'contract_id': CONTRACT_ID_104,
        'region_id': 'region_id_101',
        'project_id': 'project_id_101',
        'status': 'applied_104',
        'project_name': 'project_name_101',
        'catalog_id': 'catalog_id_104',
        'catalog_name': 'catalog_name_104',
        'num': 104,
        'parent_ticket_template_id': 'parent_ticket_template_id_104',
        'ticket_template_id': 'ticket_template_id_104',
        'parent_ticket_template_name': 'parent_ticket_template_name_104',
        'parent_application_kinds_name': 'parent_application_kinds_name_104',
        'application_kinds_name': 'application_kinds_name_104',
        'cancel_application_id': 'cancel_application_id_104',
        'application_id': 'application_id_104',
        'ticket_template_name': 'ticket_template_name_104',
        'application_name': 'application_name_104',
        'application_date': datetime(2015, 6, 4, 0, 0, 0, 0),
        'parent_contract_id': 'parent_contract_id_104',
        'lifetime_start': '2015-07-04',
        'lifetime_end': '2015-08-04',
        'created_at': datetime.now(),
        'updated_at': datetime.now(),
        'deleted_at': None,
        'deleted': False,
        'expansions': {'expansion_key1': 'expansion_key1',
                       'expansion_key2': 'expansion_key2',
                       'expansion_key3': 'expansion_key3',
                       'expansion_key4': 'expansion_key4',
                       'expansion_key5': 'expansion_key5'},
        'expansions_text': {'expansion_text': 'expansion_text'}
    }

contract_list_105 = \
    {
        'contract_id': CONTRACT_ID_105,
        'region_id': 'region_id_102',
        'project_id': 'project_id_102',
        'status': 'applied_105',
        'project_name': 'project_name_102',
        'catalog_id': 'catalog_id_105',
        'catalog_name': 'catalog_name_105',
        'num': 105,
        'parent_ticket_template_id': 'parent_ticket_template_id_105',
        'ticket_template_id': 'ticket_template_id_105',
        'parent_ticket_template_name': 'parent_ticket_template_name_105',
        'parent_application_kinds_name': 'parent_application_kinds_name_105',
        'application_kinds_name': 'application_kinds_name_105',
        'cancel_application_id': 'cancel_application_id_105',
        'application_id': 'application_id_105',
        'ticket_template_name': 'ticket_template_name_105',
        'application_name': 'application_name_105',
        'application_date': datetime(2015, 6, 5, 0, 0, 0, 0),
        'parent_contract_id': 'parent_contract_id_105',
        'lifetime_start': '2015-07-05',
        'lifetime_end': '2015-08-05',
        'created_at': datetime.now(),
        'updated_at': datetime.now(),
        'deleted_at': None,
        'deleted': False,
        'expansions': {'expansion_key1': 'expansion_key1',
                       'expansion_key2': 'expansion_key2',
                       'expansion_key3': 'expansion_key3',
                       'expansion_key4': 'expansion_key4',
                       'expansion_key5': 'expansion_key5'},
        'expansions_text': {'expansion_text': 'expansion_text'}
    }

contract_list_106 = \
    {
        'contract_id': CONTRACT_ID_106,
        'region_id': 'region_id_102',
        'project_id': 'project_id_102',
        'status': 'applied_106',
        'project_name': 'project_name_102',
        'catalog_id': 'catalog_id_106',
        'catalog_name': 'catalog_name_106',
        'num': 106,
        'parent_ticket_template_id': 'parent_ticket_template_id_106',
        'ticket_template_id': 'ticket_template_id_106',
        'parent_ticket_template_name': 'parent_ticket_template_name_106',
        'parent_application_kinds_name': 'parent_application_kinds_name_106',
        'application_kinds_name': 'application_kinds_name_106',
        'cancel_application_id': 'cancel_application_id_106',
        'application_id': 'application_id_106',
        'ticket_template_name': 'ticket_template_name_106',
        'application_name': 'application_name_106',
        'application_date': datetime(2015, 6, 6, 0, 0, 0, 0),
        'parent_contract_id': 'parent_contract_id_106',
        'lifetime_start': '2015-07-06',
        'lifetime_end': '2015-08-06',
        'created_at': datetime.now(),
        'updated_at': datetime.now(),
        'deleted_at': None,
        'deleted': False,
        'expansions': {'expansion_key1': 'expansion_key1',
                       'expansion_key2': 'expansion_key2',
                       'expansion_key3': 'expansion_key3',
                       'expansion_key4': 'expansion_key4',
                       'expansion_key5': 'expansion_key5'},
        'expansions_text': {'expansion_text': 'expansion_text'}
    }

contract_list_107 = \
    {
        'contract_id': CONTRACT_ID_107,
        'region_id': 'region_id_102',
        'project_id': 'project_id_102',
        'status': 'applied_107',
        'project_name': 'project_name_102',
        'catalog_id': 'catalog_id_107',
        'catalog_name': 'catalog_name_107',
        'num': 107,
        'parent_ticket_template_id': 'parent_ticket_template_id_107',
        'ticket_template_id': 'ticket_template_id_107',
        'parent_ticket_template_name': 'parent_ticket_template_name_107',
        'parent_application_kinds_name': 'parent_application_kinds_name_107',
        'application_kinds_name': 'application_kinds_name_107',
        'cancel_application_id': 'cancel_application_id_107',
        'application_id': 'application_id_107',
        'ticket_template_name': 'ticket_template_name_107',
        'application_name': 'application_name_107',
        'application_date': datetime(2015, 6, 7, 0, 0, 0, 0),
        'parent_contract_id': 'parent_contract_id_107',
        'lifetime_start': None,
        'lifetime_end': None,
        'created_at': datetime.now(),
        'updated_at': datetime.now(),
        'deleted_at': None,
        'deleted': False,
        'expansions': {'expansion_key1': 'expansion_key1',
                       'expansion_key2': 'expansion_key2',
                       'expansion_key3': 'expansion_key3',
                       'expansion_key4': 'expansion_key4',
                       'expansion_key5': 'expansion_key5'},
        'expansions_text': {'expansion_text': 'expansion_text'}
    }

contract_list_108 = \
    {
        'contract_id': CONTRACT_ID_108,
        'region_id': 'region_id_102',
        'project_id': 'project_id_102',
        'status': 'applied_108',
        'project_name': 'project_name_102',
        'catalog_id': 'catalog_id_108',
        'catalog_name': 'catalog_name_108',
        'num': 108,
        'parent_ticket_template_id': 'parent_ticket_template_id_108',
        'ticket_template_id': 'ticket_template_id_108',
        'parent_ticket_template_name': 'parent_ticket_template_name_108',
        'parent_application_kinds_name': 'parent_application_kinds_name_108',
        'application_kinds_name': 'application_kinds_name_108',
        'cancel_application_id': 'cancel_application_id_108',
        'application_id': 'application_id_108',
        'ticket_template_name': 'ticket_template_name_108',
        'application_name': 'application_name_108',
        'application_date': datetime(2015, 6, 8, 0, 0, 0, 0),
        'parent_contract_id': 'parent_contract_id_108',
        'lifetime_start': '2015-07-08',
        'lifetime_end': '2015-08-08',
        'created_at': datetime.now(),
        'updated_at': datetime.now(),
        'deleted_at': datetime.now(),
        'deleted': True,
        'expansions': {'expansion_key1': 'expansion_key1',
                       'expansion_key2': 'expansion_key2',
                       'expansion_key3': 'expansion_key3',
                       'expansion_key4': 'expansion_key4',
                       'expansion_key5': 'expansion_key5'},
        'expansions_text': {'expansion_text': 'expansion_text'}
    }

# from afloclient.v1 import client
#  request fixtures
#    (request url, request header, request parameter).
fixtures = \
    {
        '/v1/contract': {
            'POST': (
                {},
                {'contract': contract_101},
            ),
            'GET': (
                {},
                {'contract': [contract_list_107,
                              contract_list_106,
                              contract_list_105,
                              contract_list_104,
                              contract_list_103,
                              contract_list_102,
                              contract_list_101]},
            )
        },
        '/v1/contract/ea0a4146-fd07-414b-aa5e-dedbeef00001': {
            'PATCH': (
                {},
                {'contract': contract_101},
            )
        },
        '/v1/contract/ea0a4146-fd07-414b-aa5e-dedbeef00101': {
            'DELETE': (
                {},
                {},
            )
        },
        '/v1/contract/1': {
            'GET': (
                {},
                {'contract': {
                    'contract_id': '1',
                    'region_id': '1',
                    'project_id': '1',
                    'status': '1',
                    'project_name': '1',
                    'catalog_id': '1',
                    'catalog_name': '1',
                    'num': 1,
                    'application_id': '1',
                    'lifetime_start': '2015-07-10',
                    'lifetime_end': '2015-07-10',
                    'created_at': '2015-07-10',
                    'updated_at': '2015-07-10',
                    'deleted_at': '2015-07-10',
                    'deleted': False,
                    'expansions': {
                        'expansion_key1': '1',
                        'expansion_key2': '1',
                        'expansion_key3': '1',
                        'expansion_key4': '1',
                        'expansion_key5': '1',
                    },
                    'expansions_text': {
                        'expansion_text': '1',
                    }
                }}
            ),
        },
        '/v1/contract?project_id=project_id_102': {
            'GET': (
                {},
                {'contract': [contract_list_107,
                              contract_list_106,
                              contract_list_105]},
            ),
        },
        '/v1/contract?region_id=region_id_101': {
            'GET': (
                {},
                {'contract': [contract_list_104,
                              contract_list_103,
                              contract_list_102,
                              contract_list_101]},
            ),
        },
        '/v1/contract?project_name=roject_name_10': {
            'GET': (
                {},
                {'contract': [contract_list_107,
                              contract_list_106,
                              contract_list_105,
                              contract_list_104,
                              contract_list_103,
                              contract_list_102,
                              contract_list_101]},
            ),
        },
        '/v1/contract?catalog_name=atalog_name_10': {
            'GET': (
                {},
                {'contract': [contract_list_107,
                              contract_list_106,
                              contract_list_105,
                              contract_list_104,
                              contract_list_103,
                              contract_list_102,
                              contract_list_101]},
            ),
        },
        '/v1/contract?application_id=pplication_id_10': {
            'GET': (
                {},
                {'contract': [contract_list_107,
                              contract_list_106,
                              contract_list_105,
                              contract_list_104,
                              contract_list_103,
                              contract_list_102,
                              contract_list_101]},
            ),
        },
        '/v1/contract?ticket_template_name=ticket_template_name_102': {
            'GET': (
                {},
                {'contract': [contract_list_102]},
            ),
        },
        '/v1/contract?application_kinds_name=application_kinds_name_105': {
            'GET': (
                {},
                {'contract': [contract_list_105]},
            ),
        },
        '/v1/contract?application_name=application_name_103': {
            'GET': (
                {},
                {'contract': [contract_list_103]},
            ),
        },
        '/v1/contract?parent_contract_id=fd07-414b-aa5e-dedbeef00104': {
            'GET': (
                {},
                {'contract': [contract_list_104]},
            ),
        },
        '/v1/contract?application_date_from=2015-06-05': {
            'GET': (
                {},
                {'contract': [contract_list_108,
                              contract_list_107,
                              contract_list_106,
                              contract_list_105]},
            ),
        },
        '/v1/contract?application_date_to=2015-06-05': {
            'GET': (
                {},
                {'contract': [contract_list_105,
                              contract_list_104,
                              contract_list_103,
                              contract_list_102,
                              contract_list_101]},
            ),
        },
        '/v1/contract?lifetime_start_from=2015-07-06': {
            'GET': (
                {},
                {'contract': [contract_list_108,
                              contract_list_107,
                              contract_list_106]},
            ),
        },
        '/v1/contract?lifetime_start_to=2015-07-03': {
            'GET': (
                {},
                {'contract': [contract_list_103,
                              contract_list_102,
                              contract_list_101]},
            ),
        },
        '/v1/contract?lifetime_end_from=2015-08-07': {
            'GET': (
                {},
                {'contract': [contract_list_108,
                              contract_list_107]},
            ),
        },
        '/v1/contract?lifetime_end_to=2015-08-02': {
            'GET': (
                {},
                {'contract': [contract_list_102,
                              contract_list_101]},
            ),
        },
        '/v1/contract?lifetime=2015-08-05T23%3A59%3A59.000': {
            'GET': (
                {},
                {'contract': [contract_list_106,
                              contract_list_105,
                              contract_list_104]},
            ),
        },
        '/v1/contract?date_in_lifetime=2015-08-05': {
            'GET': (
                {},
                {'contract': [contract_list_107,
                              contract_list_106,
                              contract_list_105]},
            ),
        },
        '/v1/contract?limit=6': {
            'GET': (
                {},
                {'contract': [contract_list_107,
                              contract_list_106,
                              contract_list_105,
                              contract_list_104,
                              contract_list_103,
                              contract_list_102]},
            ),
        },
        '/v1/contract?marker=%s' % CONTRACT_ID_104: {
            'GET': (
                {},
                {'contract': [contract_list_103,
                              contract_list_102,
                              contract_list_101]},
            ),
        },
        '/v1/contract?sort_key=lifetime_start': {
            'GET': (
                {},
                {'contract': [contract_list_106,
                              contract_list_105,
                              contract_list_104,
                              contract_list_103,
                              contract_list_102,
                              contract_list_101,
                              contract_list_107]},
            ),
        },
        '/v1/contract?sort_dir=asc': {
            'GET': (
                {},
                {'contract': [contract_list_101,
                              contract_list_102,
                              contract_list_103,
                              contract_list_104,
                              contract_list_105,
                              contract_list_106,
                              contract_list_107]},
            ),
        },
        '/v1/contract?sort_dir=asc%2Cdesc'
        '&sort_key=project_name%2Ccatalog_name': {
            'GET': (
                {},
                {'contract': [contract_list_104,
                              contract_list_103,
                              contract_list_102,
                              contract_list_101,
                              contract_list_107,
                              contract_list_106,
                              contract_list_105]},
            ),
        },
        '/v1/contract?sort_dir=asc%2Cdesc&sort_key=catalog_name': {
            'GET': (
                {},
                {'contract': [contract_list_101,
                              contract_list_102,
                              contract_list_103,
                              contract_list_104,
                              contract_list_105,
                              contract_list_106,
                              contract_list_107]},
            ),
        },
        '/v1/contract?sort_dir=asc&sort_key=project_name%2Ccatalog_name': {
            'GET': (
                {},
                {'contract': [contract_list_104,
                              contract_list_103,
                              contract_list_102,
                              contract_list_101,
                              contract_list_107,
                              contract_list_106,
                              contract_list_105]},
            ),
        },
        '/v1/contract?force_show_deleted=true': {
            'GET': (
                {},
                {'contract': [contract_list_108,
                              contract_list_107,
                              contract_list_106,
                              contract_list_105,
                              contract_list_104,
                              contract_list_103,
                              contract_list_102,
                              contract_list_101]},
            ),
        },
        '/v1/contract?'
        'application_date_from=2015-06-01'
        '&application_date_to=2015-06-02&application_id=pplication_id_10'
        '&application_kinds_name=application_kinds_name_10'
        '&application_name=application_name_101'
        '&catalog_name=atalog_name_10&date_in_lifetime=2015-08-05'
        '&force_show_deleted=false&lifetime=2015-08-05T23%3A59%3A59.00'
        '&lifetime_end_from=2015-08-01&lifetime_end_to=2015-08-02'
        '&lifetime_start_from=2015-07-01&lifetime_start_to=2015-07-02'
        '&limit=1&marker=' + CONTRACT_ID_101 + '&'
        'parent_contract_id=ea0a4146-fd07-414b-aa5e-dedbeef00101'
        '&project_id=project_id_102'
        '&project_name=roject_name_10&region_id=region_id_102'
        '&sort_dir=asc%2Cdesc&sort_key=contract_name%2Clifetime_strat'
        '&ticket_template_name=ticket_template_name_101': {
            'GET': (
                {},
                {'contract': [contract_list_105]},
            ),
        },
        '/v1/contract?project_id=project_id_110': {
            'GET': (
                {},
                {'contract': []},
            ),
        },
    }


class ContractManagerTest(testtools.TestCase):
    """ContractManager test class."""

    def setUp(self):
        """Setup test class."""
        super(ContractManagerTest, self).setUp()
        self.api = utils.FakeAPI(fixtures)
        self.mgr = contracts.ContractManager(self.api)

    def test_create(self):
        """Test create method."""
        expectResponse = {'contract': contract_101}

        self.mgr.create(contract_101)
        expect = [('POST', '/v1/contract', {}, expectResponse.items())]
        self.assertEqual(expect, self.api.calls)

    def test_update(self):
        """Test update method."""
        expectResponse = {'contract': contract_101}

        self.mgr.update('ea0a4146-fd07-414b-aa5e-dedbeef00001',
                        contract_101)
        expect = [('PATCH',
                   '/v1/contract/ea0a4146-fd07-414b-aa5e-dedbeef00001',
                   {}, expectResponse.items())]
        self.assertEqual(expect, self.api.calls)

    def test_get(self):
        """Test get method."""
        self.mgr.get('1')
        expect = [('GET', '/v1/contract/1', {}, None)]

        self.assertEqual(expect, self.api.calls)

    def test_delete(self):
        """Test delete method."""
        self.mgr.delete('ea0a4146-fd07-414b-aa5e-dedbeef00101')
        expect = [('DELETE',
                   '/v1/contract/ea0a4146-fd07-414b-aa5e-dedbeef00101',
                   {}, None)]

        self.assertEqual(expect, self.api.calls)

    def test_list_no_params(self):
        """Test list api.
        Test with no params.
        """
        contracts = list(self.mgr.list())
        expect = [('GET', '/v1/contract', {}, None)]
        self.assertEqual(expect, self.api.calls)
        self.assertEqual(len(contracts), 7)
        self.assertEqual(contracts[0].contract_id, CONTRACT_ID_107)
        self.assertEqual(contracts[1].contract_id, CONTRACT_ID_106)
        self.assertEqual(contracts[2].contract_id, CONTRACT_ID_105)
        self.assertEqual(contracts[3].contract_id, CONTRACT_ID_104)
        self.assertEqual(contracts[4].contract_id, CONTRACT_ID_103)
        self.assertEqual(contracts[5].contract_id, CONTRACT_ID_102)
        self.assertEqual(contracts[6].contract_id, CONTRACT_ID_101)

    def test_list_with_project_id(self):
        """Test list api.
        Test with project id.
        """
        kwargs = {'project_id': 'project_id_102'}
        contracts = list(self.mgr.list(kwargs))
        url = '/v1/contract?' + parse.urlencode(kwargs)
        expect = [('GET', url, {}, None)]
        self.assertEqual(expect, self.api.calls)
        self.assertEqual(len(contracts), 3)
        self.assertEqual(contracts[0].contract_id, CONTRACT_ID_107)
        self.assertEqual(contracts[1].contract_id, CONTRACT_ID_106)
        self.assertEqual(contracts[2].contract_id, CONTRACT_ID_105)

    def test_list_with_region_id(self):
        """Test list api.
        Test with region id.
        """
        kwargs = {'region_id': 'region_id_101'}
        contracts = list(self.mgr.list(kwargs))
        url = '/v1/contract?' + parse.urlencode(kwargs)
        expect = [('GET', url, {}, None)]
        self.assertEqual(expect, self.api.calls)
        self.assertEqual(len(contracts), 4)
        self.assertEqual(contracts[0].contract_id, CONTRACT_ID_104)
        self.assertEqual(contracts[1].contract_id, CONTRACT_ID_103)
        self.assertEqual(contracts[2].contract_id, CONTRACT_ID_102)
        self.assertEqual(contracts[3].contract_id, CONTRACT_ID_101)

    def test_list_with_project_name(self):
        """Test list api.
        Test with project name.
        """
        kwargs = {'project_name': 'roject_name_10'}
        contracts = list(self.mgr.list(kwargs))
        url = '/v1/contract?' + parse.urlencode(kwargs)
        expect = [('GET', url, {}, None)]
        self.assertEqual(expect, self.api.calls)
        self.assertEqual(len(contracts), 7)
        self.assertEqual(contracts[0].contract_id, CONTRACT_ID_107)
        self.assertEqual(contracts[1].contract_id, CONTRACT_ID_106)
        self.assertEqual(contracts[2].contract_id, CONTRACT_ID_105)
        self.assertEqual(contracts[3].contract_id, CONTRACT_ID_104)
        self.assertEqual(contracts[4].contract_id, CONTRACT_ID_103)
        self.assertEqual(contracts[5].contract_id, CONTRACT_ID_102)
        self.assertEqual(contracts[6].contract_id, CONTRACT_ID_101)

    def test_list_with_catalog_name(self):
        """Test list api.
        Test with catalog name.
        """
        kwargs = {'catalog_name': 'atalog_name_10'}
        contracts = list(self.mgr.list(kwargs))
        url = '/v1/contract?' + parse.urlencode(kwargs)
        expect = [('GET', url, {}, None)]
        self.assertEqual(expect, self.api.calls)
        self.assertEqual(len(contracts), 7)
        self.assertEqual(contracts[0].contract_id, CONTRACT_ID_107)
        self.assertEqual(contracts[1].contract_id, CONTRACT_ID_106)
        self.assertEqual(contracts[2].contract_id, CONTRACT_ID_105)
        self.assertEqual(contracts[3].contract_id, CONTRACT_ID_104)
        self.assertEqual(contracts[4].contract_id, CONTRACT_ID_103)
        self.assertEqual(contracts[5].contract_id, CONTRACT_ID_102)
        self.assertEqual(contracts[6].contract_id, CONTRACT_ID_101)

    def test_list_with_application_id(self):
        """Test list api.
        Test with application id.
        """
        kwargs = {'application_id': 'pplication_id_10'}
        contracts = list(self.mgr.list(kwargs))
        url = '/v1/contract?' + parse.urlencode(kwargs)
        expect = [('GET', url, {}, None)]
        self.assertEqual(expect, self.api.calls)
        self.assertEqual(len(contracts), 7)
        self.assertEqual(contracts[0].contract_id, CONTRACT_ID_107)
        self.assertEqual(contracts[1].contract_id, CONTRACT_ID_106)
        self.assertEqual(contracts[2].contract_id, CONTRACT_ID_105)
        self.assertEqual(contracts[3].contract_id, CONTRACT_ID_104)
        self.assertEqual(contracts[4].contract_id, CONTRACT_ID_103)
        self.assertEqual(contracts[5].contract_id, CONTRACT_ID_102)
        self.assertEqual(contracts[6].contract_id, CONTRACT_ID_101)

    def test_list_with_lifetime(self):
        """Test list api.
        Test with lifetime.
        """
        kwargs = {'lifetime': '2015-08-05T23:59:59.000'}
        contracts = list(self.mgr.list(kwargs))
        url = '/v1/contract?' + parse.urlencode(kwargs)
        expect = [('GET', url, {}, None)]
        self.assertEqual(expect, self.api.calls)
        self.assertEqual(len(contracts), 3)
        self.assertEqual(contracts[0].contract_id, CONTRACT_ID_106)
        self.assertEqual(contracts[1].contract_id, CONTRACT_ID_105)
        self.assertEqual(contracts[2].contract_id, CONTRACT_ID_104)

    def test_list_with_date_in_lifetime(self):
        """Test list api.
        Test with date_in_lifetime.
        """
        kwargs = {'date_in_lifetime': '2015-08-05'}
        contracts = list(self.mgr.list(kwargs))
        url = '/v1/contract?' + parse.urlencode(kwargs)
        expect = [('GET', url, {}, None)]
        self.assertEqual(expect, self.api.calls)
        self.assertEqual(len(contracts), 3)
        self.assertEqual(contracts[0].contract_id, CONTRACT_ID_107)
        self.assertEqual(contracts[1].contract_id, CONTRACT_ID_106)
        self.assertEqual(contracts[2].contract_id, CONTRACT_ID_105)

    def test_list_with_ticket_template_name(self):
        """Test list api.
        Test with ticket_template_name.
        """
        kwargs = {'ticket_template_name': 'ticket_template_name_102'}
        contracts = list(self.mgr.list(kwargs))
        url = '/v1/contract?' + parse.urlencode(kwargs)
        expect = [('GET', url, {}, None)]
        self.assertEqual(expect, self.api.calls)
        self.assertEqual(len(contracts), 1)
        self.assertEqual(contracts[0].contract_id, CONTRACT_ID_102)

    def test_list_with_application_kinds_name(self):
        """Test list api.
        Test with ticket_template_name.
        """
        kwargs = {'application_kinds_name': 'application_kinds_name_105'}
        contracts = list(self.mgr.list(kwargs))
        url = '/v1/contract?' + parse.urlencode(kwargs)
        expect = [('GET', url, {}, None)]
        self.assertEqual(expect, self.api.calls)
        self.assertEqual(len(contracts), 1)
        self.assertEqual(contracts[0].contract_id, CONTRACT_ID_105)

    def test_list_with_application_name(self):
        """Test list api.
        Test with application_name.
        """
        kwargs = {'application_name': 'application_name_103'}
        contracts = list(self.mgr.list(kwargs))
        url = '/v1/contract?' + parse.urlencode(kwargs)
        expect = [('GET', url, {}, None)]
        self.assertEqual(expect, self.api.calls)
        self.assertEqual(len(contracts), 1)
        self.assertEqual(contracts[0].contract_id, CONTRACT_ID_103)

    def test_list_with_parent_contract_id(self):
        """Test list api.
        Test with contract_id.
        """
        kwargs = {'parent_contract_id': 'fd07-414b-aa5e-dedbeef00104'}
        contracts = list(self.mgr.list(kwargs))
        url = '/v1/contract?' + parse.urlencode(kwargs)
        expect = [('GET', url, {}, None)]
        self.assertEqual(expect, self.api.calls)
        self.assertEqual(len(contracts), 1)
        self.assertEqual(contracts[0].contract_id, CONTRACT_ID_104)

    def test_list_with_application_date_from(self):
        """Test list api.
        Test with application_date_from.
        """
        kwargs = {'application_date_from': '2015-06-05'}
        contracts = list(self.mgr.list(kwargs))
        url = '/v1/contract?' + parse.urlencode(kwargs)
        expect = [('GET', url, {}, None)]
        self.assertEqual(expect, self.api.calls)
        self.assertEqual(len(contracts), 4)
        self.assertEqual(contracts[0].contract_id, CONTRACT_ID_108)
        self.assertEqual(contracts[1].contract_id, CONTRACT_ID_107)
        self.assertEqual(contracts[2].contract_id, CONTRACT_ID_106)
        self.assertEqual(contracts[3].contract_id, CONTRACT_ID_105)

    def test_list_with_application_date_to(self):
        """Test list api.
        Test with application_date_to.
        """
        kwargs = {'application_date_to': '2015-06-05'}
        contracts = list(self.mgr.list(kwargs))
        url = '/v1/contract?' + parse.urlencode(kwargs)
        expect = [('GET', url, {}, None)]
        self.assertEqual(expect, self.api.calls)
        self.assertEqual(len(contracts), 5)
        self.assertEqual(contracts[0].contract_id, CONTRACT_ID_105)
        self.assertEqual(contracts[1].contract_id, CONTRACT_ID_104)
        self.assertEqual(contracts[2].contract_id, CONTRACT_ID_103)
        self.assertEqual(contracts[3].contract_id, CONTRACT_ID_102)
        self.assertEqual(contracts[4].contract_id, CONTRACT_ID_101)

    def test_list_with_lifetime_start_from(self):
        """Test list api.
        Test with lifetime_start_from.
        """
        kwargs = {'lifetime_start_from': '2015-07-06'}
        contracts = list(self.mgr.list(kwargs))
        url = '/v1/contract?' + parse.urlencode(kwargs)
        expect = [('GET', url, {}, None)]
        self.assertEqual(expect, self.api.calls)
        self.assertEqual(len(contracts), 3)
        self.assertEqual(contracts[0].contract_id, CONTRACT_ID_108)
        self.assertEqual(contracts[1].contract_id, CONTRACT_ID_107)
        self.assertEqual(contracts[2].contract_id, CONTRACT_ID_106)

    def test_list_with_lifetime_start_to(self):
        """Test list api.
        Test with lifetime_start_to.
        """
        kwargs = {'lifetime_start_to': '2015-07-03'}
        contracts = list(self.mgr.list(kwargs))
        url = '/v1/contract?' + parse.urlencode(kwargs)
        expect = [('GET', url, {}, None)]
        self.assertEqual(expect, self.api.calls)
        self.assertEqual(len(contracts), 3)
        self.assertEqual(contracts[0].contract_id, CONTRACT_ID_103)
        self.assertEqual(contracts[1].contract_id, CONTRACT_ID_102)
        self.assertEqual(contracts[2].contract_id, CONTRACT_ID_101)

    def test_list_with_lifetime_end_from(self):
        """Test list api.
        Test with lifetime_end_from.
        """
        kwargs = {'lifetime_end_from': '2015-08-07'}
        contracts = list(self.mgr.list(kwargs))
        url = '/v1/contract?' + parse.urlencode(kwargs)
        expect = [('GET', url, {}, None)]
        self.assertEqual(expect, self.api.calls)
        self.assertEqual(len(contracts), 2)
        self.assertEqual(contracts[0].contract_id, CONTRACT_ID_108)
        self.assertEqual(contracts[1].contract_id, CONTRACT_ID_107)

    def test_list_with_lifetime_end_to(self):
        """Test list api.
        Test with lifetime_end_to.
        """
        kwargs = {'lifetime_end_to': '2015-08-02'}
        contracts = list(self.mgr.list(kwargs))
        url = '/v1/contract?' + parse.urlencode(kwargs)
        expect = [('GET', url, {}, None)]
        self.assertEqual(expect, self.api.calls)
        self.assertEqual(len(contracts), 2)
        self.assertEqual(contracts[0].contract_id, CONTRACT_ID_102)
        self.assertEqual(contracts[1].contract_id, CONTRACT_ID_101)

    def test_list_with_limit(self):
        """Test list api.
        Test with limit.
        """
        kwargs = {'limit': 6}
        contracts = list(self.mgr.list(kwargs))
        url = '/v1/contract?' + parse.urlencode(kwargs)
        expect = [('GET', url, {}, None)]
        self.assertEqual(expect, self.api.calls)
        self.assertEqual(len(contracts), 6)
        self.assertEqual(contracts[0].contract_id, CONTRACT_ID_107)
        self.assertEqual(contracts[1].contract_id, CONTRACT_ID_106)
        self.assertEqual(contracts[2].contract_id, CONTRACT_ID_105)
        self.assertEqual(contracts[3].contract_id, CONTRACT_ID_104)
        self.assertEqual(contracts[4].contract_id, CONTRACT_ID_103)
        self.assertEqual(contracts[5].contract_id, CONTRACT_ID_102)

    def test_list_with_marker(self):
        """Test list api.
        Test with marker.
        """
        kwargs = {'marker': CONTRACT_ID_104}
        contracts = list(self.mgr.list(kwargs))
        url = '/v1/contract?' + parse.urlencode(kwargs)
        expect = [('GET', url, {}, None)]
        self.assertEqual(expect, self.api.calls)
        self.assertEqual(len(contracts), 3)
        self.assertEqual(contracts[0].contract_id, CONTRACT_ID_103)
        self.assertEqual(contracts[1].contract_id, CONTRACT_ID_102)
        self.assertEqual(contracts[2].contract_id, CONTRACT_ID_101)

    def test_list_with_sort_key(self):
        """Test list api.
        Test with sort key.
        """
        kwargs = {'sort_key': 'lifetime_start'}
        contracts = list(self.mgr.list(kwargs))
        url = '/v1/contract?' + parse.urlencode(kwargs)
        expect = [('GET', url, {}, None)]
        self.assertEqual(expect, self.api.calls)
        self.assertEqual(len(contracts), 7)
        self.assertEqual(contracts[0].contract_id, CONTRACT_ID_106)
        self.assertEqual(contracts[1].contract_id, CONTRACT_ID_105)
        self.assertEqual(contracts[2].contract_id, CONTRACT_ID_104)
        self.assertEqual(contracts[3].contract_id, CONTRACT_ID_103)
        self.assertEqual(contracts[4].contract_id, CONTRACT_ID_102)
        self.assertEqual(contracts[5].contract_id, CONTRACT_ID_101)
        self.assertEqual(contracts[6].contract_id, CONTRACT_ID_107)

    def test_list_with_sort_dir(self):
        """Test list api.
        Test with sort dir.
        """
        kwargs = {'sort_dir': 'asc'}
        contracts = list(self.mgr.list(kwargs))
        url = '/v1/contract?' + parse.urlencode(kwargs)
        expect = [('GET', url, {}, None)]
        self.assertEqual(expect, self.api.calls)
        self.assertEqual(len(contracts), 7)
        self.assertEqual(contracts[0].contract_id, CONTRACT_ID_101)
        self.assertEqual(contracts[1].contract_id, CONTRACT_ID_102)
        self.assertEqual(contracts[2].contract_id, CONTRACT_ID_103)
        self.assertEqual(contracts[3].contract_id, CONTRACT_ID_104)
        self.assertEqual(contracts[4].contract_id, CONTRACT_ID_105)
        self.assertEqual(contracts[5].contract_id, CONTRACT_ID_106)
        self.assertEqual(contracts[6].contract_id, CONTRACT_ID_107)

    def test_list_with_sort_key_dir(self):
        """Test list api.
        Test with sort key and sort dir.
        """
        kwargs = {'sort_dir': 'asc,desc',
                  'sort_key': 'project_name,catalog_name'}
        contracts = list(self.mgr.list(kwargs))
        url = '/v1/contract?' + parse.urlencode(kwargs)
        expect = [('GET', url, {}, None)]
        self.assertEqual(expect, self.api.calls)
        self.assertEqual(len(contracts), 7)
        self.assertEqual(contracts[0].contract_id, CONTRACT_ID_104)
        self.assertEqual(contracts[1].contract_id, CONTRACT_ID_103)
        self.assertEqual(contracts[2].contract_id, CONTRACT_ID_102)
        self.assertEqual(contracts[3].contract_id, CONTRACT_ID_101)
        self.assertEqual(contracts[4].contract_id, CONTRACT_ID_107)
        self.assertEqual(contracts[5].contract_id, CONTRACT_ID_106)
        self.assertEqual(contracts[6].contract_id, CONTRACT_ID_105)

    def test_list_with_sort_key_less_than_sort_dir(self):
        """Test list api.
        Test with sort key and sort dir, where key is less than dir.
        """
        kwargs = {'sort_dir': 'asc,desc',
                  'sort_key': 'catalog_name'}

        contracts = list(self.mgr.list(kwargs))
        url = '/v1/contract?' + parse.urlencode(kwargs)
        expect = [('GET', url, {}, None)]
        self.assertEqual(expect, self.api.calls)
        self.assertEqual(len(contracts), 7)
        self.assertEqual(contracts[0].contract_id, CONTRACT_ID_101)
        self.assertEqual(contracts[1].contract_id, CONTRACT_ID_102)
        self.assertEqual(contracts[2].contract_id, CONTRACT_ID_103)
        self.assertEqual(contracts[3].contract_id, CONTRACT_ID_104)
        self.assertEqual(contracts[4].contract_id, CONTRACT_ID_105)
        self.assertEqual(contracts[5].contract_id, CONTRACT_ID_106)
        self.assertEqual(contracts[6].contract_id, CONTRACT_ID_107)

    def test_list_with_sort_key_more_than_sort_dir(self):
        """Test list api.
        Test with sort key and sort dir, where key is more than dir.
        """
        kwargs = {'sort_dir': 'asc',
                  'sort_key': 'project_name,catalog_name'}
        contracts = list(self.mgr.list(kwargs))
        url = '/v1/contract?' + parse.urlencode(kwargs)
        expect = [('GET', url, {}, None)]
        self.assertEqual(expect, self.api.calls)
        self.assertEqual(len(contracts), 7)
        self.assertEqual(contracts[0].contract_id, CONTRACT_ID_104)
        self.assertEqual(contracts[1].contract_id, CONTRACT_ID_103)
        self.assertEqual(contracts[2].contract_id, CONTRACT_ID_102)
        self.assertEqual(contracts[3].contract_id, CONTRACT_ID_101)
        self.assertEqual(contracts[4].contract_id, CONTRACT_ID_107)
        self.assertEqual(contracts[5].contract_id, CONTRACT_ID_106)
        self.assertEqual(contracts[6].contract_id, CONTRACT_ID_105)

    def test_list_with_deleted(self):
        """Test list api.
        Test with deleted.
        """
        kwargs = {'force_show_deleted': 'true'}
        contracts = list(self.mgr.list(kwargs))
        url = '/v1/contract?' + parse.urlencode(kwargs)
        expect = [('GET', url, {}, None)]
        self.assertEqual(expect, self.api.calls)
        self.assertEqual(len(contracts), 8)
        self.assertEqual(contracts[0].contract_id, CONTRACT_ID_108)
        self.assertEqual(contracts[1].contract_id, CONTRACT_ID_107)
        self.assertEqual(contracts[2].contract_id, CONTRACT_ID_106)
        self.assertEqual(contracts[3].contract_id, CONTRACT_ID_105)
        self.assertEqual(contracts[4].contract_id, CONTRACT_ID_104)
        self.assertEqual(contracts[5].contract_id, CONTRACT_ID_103)
        self.assertEqual(contracts[6].contract_id, CONTRACT_ID_102)
        self.assertEqual(contracts[7].contract_id, CONTRACT_ID_101)

    def test_list_with_all_params(self):
        """Test list api.
        Test with all parameters.
        """
        kwargs = {'application_id': 'pplication_id_10',
                  'catalog_name': 'atalog_name_10',
                  'force_show_deleted': 'false',
                  'lifetime': '2015-08-05T23:59:59.00',
                  'date_in_lifetime': '2015-08-05',
                  'ticket_template_name': 'ticket_template_name_101',
                  'application_kinds_name': 'application_kinds_name_10',
                  'application_name': 'application_name_101',
                  'parent_contract_id': 'ea0a4146-fd07-414b-aa5e-dedbeef00101',
                  'application_date_from': '2015-06-01',
                  'application_date_to': '2015-06-02',
                  'lifetime_start_from': '2015-07-01',
                  'lifetime_start_to': '2015-07-02',
                  'lifetime_end_from': '2015-08-01',
                  'lifetime_end_to': '2015-08-02',
                  'limit': 1,
                  'marker': CONTRACT_ID_101,
                  'project_id': 'project_id_102',
                  'project_name': 'roject_name_10',
                  'region_id': 'region_id_102',
                  'sort_dir': 'asc,desc',
                  'sort_key': 'contract_name,lifetime_strat'}
        contracts = list(self.mgr.list(kwargs))
        url = '/v1/contract?' \
              'application_date_from=2015-06-01' \
              '&application_date_to=2015-06-02' \
              '&application_id=pplication_id_10' \
              '&application_kinds_name=application_kinds_name_10' \
              '&application_name=application_name_101' \
              '&catalog_name=atalog_name_10&date_in_lifetime=2015-08-05' \
              '&force_show_deleted=false&lifetime=2015-08-05T23%3A59%3A59.00' \
              '&lifetime_end_from=2015-08-01&lifetime_end_to=2015-08-02' \
              '&lifetime_start_from=2015-07-01&lifetime_start_to=2015-07-02' \
              '&limit=1&marker=' + CONTRACT_ID_101 + \
              '&parent_contract_id=ea0a4146-fd07-414b-aa5e-dedbeef00101' \
              '&project_id=project_id_102' \
              '&project_name=roject_name_10&region_id=region_id_102' \
              '&sort_dir=asc%2Cdesc&sort_key=contract_name%2Clifetime_strat' \
              '&ticket_template_name=ticket_template_name_101'
        expect = [('GET', url, {}, None)]
        self.assertEqual(expect, self.api.calls)
        self.assertEqual(len(contracts), 1)
        self.assertEqual(contracts[0].contract_id, CONTRACT_ID_105)

    def test_list_no_result(self):
        """Test list api.
        Test if the retrieved result is of 0.
        """
        kwargs = {'project_id': 'project_id_110'}
        contracts = list(self.mgr.list(kwargs))
        url = '/v1/contract?' + parse.urlencode(kwargs)
        expect = [('GET', url, {}, None)]
        self.assertEqual(expect, self.api.calls)
        self.assertEqual(len(contracts), 0)
