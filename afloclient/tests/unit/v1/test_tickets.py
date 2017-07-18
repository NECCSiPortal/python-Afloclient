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

"""Test afloclient/v1/ticket.py."""
import copy
import testtools

from afloclient.tests.unit import utils
from afloclient.v1 import tickets
from six.moves.urllib import parse

fixtures_ticket_data_detail = \
    {
        'ticket': {
            'id': '1',
            'ticket_template_id': '1',
            'ticket_type': '1',
            'target_id': '1',
            'tenant_id': '1',
            'owner_id': '1',
            'owner_at': '1',
            'ticket_detail': '1',
            'action_detail': '1',
            'created_at': '2015-07-01',
            'updated_at': '2015-07-01',
            'deleted_at': '2015-07-01',
            'deleted': False,
            'workflow': [{
                'id': '10',
                'ticket_id': '10',
                'status': '10',
                'status_code': '10',
                'status_detail': '10',
                'target_role': '10',
                'confirmer_id': '10',
                'confirmed_at': '2015-07-10',
                'additional_data': '10',
                'created_at': '2015-07-10',
                'updated_at': '2015-07-10',
                'deleted_at': '2015-07-10',
                'deleted': False
            }]
        }
    }
fixtures_ticket_data_row1 = \
    {
        'id': '1',
        'ticket_template_id': '1',
        'ticket_type': '1',
        'target_id': '1',
        'tenant_id': '1',
        'owner_id': '1',
        'owner_at': '1',
        'ticket_detail': '1',
        'action_detail': '1',
        'created_at': '2015-07-01',
        'updated_at': '2015-07-01',
        'deleted_at': '2015-07-01',
        'deleted': False,
        'last_workflow': {
            'id': '10',
            'ticket_id': '10',
            'status': '10',
            'status_code': '10',
            'status_detail': '10',
            'target_role': '10',
            'confirmer_id': '10',
            'confirmed_at': '2015-07-10',
            'additional_data': '10',
            'created_at': '2015-07-10',
            'updated_at': '2015-07-10',
            'deleted_at': '2015-07-10',
            'deleted': False
        }
    }
fixtures_ticket_data_row2 = \
    {
        'ticket': {
            'id': '2',
            'ticket_template_id': '2',
            'ticket_type': '2',
            'target_id': '2',
            'tenant_id': '2',
            'owner_id': '2',
            'owner_at': '2',
            'ticket_detail': '2',
            'action_detail': '2',
            'created_at': '2015-07-02',
            'updated_at': '2015-07-02',
            'deleted_at': '2015-07-02',
            'deleted': False,
            'last_workflow': {
                'id': '11',
                'ticket_id': '11',
                'status': '11',
                'status_code': '11',
                'status_detail': '11',
                'target_role': '11',
                'confirmer_id': '11',
                'confirmed_at': '2015-07-11',
                'additional_data': '11',
                'created_at': '2015-07-11',
                'updated_at': '2015-07-11',
                'deleted_at': '2015-07-11',
                'deleted': False
            }
        }
    }

# from afloclient.v1 import client
#  request fixtures
#    (request url, request header, request parameter).
fixtures = \
    {
        '/v1/tickets/1': {
            'GET': (
                {},
                fixtures_ticket_data_detail,
            ),
            'PUT': (
                {},
                {'ticket': {
                    'last_workflow_id': '1',
                    'next_workflow_id': '1',
                    'status_code': '1',
                    'additional_data': '{"json": "1"}'
                }},
            ),
            'DELETE': (
                {},
                None
            ),
        },
        '/v1/tickets': {
            'GET': (
                {},
                {'tickets': [fixtures_ticket_data_row1,
                             fixtures_ticket_data_row2]},
            ),
            'POST': (
                {},
                {'ticket': {
                    'id': '1',
                    'text': 'aflo-1'
                }},
            ),
        },
        # filter parameter start
        '/v1/tickets?id=1': {
            'GET': (
                {},
                {'tickets': [fixtures_ticket_data_row1,
                             fixtures_ticket_data_row2]},
            ),
        },
        '/v1/tickets?tenant_id=1': {
            'GET': (
                {},
                {'tickets': [fixtures_ticket_data_row1,
                             fixtures_ticket_data_row2]},
            ),
        },
        '/v1/tickets?last_status_code=1': {
            'GET': (
                {},
                {'tickets': [fixtures_ticket_data_row1,
                             fixtures_ticket_data_row2]},
            ),
        },
        '/v1/tickets?ticket_template_id=1': {
            'GET': (
                {},
                {'tickets': [fixtures_ticket_data_row1,
                             fixtures_ticket_data_row2]},
            ),
        },
        '/v1/tickets?ticket_type=1': {
            'GET': (
                {},
                {'tickets': [fixtures_ticket_data_row1,
                             fixtures_ticket_data_row2]},
            ),
        },
        '/v1/tickets?ticket_type=1&ticket_type=2': {
            'GET': (
                {},
                {'tickets': [fixtures_ticket_data_row1,
                             fixtures_ticket_data_row2]},
            ),
        },
        '/v1/tickets?target_id=1': {
            'GET': (
                {},
                {'tickets': [fixtures_ticket_data_row1,
                             fixtures_ticket_data_row2]},
            ),
        },
        '/v1/tickets?owner_id=1': {
            'GET': (
                {},
                {'tickets': [fixtures_ticket_data_row1,
                             fixtures_ticket_data_row2]},
            ),
        },
        '/v1/tickets?owner_at=1': {
            'GET': (
                {},
                {'tickets': [fixtures_ticket_data_row1,
                             fixtures_ticket_data_row2]},
            ),
        },
        '/v1/tickets?last_confirmer_id=1': {
            'GET': (
                {},
                {'tickets': [fixtures_ticket_data_row1,
                             fixtures_ticket_data_row2]},
            ),
        },
        '/v1/tickets?last_confirmed_at=2015-07-01': {
            'GET': (
                {},
                {'tickets': [fixtures_ticket_data_row1,
                             fixtures_ticket_data_row2]},
            ),
        },
        '/v1/tickets?tenant_id=1': {
            'GET': (
                {},
                {'tickets': [fixtures_ticket_data_row1,
                             fixtures_ticket_data_row2]},
            ),
        },
        # filter parameter end
        '/v1/tickets?limit=1': {
            'GET': (
                {},
                {'tickets': [fixtures_ticket_data_row1,
                             fixtures_ticket_data_row2]},
            ),
        },
        '/v1/tickets?marker=a': {
            'GET': (
                {},
                {'tickets': [fixtures_ticket_data_row1,
                             fixtures_ticket_data_row2]},
            ),
        },
        '/v1/tickets?sort_dir=desc': {
            'GET': (
                {},
                {'tickets': [fixtures_ticket_data_row1,
                             fixtures_ticket_data_row2]},
            ),
        },
        '/v1/tickets?sort_key=tenant_id': {
            'GET': (
                {},
                {'tickets': [fixtures_ticket_data_row1,
                             fixtures_ticket_data_row2]},
            ),
        },
        '/v1/tickets?sort_dir=desc&sort_key=tenant_id': {
            'GET': (
                {},
                {'tickets': [fixtures_ticket_data_row1,
                             fixtures_ticket_data_row2]},
            ),
        },
        '/v1/tickets?sort_key=text&sort_dir=desc': {
            'GET': (
                {},
                {'tickets': [fixtures_ticket_data_row1,
                             fixtures_ticket_data_row2]},
            ),
        },
        '/v1/tickets?force_show_deleted=True': {
            'GET': (
                {},
                {'tickets': []},
            ),
        },
        '/v1/tickets?enable_expansion_filters=False': {
            'GET': (
                {},
                {'tickets': []},
            ),
        },
        '/v1/tickets?ticket_template_name=a': {
            'GET': (
                {},
                {'tickets': []},
            ),
        },
        '/v1/tickets?application_kinds_name=a': {
            'GET': (
                {},
                {'tickets': []},
            ),
        },
        '/v1/tickets?application_kinds_name=a&'
        'ticket_template_name=b': {
            'GET': (
                {},
                {'tickets': []},
            ),
        },
    }


class TicketManagerTest(testtools.TestCase):
    """TicketManager Test class."""

    def setUp(self):
        """Setup test class."""
        super(TicketManagerTest, self).setUp()
        self.api = utils.FakeAPI(fixtures)
        self.mgr = tickets.TicketManager(self.api)

    def test_get(self):
        """Test get method."""
        ticket = self.mgr.get('1')
        expect = [('GET', '/v1/tickets/1', {}, None)]

        self.assertEqual(expect, self.api.calls)
        self.assertEqual('1', ticket.id)
        self.assertEqual('1', ticket.tenant_id)
        self.assertEqual('10', ticket.workflow[0]['id'])

    def test_list(self):
        """Test list method."""
        tickets = list(self.mgr.list())
        expect = [('GET', '/v1/tickets', {}, None)]
        self.assertEqual(expect, self.api.calls)
        self.assertEqual(2, len(tickets))
        self.assertEqual('1', tickets[0].id)

    def test_list_filter(self):
        """Test list method by add filter options."""
        filter = [{'tenant_id': '1'},
                  {'last_status_code': '1'},
                  {'ticket_template_id': '1'},
                  {'ticket_type': '1'},
                  {'target_id': '1'},
                  {'owner_id': '1'},
                  {'owner_at': '1'},
                  {'last_confirmer_id': '1'},
                  {'last_confirmed_at': '2015-07-01'},
                  {"force_show_deleted": True},
                  {"enable_expansion_filters": False},
                  {"ticket_template_name": 'a'},
                  {"application_kinds_name": 'a'}, ]
        expect = []

        for kwargs in filter:
            call_kwargs = copy.deepcopy(kwargs)
            list(self.mgr.list(kwargs))
            expect.append(('GET', '/v1/tickets?' +
                           parse.urlencode(call_kwargs),
                           {}, None))
            self.assertEqual(expect, self.api.calls)

    def test_list_limit(self):
        """Test list method by add limit option."""
        kwargs = {'limit': 1}
        list(self.mgr.list(kwargs))
        expect = [('GET', '/v1/tickets?' + parse.urlencode(kwargs),
                   {}, None)]

        self.assertEqual(expect, self.api.calls)

    def test_list_marker(self):
        """Test list method by add marker option."""
        kwargs = {'marker': 'a'}
        list(self.mgr.list(kwargs))
        expect = [('GET', '/v1/tickets?' + parse.urlencode(kwargs),
                   {}, None)]

        self.assertEqual(expect, self.api.calls)

    def test_list_sort_dir(self):
        """Test list method by add sort-dir option."""
        kwargs = {'sort_dir': 'desc'}
        list(self.mgr.list(kwargs))
        expect = [('GET', '/v1/tickets?' + parse.urlencode(kwargs),
                   {}, None)]

        self.assertEqual(expect, self.api.calls)

    def test_list_sort_key(self):
        """Test list method by add sort-key option."""
        kwargs = {'sort_key': 'tenant_id'}
        list(self.mgr.list(kwargs))
        expect = [('GET', '/v1/tickets?' + parse.urlencode(kwargs),
                   {}, None)]

        self.assertEqual(expect, self.api.calls)

    def test_list_sort(self):
        """Test list method by add sort-key and sort-dir options."""
        kwargs = {'sort_dir': 'desc', 'sort_key': 'tenant_id'}
        list(self.mgr.list(kwargs))
        expect = [('GET', '/v1/tickets?' + parse.urlencode(kwargs),
                   {}, None)]

        self.assertEqual(expect, self.api.calls)

    def test_list_ticket_template_contents(self):
        """Test 'List method'
        Test of if you specify multiple value
        of ticket template contents.
        """
        kwargs = {'application_kinds_name': 'a',
                  'ticket_template_name': 'b'}
        list(self.mgr.list(kwargs))
        expect = [('GET', '/v1/tickets?application_kinds_name=a&'
                   'ticket_template_name=b',
                   {}, None)]

        self.assertEqual(expect, self.api.calls)

    def test_list_multi_ticket_type(self):
        """Test list method by multi ticket_type filter options."""
        filter = {'ticket_type': ['1', '2']}

        list(self.mgr.list(filter))
        expect = [('GET', '/v1/tickets?ticket_type=1&ticket_type=2',
                   {}, None)]
        self.assertEqual(expect, self.api.calls)

    def test_list_deleted(self):
        """Test list method by add force-show-deleted options."""
        kwargs = {'force_show_deleted': True}
        list(self.mgr.list(kwargs))
        expect = [('GET', '/v1/tickets?' + parse.urlencode(kwargs),
                   {}, None)]

        self.assertEqual(expect, self.api.calls)

    def test_delete(self):
        """Test delete method."""
        self.mgr.delete('1')
        expect = [('DELETE', '/v1/tickets/1', {}, None)]

        self.assertEqual(expect, self.api.calls)

    def test_create(self):
        """Test create method."""
        kwargs = {
            'ticket_template_id': '1',
            'ticket_detail': '{}',
            'status_code': 'status_code'
        }
        expectResponse = {
            'ticket': kwargs
        }

        self.mgr.create(kwargs)
        expect = [('POST', '/v1/tickets', {}, expectResponse.items())]

        self.assertEqual(expect, self.api.calls)

    def test_update(self):
        """Test update method."""
        kwargs = {
            'last_workflow_id': '1',
            'next_workflow_id': '1',
            'status_code': '1',
            'additional_data': '{"json": "1"}'
        }
        expectResponse = {
            'ticket': {
                'last_workflow_id': '1',
                'next_workflow_id': '1',
                'status_code': '1',
                'additional_data': '{"json": "1"}'
            }
        }
        self.mgr.update('1', kwargs)
        expect = [('PUT', '/v1/tickets/1', {}, expectResponse.items())]

        self.assertEqual(expect, self.api.calls)
