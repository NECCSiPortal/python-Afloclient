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
#

import ddt
import uuid

from tempest_lib.cli import output_parser
from tempest_lib import exceptions

from afloclient import config
from afloclient.tests.functional import base

CONF = config.CONF


@ddt.ddt
class ClientTestCatalogScope(base.BaseTestCase):
    """Test catalog scope of aflo component service."""

    @ddt.data('admin', 'user')
    def test_catalog_scope(self, role):
        """Test of 'Catalog scope commands'
        Test the operation of the List, Get, Update, Delete commands result.
        :param role:running user.
        """

        catalog_id = 'catalog0-111-222-333-0000001'

        # Get users project_id.
        if role == 'user':
            scope = CONF.project_id
        else:
            scope = CONF.admin_project_id

        # Add records.
        catalog_scope_id, catalog_scope_id_dammy = self._create_catalog_scope(
            'admin', catalog_id, scope)

        # Get records by catalog scope list.
        self._list_catalog_scope(role, catalog_scope_id)

        # Get records by catalog scope get.
        self._show_catalog_scope(role,
                                 catalog_scope_id,
                                 catalog_id,
                                 scope)

        # Update records.
        if role == 'admin':
            self._update_catalog_scope(role,
                                       catalog_scope_id,
                                       catalog_id,
                                       scope)

        # Delete records.
        self.clients['admin'].run_command(
            'catalog-scope-delete', params=' --id ' + catalog_scope_id)

        self.clients['admin'].run_command(
            'catalog-scope-delete', params=' --id ' + catalog_scope_id_dammy)

        self.assertRaises(exceptions.CommandFailed,
                          self.clients['admin'].run_command,
                          'catalog-scope-delete',
                          params=' --id ' + catalog_scope_id)

    def _create_catalog_scope(self, role, catalog_id, scope):
        """Create catalog data.
        :param role: running user.
        """
        st_create = self.clients[role].run_command(
            'catalog-scope-create',
            params=' --catalog-id {0}'
                   ' --scope {1}'
                   ' --lifetime-start {2}'
                   ' --lifetime-end {3}'
                   .format(catalog_id,
                           scope,
                           '2015-01-01T01:02:03.123456',
                           '2020-11-12T04:05:06.234567'))

        st_create_dammy = self.clients[role].run_command(
            'catalog-scope-create',
            params=' --catalog-id {0}'
                   ' --scope {1}'
                   ' --lifetime-start {2}'
                   ' --lifetime-end {3}'
                   .format('catalog-dammy0-111-222-333',
                           scope,
                           '2015-01-01T01:02:03.123456',
                           '2020-11-12T04:05:06.234567'))

        # Check got UUID.
        catalog_scope_id = output_parser.tables(st_create)[0]['values'][0][0]
        catalog_scope_id_dammy = \
            output_parser.tables(st_create_dammy)[0]['values'][0][0]
        self.assertTrue(catalog_id is not None)

        # Check all param.
        check_param = {'id': catalog_scope_id,
                       'catalog_id': catalog_id,
                       'scope': scope,
                       'lifetime_start': '2015-01-01T01:02:03.123456',
                       'lifetime_end': '2020-11-12T04:05:06.234567'}

        self._check_return_param(
            output_parser.tables(st_create)[0]['values'][0],
            check_param)

        return catalog_scope_id, catalog_scope_id_dammy

    def _list_catalog_scope(self, role, catalog_scope_id):
        """List catalog scope data.
        :param role: running user.
        """

        st_list = self.clients[role].run_command('catalog-scope-list')

        catalog_scope_list = output_parser.tables(st_list)[0]['values']
        self.assertTrue(len(catalog_scope_list) >= 1)

        # Check all param.
        result = False
        for catalog_scope_info in catalog_scope_list:
            if catalog_scope_info[0] == catalog_scope_id:
                result = True
                break

        self.assertTrue(result)

    def _show_catalog_scope(self, role, catalog_scope_id, catalog_id, scope):
        """Show catalog scope data.
        :param role: running user.
        :param catalog_scope_id: The id of catalog scope table.
        """
        st_get = self.clients[role].run_command(
            'catalog-scope-get', params=' --id ' + catalog_scope_id)
        catalog_scope = output_parser.tables(st_get)[0]['values'][0]

        # Check all param.
        check_param = {'id': catalog_scope_id,
                       'catalog_id': catalog_id,
                       'scope': scope,
                       'lifetime_start': '2015-01-01T01:02:03.000000',
                       'lifetime_end': '2020-11-12T04:05:06.000000'}

        self._check_return_param(catalog_scope,
                                 check_param)

    def _update_catalog_scope(self, role, catalog_scope_id, catalog_id, scope):
        """Update catalog scope data.
        :param role: running user.
        :param catalog_scope_id: The id of catalog scope table.
        """
        st_update = self.clients[role].run_command(
            'catalog-scope-update',
            params=' --id {0}'
                   ' --lifetime-start {1}'
                   ' --lifetime-end {2}'
                   .format(catalog_scope_id,
                           '2016-01-31T23:59:59.999999',
                           '2021-12-31T23:59:59.999999'))

        catalog_scope = output_parser.tables(st_update)[0]['values'][0]

        # Check all param.
        check_param = {'id': catalog_scope_id,
                       'catalog_id': catalog_id,
                       'scope': scope,
                       'lifetime_start': '2016-01-31T23:59:59.999999',
                       'lifetime_end': '2021-12-31T23:59:59.999999'}

        self._check_return_param(catalog_scope, check_param)

    def _check_return_param(self, return_data, check_param):
        self.assertEqual(return_data[0], check_param['id'])
        self.assertEqual(return_data[1], check_param['catalog_id'])
        self.assertEqual(return_data[2], check_param['scope'])
        self.assertEqual(return_data[3], check_param['lifetime_start'])
        self.assertEqual(return_data[4], check_param['lifetime_end'])
        self.assertIsNotNone(return_data[5])
        self.assertIsNotNone(return_data[6])
        self.assertEqual(return_data[7], 'None')
        self.assertEqual(return_data[8], 'False')
        self.assertEqual(return_data[9], 'None')
        self.assertEqual(return_data[10], 'None')
        self.assertEqual(return_data[11], 'None')
        self.assertEqual(return_data[12], 'None')
        self.assertEqual(return_data[13], 'None')
        self.assertEqual(return_data[14], 'None')

    @ddt.data('admin', 'user')
    def test_catalog_scope_invalid_show_irregular_no_data(self, role):
        """Test of 'Catalog scope commands'
        Test the operation of the Show command(Not exist catalog scope id).
        :param role: running user.
        """
        catalog_scope_id = str(uuid.uuid4())

        self.assertRaises(exceptions.CommandFailed,
                          self.clients[role].run_command,
                          'catalog-scope-show',
                          params=' --id ' + catalog_scope_id)

    @ddt.data('admin', 'user')
    def test_catalog_scope_list_irregular_params(self, role):
        """Test of 'Catalog scope commands'
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
                              'catalog-scope-list %s' % arg)

    @ddt.data('user')
    def test_catalog_scope_create_irregular_no_authority(self, role):
        """Test of 'Catalog scope commands'
        Test the operation of the Create command(Not exist authority).
        :param role: running user.
        """
        self.assertRaises(exceptions.CommandFailed,
                          self.clients[role].run_command,
                          'catalog-scope-create',
                          params=' --catalog-id {0}'
                                 ' --scope {1}'
                                 ' --lifetime-start {2}'
                                 ' --lifetime-end {3}'
                                 .format('catalog0-111-222-333-000001',
                                         '5d19ec09dfb04e83b8385a2365c217e0',
                                         '2015-01-01T12:13:14.123456',
                                         '2015-12-13T13:14:15.234567'))

    @ddt.data('admin', 'user')
    def test_catalog_invalid_update_irregular_no_data(self, role):
        """Test of 'Catalog scope commands'
        Test the operation of the Update command(Not exist catalog scope id).
        :param role: running user.
        """
        catalog_scope_id = str(uuid.uuid4())

        self.assertRaises(exceptions.CommandFailed,
                          self.clients[role].run_command,
                          'catalog-scope-update',
                          params=' --id {0}'
                                 ' --lifetime_start {1} '
                                 ' --lifetime_end {2}'
                                 .format(catalog_scope_id,
                                         '2015-01-01T12:13:14.123456',
                                         '2015-12-13T13:14:15.234567'))

    @ddt.data('admin')
    def test_catalog_scope_delete_irregular_no_data(self, role):
        """Test of 'Catalog scope commands'
        Test the operation of the Delete command(Not exist catalog scope id).
        """
        catalog_scope_id = str(uuid.uuid4())

        self.assertRaises(exceptions.CommandFailed,
                          self.clients[role].run_command,
                          'catalog-scope-delete',
                          params=' --id ' + catalog_scope_id)

    @ddt.data('user')
    def test_catalog_scope_delete_irregular_no_authority(self, role):
        """Test of 'Catalog scope commands'
        Test the operation of the Delete command(Not exist catalog scope id).
        """
        catalog_scope_id = str(uuid.uuid4())

        self.assertRaises(exceptions.CommandFailed,
                          self.clients[role].run_command,
                          'catalog-scope-delete',
                          params=' --id ' + catalog_scope_id)
