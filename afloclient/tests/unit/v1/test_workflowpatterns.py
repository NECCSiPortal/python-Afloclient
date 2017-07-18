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

"""Test afloclient/v1/workflowpatterns.py."""

import codecs
import json
import testtools

from afloclient.tests.unit import utils
from afloclient.v1 import workflowpatterns

# from afloclient.v1 import client
#  request fixtures
#    (request url, request header, request parameter).
fixtures = {
    '/v1/workflowpatterns': {
        'POST': (
            {},
            {'workflowpattern': {
                'id': '1',
                'code': 'wf_pattern_code',
                'wf_pattern_contents': {'contents'},
                'created_at': '2015-07-01',
                'updated_at': '2015-07-01',
                'deleted_at': '2015-07-01',
                'deleted': True
            }},
        ),
    },
    '/v1/workflowpatterns/1': {
        'DELETE': (
            {},
            None,
        ),
    },
}


class WorkflowpatternManagerTest(testtools.TestCase):
    """WorkflowpatternManager Test class."""

    def setUp(self):
        """Setup test class."""
        super(WorkflowpatternManagerTest, self).setUp()
        self.api = utils.FakeAPI(fixtures)
        self.mgr = workflowpatterns.WorkflowpatternManager(self.api)

    def test_create(self):
        """Test 'Create of workflow pattern'."""

        workflow_pattern_string = codecs.open(
            'afloclient/tests/unit/v1/operation_definition_files'
            '/workflow_pattern_contents.json',
            'r', 'utf-8').read()
        wf_pattern_contents = json.loads(workflow_pattern_string, 'utf-8')

        kwargs = {
            'wf_pattern_contents': wf_pattern_contents
        }
        expectResponse = {
            'workflowpattern': kwargs
        }

        self.mgr.create(kwargs)
        expect = [('POST', '/v1/workflowpatterns', {}, expectResponse.items())]

        self.assertEqual(expect, self.api.calls)

    def test_delete(self):
        """Test delete method."""
        self.mgr.delete('1')
        expect = [('DELETE', '/v1/workflowpatterns/1', {}, None)]

        self.assertEqual(expect, self.api.calls)
