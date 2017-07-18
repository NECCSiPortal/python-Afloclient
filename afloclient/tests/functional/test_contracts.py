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

from afloclient import config
from afloclient.tests.functional import base

CONF = config.CONF


@ddt.ddt
class ClientTestContracts(base.BaseTestCase):
    """Test contract of aflo component service."""

    @ddt.data('admin', 'user')
    def test_contract(self, role):
        """Test of 'Contract commands'
       Test the operation of the List, Get, Update, Delete commands result.
        :param role: running user.
        """

        # Get users project_id
        if role == 'user':
            project_id = CONF.project_id
        else:
            project_id = CONF.admin_project_id

        # Add records
        contract_id, contract_id_dammy = self._create_contract('admin',
                                                               project_id)

        # Get records by list.
        self._list_contract(role, contract_id)

        # Get records by contract get.
        self._get_contract(role, contract_id, project_id)

        # Update records
        if role == 'admin':
            self._update_contract(role, contract_id)

        # Delete records
        self.clients['admin']\
            .run_command('contract-delete',
                         params=' --contract-id %s' % contract_id)

        self.clients['admin']\
            .run_command('contract-delete',
                         params=' --contract-id %s' % contract_id_dammy)

        self.assertRaises(exceptions.CommandFailed,
                          self.clients['admin'].run_command,
                          'contract-delete',
                          params=' --contract-id %s' % contract_id)

    def _create_contract(self, role, project_id):
        """Create contract data.
        :param role: running user.
        """
        st_create_dammy = self.clients[role].run_command(
            'contract-create',
            params=' --region-id {0}'
                   ' --project-id {1}'
                   ' --project-name {2}'
                   ' --catalog-id {3}'
                   ' --catalog-name {4}'
                   ' --num {5}'
                   ' --parent-ticket-template-id {6}'
                   ' --ticket-template-id {7}'
                   ' --parent-ticket-template-name {8}'
                   ' --ticket-template-name {9}'
                   ' --parent-application-kinds-name {10}'
                   ' --application-kinds-name {11}'
                   ' --cancel-application-id {12}'
                   ' --application-id {13}'
                   ' --application-name {14}'
                   ' --application-date {15}'
                   ' --parent-contract-id {16}'
                   ' --lifetime-start {17}'
                   ' --lifetime-end {18}'
                   .format('region_id_dammy',
                           '5d19ec09dfb04e83b8385a2365c217e0',
                           'project_name',
                           'catalog_id',
                           'catalog_name',
                           '1234',
                           'parent_ticket_template_id',
                           'ticket_template_id',
                           'parent_ticket_template_name',
                           'ticket_template_name',
                           'parent_application_kinds_name',
                           'application_kinds_name',
                           'cancel_application_id',
                           'application_id',
                           'application_name',
                           '2015-09-10T06:07:08.345678',
                           'parent_contract_id',
                           '2015-01-01T01:02:03.123456',
                           '2015-11-12T04:05:06.234567'))

        st_create = self.clients[role].run_command(
            'contract-create',
            params=' --region-id {0}'
                   ' --project-id {1}'
                   ' --project-name {2}'
                   ' --catalog-id {3}'
                   ' --catalog-name {4}'
                   ' --num {5}'
                   ' --parent-ticket-template-id {6}'
                   ' --ticket-template-id {7}'
                   ' --parent-ticket-template-name {8}'
                   ' --ticket-template-name {9}'
                   ' --parent-application-kinds-name {10}'
                   ' --application-kinds-name {11}'
                   ' --cancel-application-id {12}'
                   ' --application-id {13}'
                   ' --application-name {14}'
                   ' --application-date {15}'
                   ' --parent-contract-id {16}'
                   ' --lifetime-start {17}'
                   ' --lifetime-end {18}'
                   .format('region_id',
                           project_id,
                           'project_name',
                           'catalog_id',
                           'catalog_name',
                           '1234',
                           'parent_ticket_template_id',
                           'ticket_template_id',
                           'parent_ticket_template_name',
                           'ticket_template_name',
                           'parent_application_kinds_name',
                           'application_kinds_name',
                           'cancel_application_id',
                           'application_id',
                           'application_name',
                           '2015-09-10T06:07:08.345678',
                           'parent_contract_id',
                           '2015-01-01T01:02:03.123456',
                           '2015-11-12T04:05:06.234567'))

        # Check got UUID
        contract_id = output_parser.tables(st_create)[0]['values'][0][0]
        self.assertTrue(contract_id is not None)
        contract_id_dammy = \
            output_parser.tables(st_create_dammy)[0]['values'][0][0]

        # Check all param
        check_param = {'contract_id': contract_id,
                       'region-id': 'region_id',
                       'project-id': project_id,
                       'project-name': 'project_name',
                       'catalog-id': 'catalog_id',
                       'catalog-name': 'catalog_name',
                       'num': '1234',
                       'parent-ticket-template-id':
                       'parent_ticket_template_id',
                       'ticket-template-id': 'ticket_template_id',
                       'parent-ticket-template-name':
                       'parent_ticket_template_name',
                       'ticket-template-name': 'ticket_template_name',
                       'parent-application-kinds-name':
                       'parent_application_kinds_name',
                       'application-kinds-name': 'application_kinds_name',
                       'cancel-application-id': 'cancel_application_id',
                       'application-id': 'application_id',
                       'application-name': 'application_name',
                       'application-date': '2015-09-10T06:07:08.000000',
                       'parent-contract-id': 'parent_contract_id',
                       'lifetime-start': '2015-01-01T01:02:03.000000',
                       'lifetime-end': '2015-11-12T04:05:06.000000',
                       }
        self._check_return_param(
            output_parser.tables(st_create)[0]['values'][0],
            check_param)

        return contract_id, contract_id_dammy

    def _get_contract(self, role, contract_id, project_id):
        """Get contract data.
        :param role: running user.
        :param contract_id: Contract id.
        """
        st_get = self.clients[role].run_command(
            'contract-get',
            params=' --contract-id ' + contract_id)
        contract = output_parser.tables(st_get)[0]['values'][0]

        # Check all param
        check_param = {'contract_id': contract_id,
                       'region-id': 'region_id',
                       'project-id': project_id,
                       'project-name': 'project_name',
                       'catalog-id': 'catalog_id',
                       'catalog-name': 'catalog_name',
                       'num': '1234',
                       'parent-ticket-template-id':
                       'parent_ticket_template_id',
                       'ticket-template-id':
                       'ticket_template_id',
                       'parent-ticket-template-name':
                       'parent_ticket_template_name',
                       'ticket-template-name':
                       'ticket_template_name',
                       'parent-application-kinds-name':
                       'parent_application_kinds_name',
                       'application-kinds-name': 'application_kinds_name',
                       'cancel-application-id': 'cancel_application_id',
                       'application-id': 'application_id',
                       'application-name': 'application_name',
                       'application-date': '2015-09-10T06:07:08.000000',
                       'parent-contract-id': 'parent_contract_id',
                       'lifetime-start': '2015-01-01T01:02:03.000000',
                       'lifetime-end': '2015-11-12T04:05:06.000000',
                       }
        self._check_return_param(contract,
                                 check_param)

        return contract

    def _list_contract(self, role, contract_id):
        """List contract data.
        :param role: running user.
        """

        params = ' --lifetime {0}' \
                 ' --limit {1}' \
                 ' --sort-key {2}' \
                 ' --sort-dir {3}' \
                 .format('2015-09-28T00:00:00.000000',
                         '1000',
                         'contract_id',
                         'desc')
        if role == 'user':
            params = ' '.join([params,
                               '--project-id',
                               '5d19ec09dfb04e83b8385a2365c217e0'])
        st_list = self.clients[role].run_command(
            'contract-list',
            params=params)

        contract_list = output_parser.tables(st_list)[0]['values']
        self.assertTrue(len(contract_list) >= 1)

        # Check all param
        result = False
        for contract in contract_list:
            if contract[0] == contract_id:
                result = True
                break

        self.assertTrue(result)

        return contract_list

    def _update_contract(self, role, contract_id):
        """Update contract data.
        :param role: running user.
        :param contract_id: Contract id.
        :param contract: contract.
        """
        st_update = self.clients[role].run_command(
            'contract-update',
            params=' --contract-id {0}'
                   ' --region-id {1}'
                   ' --project-id {2}'
                   ' --project-name {3}'
                   ' --catalog-id {4}'
                   ' --catalog-name {5}'
                   ' --num {6}'
                   ' --parent-ticket-template-id {7}'
                   ' --ticket-template-id {8}'
                   ' --parent-ticket-template-name {9}'
                   ' --ticket-template-name {10}'
                   ' --parent-application-kinds-name {11}'
                   ' --application-kinds-name {12}'
                   ' --cancel-application-id {13}'
                   ' --application-id {14}'
                   ' --application-name {15}'
                   ' --application-date {16}'
                   ' --parent-contract-id {17}'
                   ' --lifetime-start {18}'
                   ' --lifetime-end {19}'
                   .format(contract_id,
                           'region_id_updated',
                           '5d19ec09dfb04e83b8385a2365c217e0',
                           'project_name',
                           'catalog_id',
                           'catalog_name',
                           '1234',
                           'parent_ticket_template_id',
                           'ticket_template_id',
                           'parent_ticket_template_name',
                           'ticket_template_name',
                           'parent_application_kinds_name',
                           'application_kinds_name',
                           'cancel_application_id',
                           'application_id',
                           'application_name',
                           '2015-09-11T06:07:08.345678',
                           'parent_contract_id',
                           '2015-01-02T01:02:03.123456',
                           '2015-11-13T04:05:06.234567',))

        contract = output_parser.tables(st_update)[0]['values']

        # Check all param
        check_param = {'contract_id': contract_id,
                       'region-id': 'region_id_updated',
                       'project-id': '5d19ec09dfb04e83b8385a2365c217e0',
                       'project-name': 'project_name',
                       'catalog-id': 'catalog_id',
                       'catalog-name': 'catalog_name',
                       'num': '1234',
                       'parent-ticket-template-id':
                       'parent_ticket_template_id',
                       'ticket-template-id': 'ticket_template_id',
                       'parent-ticket-template-name':
                       'parent_ticket_template_name',
                       'ticket-template-name': 'ticket_template_name',
                       'parent-application-kinds-name':
                       'parent_application_kinds_name',
                       'application-kinds-name': 'application_kinds_name',
                       'cancel-application-id': 'cancel_application_id',
                       'application-id': 'application_id',
                       'application-name': 'application_name',
                       'application-date': '2015-09-11T06:07:08.345678',
                       'parent-contract-id': 'parent_contract_id',
                       'lifetime-start': '2015-01-02T01:02:03.123456',
                       'lifetime-end': '2015-11-13T04:05:06.234567',
                       }
        self._check_return_param(contract[0], check_param)

        return contract

    def _check_return_param(self, return_data, check_param):
        self.assertEqual(return_data[0], check_param['contract_id'])
        self.assertEqual(return_data[1], check_param['region-id'])
        self.assertEqual(return_data[2], check_param['project-id'])
        self.assertEqual(return_data[3], check_param['project-name'])
        self.assertEqual(return_data[4], check_param['catalog-id'])
        self.assertEqual(return_data[5], check_param['catalog-name'])
        self.assertEqual(return_data[6], check_param['num'])
        self.assertEqual(return_data[7],
                         check_param['parent-ticket-template-id'])
        self.assertEqual(return_data[8],
                         check_param['ticket-template-id'])
        self.assertEqual(return_data[9],
                         check_param['parent-ticket-template-name'])
        self.assertEqual(return_data[10],
                         check_param['parent-application-kinds-name'])
        self.assertEqual(return_data[11],
                         check_param['application-kinds-name'])
        self.assertEqual(return_data[12], check_param['cancel-application-id'])
        self.assertEqual(return_data[13], check_param['application-id'])
        self.assertEqual(return_data[14], check_param['ticket-template-name'])
        self.assertEqual(return_data[15], check_param['application-name'])
        self.assertEqual(return_data[16], check_param['application-date'])
        self.assertEqual(return_data[17], check_param['parent-contract-id'])
        self.assertEqual(return_data[18], check_param['lifetime-start'])
        self.assertEqual(return_data[19], check_param['lifetime-end'])
        self.assertIsNotNone(return_data[20])
        self.assertIsNotNone(return_data[21])
        self.assertEqual(return_data[22], 'None')
        self.assertEqual(return_data[23], 'False')
        self.assertEqual(return_data[24], 'None')
        self.assertEqual(return_data[25], 'None')
        self.assertEqual(return_data[26], 'None')
        self.assertEqual(return_data[27], 'None')
        self.assertEqual(return_data[28], 'None')
        self.assertEqual(return_data[29], 'None')

    @ddt.data('admin', 'user')
    def test_contract_invalid_show_irregular_no_data(self, role):
        """Test of 'contract commands'
        Test the operation of the Show command(Not exist contract id).
        :param role: running user.
        """
        contract_id = str(uuid.uuid4())

        self.assertRaises(exceptions.CommandFailed,
                          self.clients[role].run_command,
                          'contract-get',
                          params=' --contract-id ' + contract_id)

    @ddt.data('admin', 'user')
    def test_contract_list_irregular_params(self, role):
        """Test of 'contract commands'
        Test the operation of the List command(Ignore parameters).
        :param role: running user.
        """
        args = [' --lifetime a',
                ' --sort-key a',
                ' --sort-dir a',
                ' --limit a',
                ' --marker a',
                ' --force-show-deleted a']

        for arg in args:
            # List data.
            self.assertRaises(exceptions.CommandFailed,
                              self.clients[role].run_command,
                              'contract-list %s' % arg)

    @ddt.data('user')
    def test_contract_invalid_create_irregular_no_authority(self, role):
        """Test of 'contract commands'
        Test the operation of the Create command(Not exist authority).
        :param role: running user.
        """
        self.assertRaises(exceptions.CommandFailed,
                          self.clients[role].run_command,
                          'contract-create',
                          params=' --region-id {0}'
                                 ' --project-id {1}'
                                 ' --project-name {2}'
                                 ' --catalog-id {3}'
                                 ' --catalog-name {4}'
                                 ' --num {5}'
                                 ' --parent-ticket-template-id {6}'
                                 ' --ticket-template-id {7}'
                                 ' --parent-ticket-template-name {8}'
                                 ' --ticket-template-name {9}'
                                 ' --parent-application-kinds-name {10}'
                                 ' --application-kinds-name {11}'
                                 ' --cancel-application-id {12}'
                                 ' --application-id {13}'
                                 ' --application-name {14}'
                                 ' --application-date {15}'
                                 ' --parent-contract-id {16}'
                                 ' --lifetime-start {17}'
                                 ' --lifetime-end {18}'
                                 .format('region_id',
                                         'project_id',
                                         'project_name',
                                         'catalog_id',
                                         'catalog_name',
                                         '1234',
                                         'parent_ticket_template_id',
                                         'ticket_template_id',
                                         'parent_ticket_template_name',
                                         'ticket_template_name',
                                         'parent_application_kinds_name',
                                         'application_kinds_name',
                                         'cancel_application_id',
                                         'application_id',
                                         'application_name',
                                         '2015-09-10T06:07:08.345678',
                                         'parent_contract_id',
                                         '2015-01-01T01:02:03.123456',
                                         '2015-11-12T04:05:06.234567'))

    @ddt.data('admin', 'user')
    def test_contract_invalid_update_irregular_no_data(self, role):
        """Test of 'contract commands'
        Test the operation of the Update command(Not exist contract id).
        :param role: running user.
        """
        contract_id = str(uuid.uuid4())

        self.assertRaises(exceptions.CommandFailed,
                          self.clients[role].run_command,
                          'contract-update',
                          params=' --contract-id {0}'
                                 ' --region-id {1}'
                                 ' --lifetime-start {2}'
                                 ' --lifetime-end {3}'
                                 .format(contract_id, 'a', 'a', 'a'))

    @ddt.data('admin')
    def test_contract_invalid_delete_irregular_no_data(self, role):
        """Do a test of 'Contract commands'
        Test the operation of the Delete command(Not exist contract id).
        """
        contract_id = str(uuid.uuid4())

        self.assertRaises(exceptions.CommandFailed,
                          self.clients[role].run_command,
                          'contract-delete',
                          params=' --contract-id ' + contract_id)

    @ddt.data('user')
    def test_contract_invalid_delete_irregular_no_authority(self, role):
        """Do a test of 'contract commands'
        Test the operation of the Delete command(Not exist authority).
        """
        contract_id = str(uuid.uuid4())

        self.assertRaises(exceptions.CommandFailed,
                          self.clients[role].run_command,
                          'contract-delete',
                          params=' --contract-id ' + contract_id)
