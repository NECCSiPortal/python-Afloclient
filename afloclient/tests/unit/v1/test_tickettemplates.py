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

"""Test afloclient/v1/tickettemplates.py."""

import codecs
import json
import os
import testtools

from afloclient.common import utils as common_utils
from afloclient.tests.unit import utils
from afloclient.v1 import tickettemplates

FILES_DIR = 'afloclient/tests/unit/v1/operation_definition_files/'


# from afloclient.v1 import client
#  request fixtures
#    (request url, request header, request parameter).
fixtures = {
    '/v1/tickettemplates/1': {
        'GET': (
            {},
            {'tickettemplate': {
                'id': '1',
                'ticket_type': 'request',
                'template_contents': 'template',
                'workflow_pattern_id': 'workflow',
                'created_at': '2015-07-01',
                'updated_at': '2015-07-01',
                'deleted_at': '2015-07-01',
                'deleted': True
            }},
        ),
        'DELETE': (
            {},
            None,
        )
    },
    '/v1/tickettemplates/2': {
        'GET': (
            {},
            {'tickettemplate': {
                'id': '2',
                'ticket_type': 'request',
                'template_contents': u"ni\xf1o",
                'workflow_pattern_id': 'workflow',
                'created_at': '2015-07-01',
                'updated_at': '2015-07-01',
                'deleted_at': '2015-07-01',
                'deleted': True
            }},
        ),
    },
    '/v1/tickettemplates': {
        'GET': (
            {},
            {'tickettemplates': [
                {
                    'id': '1',
                    'ticket_type': 'request',
                    'template_contents': 'template',
                    'workflow_pattern_id': 'workflow',
                    'created_at': '2015-07-01',
                    'updated_at': '2015-07-01',
                    'deleted_at': '2015-07-01',
                    'deleted': True
                },
                {
                    'id': '2',
                    'ticket_type': 'request',
                    'template_contents': 'template',
                    'workflow_pattern_id': 'workflow',
                    'created_at': '2015-07-01',
                    'updated_at': '2015-07-01',
                    'deleted_at': '2015-07-01',
                    'deleted': True
                }
            ]},
        ),
        'POST': (
            {},
            {'tickettemplate': {
                'id': '1',
                'ticket_type': 'request',
                'template_contents': 'template',
                'workflow_pattern_id': 'workflow',
                'created_at': '2015-07-01',
                'updated_at': '2015-07-01',
                'deleted_at': '2015-07-01',
                'deleted': True
            }},
        ),
    },
    '/v1/tickettemplates?name=aflo-1': {
        'GET': (
            {},
            {'tickettemplates': [
                {
                    'id': '1',
                    'ticket_type': 'request',
                    'template_contents': 'template',
                    'workflow_pattern_id': 'workflow',
                    'created_at': '2015-07-01',
                    'updated_at': '2015-07-01',
                    'deleted_at': '2015-07-01',
                    'deleted': True
                },
            ]},
        ),
    },
    '/v1/tickettemplates?limit=1': {
        'GET': (
            {},
            {'tickettemplates': [
                {
                    'id': '1',
                    'ticket_type': 'request',
                    'template_contents': 'template',
                    'workflow_pattern_id': 'workflow',
                    'created_at': '2015-07-01',
                    'updated_at': '2015-07-01',
                    'deleted_at': '2015-07-01',
                    'deleted': True
                },
            ]},
        ),
    },
    '/v1/tickettemplates?marker=a': {
        'GET': (
            {},
            {'tickettemplates': [
                {
                    'id': '1',
                    'ticket_type': 'request',
                    'template_contents': 'template',
                    'workflow_pattern_id': 'workflow',
                    'created_at': '2015-07-01',
                    'updated_at': '2015-07-01',
                    'deleted_at': '2015-07-01',
                    'deleted': True
                },
            ]},
        ),
    },
    '/v1/tickettemplates?marker=nodata': {
        'GET': (
            {},
            {'tickettemplates': []},
        ),
    },
    '/v1/tickettemplates?sort_dir=desc&sort_key=id': {
        'GET': (
            {},
            {'tickettemplates': [
                {
                    'id': '1',
                    'ticket_type': 'request',
                    'template_contents': 'template',
                    'workflow_pattern_id': 'workflow',
                    'created_at': '2015-07-01',
                    'updated_at': '2015-07-01',
                    'deleted_at': '2015-07-01',
                    'deleted': True
                },
            ]},
        ),
    },
    '/v1/tickettemplates?sort_key=id&sort_dir=desc': {
        'GET': (
            {},
            {'tickettemplates': [
                {
                    'id': '1',
                    'ticket_type': 'request',
                    'template_contents': 'template',
                    'workflow_pattern_id': 'workflow',
                    'created_at': '2015-07-01',
                    'updated_at': '2015-07-01',
                    'deleted_at': '2015-07-01',
                    'deleted': True
                },
            ]},
        ),
    },
    '/v1/tickettemplates?sort_dir=desc&sort_dir=asc&' +
    'sort_key=id&sort_key=created_at': {
        'GET': (
            {},
            {'tickettemplates': [
                {
                    'id': '1',
                    'ticket_type': 'request',
                    'template_contents': 'template',
                    'workflow_pattern_id': 'workflow',
                    'created_at': '2015-07-01',
                    'updated_at': '2015-07-01',
                    'deleted_at': '2015-07-01',
                    'deleted': True
                },
            ]},
        ),
    },
    '/v1/tickettemplates?sort_dir=ni%3Fo&sort_key=ni%3Fo': {
        'GET': (
            {},
            {'tickettemplates': [
                {
                    'id': '1',
                    'ticket_type': 'request',
                    'template_contents': 'template',
                    'workflow_pattern_id': 'workflow',
                    'created_at': '2015-07-01',
                    'updated_at': '2015-07-01',
                    'deleted_at': '2015-07-01',
                    'deleted': True
                },
            ]},
        ),
    },
    '/v1/tickettemplates?force_show_deleted=True': {
        'GET': (
            {},
            {'tickettemplates': [
                {
                    'id': '1',
                    'ticket_type': 'request',
                    'template_contents': 'template',
                    'workflow_pattern_id': 'workflow',
                    'created_at': '2015-07-01',
                    'updated_at': '2015-07-01',
                    'deleted_at': '2015-07-01',
                    'deleted': True
                },
            ]},
        ),
    },
    '/v1/tickettemplates?ticket_type=request': {
        'GET': (
            {},
            {'tickettemplates': [
                {
                    'id': '1',
                    'ticket_type': 'request',
                    'template_contents': 'template',
                    'workflow_pattern_id': 'workflow',
                    'created_at': '2015-07-01',
                    'updated_at': '2015-07-01',
                    'deleted_at': '2015-07-01',
                    'deleted': True
                },
            ]},
        ),
    },
    '/v1/tickettemplates?ticket_type=New+Contract%2Crequest': {
        'GET': (
            {},
            {'tickettemplates': [
                {
                    'id': '1',
                    'ticket_type': 'request',
                    'template_contents': 'template',
                    'workflow_pattern_id': 'workflow',
                    'created_at': '2015-07-01',
                    'updated_at': '2015-07-01',
                    'deleted_at': '2015-07-01',
                    'deleted': True
                },
                {
                    'id': '2',
                    'ticket_type': 'New Contract',
                    'template_contents': 'template',
                    'workflow_pattern_id': 'workflow',
                    'created_at': '2015-07-02',
                    'updated_at': '2015-07-02',
                    'deleted_at': '2015-07-02',
                    'deleted': True
                },
            ]},
        ),
    },
    '/v1/tickettemplates?ticket_type=ni%C3%B1o': {
        'GET': (
            {},
            {'tickettemplates': [
                {
                    'id': '1',
                    'ticket_type': 'request',
                    'template_contents': 'template',
                    'workflow_pattern_id': 'workflow',
                    'created_at': '2015-07-01',
                    'updated_at': '2015-07-01',
                    'deleted_at': '2015-07-01',
                    'deleted': True
                },
            ]},
        ),
    },
}


class TickettemplateManagerTest(testtools.TestCase):
    """TickettemplateManager Test class."""

    def setUp(self):
        """Setup test class."""
        super(TickettemplateManagerTest, self).setUp()
        self.api = utils.FakeAPI(fixtures)
        self.mgr = tickettemplates.TickettemplateManager(self.api)

    def test_get(self):
        """Test get method."""
        tickettemplate = self.mgr.get('1')
        expect = [('GET', '/v1/tickettemplates/1', {}, None)]

        self.assertEqual(expect, self.api.calls)
        self.assertEqual('1', tickettemplate.id)
        self.assertEqual('template', tickettemplate.template_contents)

    def test_get_encoding(self):
        """Test get method by contain multibyte-code response."""
        tickettemplate = self.mgr.get('2')
        expect = [('GET', '/v1/tickettemplates/2', {}, None)]

        self.assertEqual(expect, self.api.calls)
        self.assertEqual(u"ni\xf1o", tickettemplate.template_contents)

    def test_list(self):
        """Test list method."""
        tickettemplate = list(self.mgr.list())
        expect = [('GET', '/v1/tickettemplates', {}, None)]

        self.assertEqual(expect, self.api.calls)
        self.assertEqual(2, len(tickettemplate))
        self.assertEqual('1', tickettemplate[0].id)
        self.assertEqual('2', tickettemplate[1].id)

    def test_list_limit(self):
        """Test list method by add limit option."""
        kwargs = {'limit': 1}
        list(self.mgr.list(kwargs))
        expect = [('GET', '/v1/tickettemplates?' +
                   common_utils.urlencode(kwargs),
                   {}, None)]

        self.assertEqual(expect, self.api.calls)

    def test_list_marker(self):
        """Test list method by add marker option.
        """
        kwargs = {'marker': 'a'}
        list(self.mgr.list(kwargs))
        expect = [('GET', '/v1/tickettemplates?' +
                   common_utils.urlencode(kwargs),
                   {}, None)]

        self.assertEqual(expect, self.api.calls)

    def test_list_sort(self):
        """Test list method by add sort-key and sort-dir options."""
        kwargs = {'sort_dir': ['desc'], 'sort_key': ['id']}
        list(self.mgr.list(kwargs))
        expect = [('GET', '/v1/tickettemplates?' +
                   'sort_dir=desc&sort_key=id',
                   {}, None)]

        self.assertEqual(expect, self.api.calls)

    def test_list_sort_multi_parameter(self):
        """Test list method by add multi sort options."""
        kwargs = {'sort_dir': ['desc', 'asc'],
                  'sort_key': ['id', 'created_at']}
        list(self.mgr.list(kwargs))
        expect = [('GET', '/v1/tickettemplates?' +
                   'sort_dir=desc&sort_dir=asc' +
                   '&sort_key=id&sort_key=created_at',
                   {}, None)]

        self.assertEqual(expect, self.api.calls)

    def test_list_sort_encoding(self):
        """Test list method by add multi byte sort-key
        and multi byte sort-dir options.
        """
        kwargs = {'sort_dir': [u"ni\xf1o"], 'sort_key': [u"ni\xf1o"]}
        list(self.mgr.list(kwargs))
        expect = [('GET', '/v1/tickettemplates?' +
                   'sort_dir=ni%3Fo&sort_key=ni%3Fo',
                   {}, None)]

        self.assertEqual(expect, self.api.calls)

    def test_list_no_data(self):
        """Test list method by add marker option."""
        kwargs = {'marker': 'nodata'}
        list(self.mgr.list(kwargs))
        expect = [('GET', '/v1/tickettemplates?' +
                   common_utils.urlencode(kwargs),
                   {}, None)]

        self.assertEqual(expect, self.api.calls)

    def test_list_force_show_deleted(self):
        """Test list method by add force show deleted option."""
        kwargs = {'force_show_deleted': True}
        list(self.mgr.list(kwargs))
        expect = [('GET', '/v1/tickettemplates?' +
                   common_utils.urlencode(kwargs),
                   {}, None)]

        self.assertEqual(expect, self.api.calls)

    def test_list_single_ticket_type(self):
        """Test 'List search of tickettemplate.'
        Test of if you filtering single ticket type.
        """
        kwargs = {'ticket_type': 'request'}
        tickettemplate = list(self.mgr.list(kwargs))
        expect = [('GET', '/v1/tickettemplates?' +
                   common_utils.urlencode(kwargs),
                   {}, None)]

        self.assertEqual(expect, self.api.calls)
        self.assertEqual(1, len(tickettemplate))

    def test_list_multi_ticket_type(self):
        """Test 'List search of tickettemplate.'
        Test of if you filtering multiple ticket type.
        """
        kwargs = {'ticket_type': 'New Contract,request'}
        tickettemplate = list(self.mgr.list(kwargs))
        expect = [('GET', '/v1/tickettemplates?' +
                   common_utils.urlencode(kwargs),
                   {}, None)]

        self.assertEqual(expect, self.api.calls)
        self.assertEqual(2, len(tickettemplate))

    def test_list_ticket_type_encoding(self):
        """Test 'List search of tickettemplate.'
        Test of if you filtering multi byte ticket type.
        """
        kwargs = {'ticket_type': u"ni\xf1o"}
        tickettemplate = list(self.mgr.list(kwargs))
        expect = [('GET', '/v1/tickettemplates?' +
                   common_utils.urlencode(kwargs),
                   {}, None)]

        self.assertEqual(expect, self.api.calls)
        self.assertEqual(1, len(tickettemplate))

    def test_create(self):
        """Test 'Create of tickettemplate'."""

        template_contents = self._get_dict_contents(
            'template_contents', '20160627')

        kwargs = {
            'template_contents': template_contents
        }
        expectResponse = {
            'tickettemplate': kwargs
        }

        self.mgr.create(kwargs)
        expect = [('POST', '/v1/tickettemplates', {},
                   expectResponse.items())]

        self.assertEqual(expect, self.api.calls)

    def test_delete(self):
        """Test delete method."""
        self.mgr.delete('1')
        expect = [('DELETE', '/v1/tickettemplates/1', {}, None)]

        self.assertEqual(expect, self.api.calls)

    def _get_dict_contents(self, file_prefix, version=None):
        file_name = None
        if version:
            file_name = '%(file_prefix)s_%(version)s.json' % {
                'file_prefix': file_prefix, 'version': version}
        else:
            file_name = '%(file_prefix)s.json' % {
                'file_prefix': file_prefix}
        obj = codecs.open(
            os.path.join(FILES_DIR, file_name), 'r', 'utf-8').read()
        return json.loads(obj, 'utf-8')
