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
import os
import uuid

from tempest_lib.cli import output_parser
from tempest_lib import exceptions

from afloclient.tests.functional import base
from afloclient.tests.functional import test_workflowpatterns

FOLDER_PATH = 'afloclient/tests/functional/operation_definition_files/'


@ddt.ddt
class ClientTestTickettemplates(base.BaseTestCase):
    """Test tickettemplate of aflo component service."""

    @ddt.data('admin')
    def test_tickettemplate(self, role):
        """Do a test of 'Tickettemplate commands'
        Test the operation of the List and Get commands result.
        """
        # Create data.
        workflow_pattern_id = \
            test_workflowpatterns.create_workflow_pattern(
                self, role, ['workflow_pattern_contents_001.json'])
        ticket_template_id = create_tickettemplate_pattern(
            self, role, ['ticket_template_contents_001'], '20160627')

        # List data.
        st_get = self.clients[role].run_command('tickettemplate-list')
        list = output_parser.tables(st_get)[0]['values']

        # Got list had greater one a row.
        self.assertTrue(len(list), 1)

        self.clients[role].run_command(
            'tickettemplate-list',
            params=' --limit 1' +
            ' --marker %s' % ticket_template_id[0] +
            ' --sort-key created_at' +
            ' --sort-dir asc' +
            ' --force-show-deleted true' +
            ' --ticket-type "New Contract"' +
            ' --enable-expansion-filters false')

        st_get = self.clients[role].run_command(
            'tickettemplate-get',
            params='--id ' + ticket_template_id[0])

        self.assertEqual(ticket_template_id[0],
                         output_parser.tables(st_get)[0]['values'][0][0])

        st_get = self.clients[role].run_command(
            'tickettemplate-list',
            params=' --enable-expansion-filters true')
        list = output_parser.tables(st_get)[0]['values']

        # 0 row because there is no valid items.
        self.assertTrue(len(list), 0)

        st_get = self.clients[role].run_command(
            'tickettemplate-list',
            params=' --enable-expansion-filters aaaaa')
        list = output_parser.tables(st_get)[0]['values']

        # Invalid values will be the same as 'False'.
        self.assertTrue(len(list), 1)

        # Delete data.
        delete_tickettemplate_pattern(
            self, role, ticket_template_id)
        test_workflowpatterns.delete_workflow_pattern(
            self, role, workflow_pattern_id)

    @ddt.data('admin')
    def test_tickettemplate_list_multi_ticket_type(self, role):
        """Test 'List search of tickettemplate.'
        Test of if you filtering multi ticket type.
        """
        # Create data.
        workflow_pattern_id = \
            test_workflowpatterns.create_workflow_pattern(
                self, role,
                ['workflow_pattern_contents_002.json',
                 'workflow_pattern_contents_003.json'])
        ticket_template_id = create_tickettemplate_pattern(
            self, role,
            ['ticket_template_contents_002',
             'ticket_template_contents_003',
             'ticket_template_contents_003'],
            '20160627')

        st_get = self.clients[role].run_command(
            'tickettemplate-list',
            params=' --ticket-type "New Contract,request"')

        list = output_parser.tables(st_get)[0]['values']

        for id in ticket_template_id:
            self.assertTrue(len(filter(lambda row:
                                       row[0] == id,
                                       list)),
                            1)

        # Delete data.
        delete_tickettemplate_pattern(
            self, role, ticket_template_id)
        test_workflowpatterns.delete_workflow_pattern(
            self, role, workflow_pattern_id)

    @ddt.data('admin')
    def test_tickettemplate_list_irregular_ticket_type(self, role):
        """Test 'List search of tickettemplate.'
        Test of if you filtering irregular ticket type.
        """
        # Create data.
        workflow_pattern_id = \
            test_workflowpatterns.create_workflow_pattern(
                self, role, ['workflow_pattern_contents_004.json'])
        ticket_template_id = create_tickettemplate_pattern(
            self, role, ['ticket_template_contents_004'], '20160627')

        st_get1 = self.clients[role].run_command(
            'tickettemplate-list',
            params=' --ticket-type aaaaa')

        self.assertEqual(0,
                         len(output_parser.tables(st_get1)[0]['values']))

        # Delete data.
        delete_tickettemplate_pattern(
            self, role, ticket_template_id)
        test_workflowpatterns.delete_workflow_pattern(
            self, role, workflow_pattern_id)

    @ddt.data('admin', 'user')
    def test_tickettemplate_list_irregular_params(self, role):
        """Do a test of 'Ticket template commands'
        Test the operation of the List command(Irregular parameters).
        """
        args = ['--sort-key a',
                '--sort-dir a',
                '--limit a'
                '--force-show-deleted a']

        for arg in args:
            # List data.
            self.assertRaises(exceptions.CommandFailed,
                              self.clients[role].run_command,
                              'tickettemplate-list %s' % arg)

    @ddt.data('admin', 'user')
    def test_tickettemplate_get_irregular_no_data(self, role):
        """Do a test of 'Ticket template commands'
        Test the operation of the Get command(Not exist ticket template id).
        """
        id = str(uuid.uuid4())

        self.assertRaises(exceptions.CommandFailed,
                          self.clients[role].run_command,
                          'tickettemplate-get',
                          params='--id %s' % id)

    @ddt.data('user')
    def test_tickettemplate_invalid_craete_irregular_no_authority(
            self, role):
        """Test 'Create ticket template commands'
        Test the operation of the not exist authority.
        """
        self.assertRaises(exceptions.CommandFailed,
                          create_tickettemplate_pattern,
                          self, role,
                          ['ticket_template_contents_001'],
                          '20160627')

    @ddt.data('user')
    def test_tickettemplate_invalid_delete_irregular_no_authority(
            self, role):
        """Test 'Delete ticket template commands'
        Test the operation of the not exist authority.
        """
        id = str(uuid.uuid4())

        self.assertRaises(exceptions.CommandFailed,
                          delete_tickettemplate_pattern,
                          self,
                          role,
                          [id])


def create_tickettemplate_pattern(self, role, files_prefix, version):
    """Create a ticket template.
    :param role: Running user.
    :param file_names: Ticket template files.
    """
    id = []

    for file_prefix in files_prefix:
        file_name = '%(file_prefix)s_%(version)s.json' % {
            'file_prefix': file_prefix, 'version': version}
        file_path = os.path.join(FOLDER_PATH, file_name)

        st = self.clients[role].run_command('tickettemplate-create',
                                            params=' --file %s' % file_path)

        id.append(output_parser.tables(st)[0]['values'][0][0])

    return id


def delete_tickettemplate_pattern(self, role, ids):
    """Create a ticket template.
    :param role: Running user.
    :param id: Ticket template id.
    """
    for id in ids:
        self.clients[role].run_command(
            'tickettemplate-delete',
            params='--id %s' % id)
