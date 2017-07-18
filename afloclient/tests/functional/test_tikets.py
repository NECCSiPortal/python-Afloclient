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
import time
import uuid

from tempest_lib.cli import output_parser
from tempest_lib import exceptions

from afloclient.tests.functional import base
from afloclient.tests.functional import test_tickettemplates
from afloclient.tests.functional import test_workflowpatterns

_RETRY_COUNT = 10
_CREATE_TICKET_COUNT = 2
_COLUMN_WORKFLOW_ID = 0
_COLUMN_WORKFLOW_STATUS = 2
_COLUMN_WORKFLOW_STATUS_CODE = 3


@ddt.ddt
class ClientTestTickets(base.BaseTestCase):
    """Test ticket of aflo component service."""

    @ddt.data('admin')
    def test_ticket(self, role):
        """Do a test of 'Ticket commands'
        Test the operation of the List, Get, Update, Delete commands result.
        """
        # Create data.
        workflow_pattern_id = \
            test_workflowpatterns.create_workflow_pattern(
                self, role, ['workflow_pattern_contents_ticket_001.json'])
        ticket_template_id = \
            test_tickettemplates.create_tickettemplate_pattern(
                self, role,
                ['ticket_template_contents_ticket_001'], '20160627')

        # Add records
        ticket_id = self._create_ticket(role, ticket_template_id[0])

        # Get records by list.
        self._list_ticket(role, ticket_id)

        # Get records by workflow get.
        (workflow_id1, workflow_id2) = self._get_workflow(role, ticket_id)

        # Update records
        self._update_ticket(role, ticket_id, workflow_id1, workflow_id2)

        # Delete record
        self._delete_ticket(role, ticket_id)

        # Delete data.
        test_tickettemplates.delete_tickettemplate_pattern(
            self, role, ticket_template_id)
        test_workflowpatterns.delete_workflow_pattern(
            self, role, workflow_pattern_id)

    def _create_ticket(self, role, ticket_template_id):
        """Create ticket data.
        :param role: running user.
        """
        ticket_id = []

        for i in range(_CREATE_TICKET_COUNT):
            st_create = self.clients[role].run_command(
                'ticket-create',
                params=' --ticket-template-id {0}'
                       ' --ticket-detail {1}'
                       ' --status-code {2}'.format(
                           ticket_template_id, '\'{"num": "0"}\'',
                           "applied"))

            # Check got UUID
            id = output_parser.tables(st_create)[0]['values'][0][0]

            self.assertTrue(id is not None)

            ticket_id.append(id)

        return ticket_id

    def _get_workflow(self, role, ticket_id):
        """Get workflow data of ticket.
        :param role: running user.
        :param ticket_id: ticket id.
        """
        st_work = self.clients[role].run_command(
            'workflow-get',
            params='--id ' + ticket_id[0])
        workflows = output_parser.tables(st_work)[0]['values']

        last = filter(lambda row:
                      row[_COLUMN_WORKFLOW_STATUS] == '1',
                      workflows)[0]

        next = filter(lambda row:
                      row[_COLUMN_WORKFLOW_STATUS_CODE] == 'withdrew',
                      workflows)[0]

        return (last[_COLUMN_WORKFLOW_ID],
                next[_COLUMN_WORKFLOW_ID])

    def _list_ticket(self, role, ticket_id):
        """List ticket data.
        :param role: running user.
        :param ticket_id: ticket id.
        """
        for c in range(0, _RETRY_COUNT):
            st_list = self.clients[role].run_command('ticket-list')
            # DB Entry is asynchronous process.
            # Wait for a seconds.
            if len(output_parser.tables(st_list)[0]['values']) \
                    < _CREATE_TICKET_COUNT:
                if c < _RETRY_COUNT - 1:
                    time.sleep(1)
                else:
                    raise exceptions.TimeoutException(str(st_list))
            else:
                break

        # Search data not exists,
        #  data by all setting filter condition.
        st_list = self.clients[role].run_command(
            'ticket-list',
            params=' --tenant-id {0}'
                   ' --last-status-code {1}'
                   ' --ticket-template-id {2}'
                   ' --ticket-type {3}'
                   ' --target-id {4}'
                   ' --owner-at-from {5}'
                   ' --owner-at-to {6}'
                   ' --owner-id {7}'
                   ' --last-confirmed-at-from {8}'
                   ' --last-confirmed-at-to {9}'
                   ' --last-confirmer-id {10}'
                   ' --sort-key {11}'
                   ' --sort-dir {12}'
                   ' --limit {13}'
                   ' --marker {14}'
                   ' --ticket-template-name {15}'
                   ' --application-kinds-name {16}'.format(
                       self.clients[role].tenant_name,
                       'applied',
                       '2',
                       'goods',
                       '3902653a15f74b55912b812f1f537e87',
                       '2015-07-01T00:00:00.000000',
                       '2015-07-01T00:00:00.000000',
                       '99b3abc617c14a258190096e0258aa9b',
                       '2015-07-20T00:00:00.000000',
                       '2015-07-20T00:00:00.000000',
                       '99b3abc617c14a258190096e0258aa9b',
                       'created_at',
                       'asc',
                       '1',
                       ticket_id[0],
                       '"flat-rate-1(ja) *root:three"',
                       'application_kinds_2(ja)'))

        self.assertEqual(len(output_parser.tables(st_list)[0]['values']),
                         0)

        # Search all data.
        st_list = self.clients[role].run_command(
            'ticket-list', params='')
        self.assertEqual(len(output_parser.tables(st_list)[0]['values']),
                         _CREATE_TICKET_COUNT)

        # Search data not exists,
        #  data by template contents invalid condition.
        self._ticket_list_irregular_template_contents(role)

    def _ticket_list_irregular_template_contents(self, role):
        """Test 'Ticket commands'
        Test the operation of the List command(Ignore parameters).
        """
        args = ['--application-kinds-name aaaaa',
                '--ticket-template-name aaaaa']

        for arg in args:
            st_list = self.clients[role].run_command('ticket-list %s' % arg)
            self.assertEqual(0,
                             len(output_parser.tables(st_list)[0]['values']))

    def _update_ticket(self, role, ticket_id, workflow_id1, workflow_id2):
        """Update ticket data.
        :param role: running user.
        :param ticket_id: ticket id.
        :param workflow_id1: last workflow id.
        :param workflow_id2: next workflow id
        """
        self.clients[role].run_command(
            'ticket-update',
            params=' --id {0}'
                   ' --last-workflow-id {1}'
                   ' --next-workflow-id {2}'
                   ' --last-status-code {3}'
                   ' --next-status-code {4}'
                   ' --additional-data {5}'.format(
                       ticket_id[0],
                       workflow_id1, workflow_id2,
                       "applied", 'withdrew',
                       '\'{"description": "test"}\''))

        # Get records.
        for c in range(0, _RETRY_COUNT):
            st_work = self.clients[role].run_command(
                'workflow-get',
                params='--id ' + ticket_id[0])
            workflow = output_parser.tables(st_work)[0]['values']
            now_status = filter(lambda row:
                                row[3] == 'withdrew',
                                workflow)
            # DB Entry is asynchronous process.
            # Wait for a seconds.
            if now_status[0][2] != '1':
                if c < _RETRY_COUNT - 1:
                    time.sleep(1)
                else:
                    raise exceptions.TimeoutException(str(st_work))
            else:
                break

    def _delete_ticket(self, role, ticket_id):
        """Delete ticket data.
        :param role: running user.
        :param ticket_id: ticket id.
        """
        for id in ticket_id:
            self.clients[role].run_command('ticket-delete',
                                           params='--id ' + id)

        # Get records.
        for c in range(0, _RETRY_COUNT):
            st_list = self.clients[role].run_command(
                'ticket-list', params='')

            # DB Entry is asynchronous process.
            # Wait for a seconds.
            if len(output_parser.tables(st_list)[0]['values']) != 0:
                if c < _RETRY_COUNT - 1:
                    time.sleep(1)
                else:
                    raise exceptions.TimeoutException(str(st_list))
            else:
                break

    @ddt.data('admin', 'user')
    def test_ticket_invalid_get_irregular_no_data(self, role):
        """Do a test of 'Ticket commands'
        Test the operation of the Get command(Not exist ticket id).
        """
        id = str(uuid.uuid4())

        self.assertRaises(exceptions.CommandFailed,
                          self.clients[role].run_command,
                          'ticket-get',
                          params='--id ' + id)

    @ddt.data('admin', 'user')
    def test_workflow_invalid_get_irregular_no_data(self, role):
        """Do a test of 'Workflow commands'
        Test the operation of the Get command(Not exist ticket id).
        """
        id = str(uuid.uuid4())

        self.assertRaises(exceptions.CommandFailed,
                          self.clients[role].run_command,
                          'workflow-get',
                          params='--id ' + id)

    @ddt.data('admin', 'user')
    def test_ticket_list_irregular_params(self, role):
        """Do a test of 'Ticket commands'
        Test the operation of the List command(Ignore parameters).
        """
        args = ['--sort-key a',
                '--sort-dir a',
                '--limit a'
                '--force-show-deleted a']

        for arg in args:
            # List data.
            self.assertRaises(exceptions.CommandFailed,
                              self.clients[role].run_command,
                              'ticket-list %s' % arg)

    @ddt.data('admin', 'user')
    def test_ticket_invalid_update_irregular_workflow(self, role):
        """Do a test of 'Ticket commands'
        Test the operation of the Update command(Not exist ticket id).
        """
        id = str(uuid.uuid4())

        self.assertRaises(exceptions.CommandFailed,
                          self.clients[role].run_command,
                          'ticket-update',
                          params=' --last-workflow-id {0}'
                                 ' --next-workflow-id {1}'
                                 ' --status-code {2}'.format(
                                 id, id, 'a'))

    @ddt.data('admin')
    def test_ticket_invalid_delete_irregular_no_data(self, role):
        """Do a test of 'Ticket commands'
        Test the operation of the Delete command(Not exist ticket id).
        """
        id = str(uuid.uuid4())

        # This test case is success pattern,
        # delete method is async.
        st = self.clients[role].run_command('ticket-delete',
                                            params='--id ' + id)

        self.assertFalse(st)

    @ddt.data('user')
    def test_ticket_invalid_delete_irregular_no_authority(self, role):
        """Do a test of 'Ticket commands'
        Test the operation of the Delete command(Not exist authority).
        """
        id = str(uuid.uuid4())

        self.assertRaises(exceptions.CommandFailed,
                          self.clients[role].run_command,
                          'ticket-delete',
                          params='--id ' + id)
