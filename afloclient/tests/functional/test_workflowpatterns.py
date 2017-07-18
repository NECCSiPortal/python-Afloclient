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

import ddt
import uuid

from tempest_lib.cli import output_parser
from tempest_lib import exceptions

from afloclient.tests.functional import base

FOLDER_PATH = 'afloclient/tests/functional/operation_definition_files/'


@ddt.ddt
class ClientTestWorkflowPattern(base.BaseTestCase):
    """Test workflow pattern of aflo component service."""

    @ddt.data('admin')
    def test_workflow_pattern(self, role):
        """Test 'Workflow pattern commands'
        Test the operation of the Create and Delete commands result.
        """
        # Create data.
        id = create_workflow_pattern(
            self, role, ['workflow_pattern_contents_workflow_001.json'])

        # Delete data.
        delete_workflow_pattern(self, role, id)

    @ddt.data('user')
    def test_workflow_pattern_invalid_craete_irregular_no_authority(
            self, role):
        """Test 'Create workflow pattern commands'
        Test the operation of the not exist authority.
        """
        self.assertRaises(exceptions.CommandFailed,
                          create_workflow_pattern,
                          self,
                          role,
                          ['workflow_pattern_contents_workflow_001.json'])

    @ddt.data('user')
    def test_workflow_pattern_invalid_delete_irregular_no_authority(
            self, role):
        """Test 'Delete workflow pattern commands'
        Test the operation of the not exist authority.
        """
        id = str(uuid.uuid4())

        self.assertRaises(exceptions.CommandFailed,
                          delete_workflow_pattern,
                          self,
                          role,
                          [id])


def create_workflow_pattern(self, role, file_names):
    """Create a workflow pattern.
    :param role: Running user.
    :param file_names: Workflow pattern files.
    """
    id = []

    for file_name in file_names:
        file = FOLDER_PATH + file_name

        st = self.clients[role].run_command(
            'workflowpattern-create',
            params=' --file %s' % file)

        id.append(output_parser.tables(st)[0]['values'][0][0])

    return id


def delete_workflow_pattern(self, role, ids):
    """Create a workflow pattern.
    :param role: Running user.
    :param ids: Workflow pattern id.
    """
    for id in ids:
        self.clients[role].run_command(
            'workflowpattern-delete',
            params='--id %s' % id)
