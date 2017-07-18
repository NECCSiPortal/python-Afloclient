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


@ddt.ddt
class ClientTestCatalogs(base.BaseTestCase):
    """Test catalog of aflo component service."""

    @ddt.data('admin', 'user')
    def test_catalog(self, role):
        """Test of 'Catalog commands'
        Test the operation of the List, Get, Update, Delete commands result.
        :param role: running user.
        """
        catalog_id, catalog_id_dammy = self._create_catalog('admin')

        # Get records by list.
        self._list_catalog(role, catalog_id)

        # Get records by catalog get.
        self._show_catalog(role, catalog_id)

        # Update records
        if role == 'admin':
            self._update_catalog(role, catalog_id)

        # Delete records
        self.clients['admin']\
            .run_command('catalog-delete',
                         params=' --catalog-id ' + catalog_id)

        self.clients['admin']\
            .run_command('catalog-delete',
                         params=' --catalog-id ' + catalog_id_dammy)

        self.assertRaises(exceptions.CommandFailed,
                          self.clients['admin'].run_command,
                          'goods-delete',
                          params=' --catalog-id ' + catalog_id_dammy)

    def _create_catalog(self, role):
        """Create catalog data.
        :param role: running user.
        """
        st_create_dammy = self.clients[role].run_command(
            'catalog-create',
            params=' --region-id {0}'
                   ' --catalog-name {1}'
                   ' --lifetime-start {2}'
                   ' --lifetime-end {3}'
                   .format('region_id_dammy',
                           'catalog_name_dammy',
                           '2015-01-01T01:02:03.123456',
                           '2015-11-12T04:05:06.234567'))

        st_create = self.clients[role].run_command(
            'catalog-create',
            params=' --region-id {0}'
                   ' --catalog-name {1}'
                   ' --lifetime-start {2}'
                   ' --lifetime-end {3}'
                   .format('region_id',
                           'catalog_name',
                           '2015-01-01T01:02:03.123456',
                           '2015-11-12T04:05:06.234567'))

        # Check got UUID
        catalog_id = output_parser.tables(st_create)[0]['values'][0][0]
        self.assertTrue(catalog_id is not None)
        catalog_id_dammy = \
            output_parser.tables(st_create_dammy)[0]['values'][0][0]

        # Check all param
        check_param = {'catalog_id': catalog_id,
                       'region_id': 'region_id',
                       'catalog_name': 'catalog_name',
                       'lifetime_start': '2015-01-01T01:02:03.123456',
                       'lifetime_end': '2015-11-12T04:05:06.234567',
                       }
        self._check_return_param(
            output_parser.tables(st_create)[0]['values'][0],
            check_param)

        return catalog_id, catalog_id_dammy

    def _show_catalog(self, role, catalog_id):
        """Show catalog data.
        :param role: running user.
        :param catalog_id: Catalog id.
        """
        st_get = self.clients[role].run_command(
            'catalog-get',
            params=' --catalog-id ' + catalog_id)
        catalog = output_parser.tables(st_get)[0]['values'][0]

        return catalog

    def _list_catalog(self, role, catalog_id):
        """List catalog data.
        :param role: running user.
        """
        st_list = self.clients[role].run_command('catalog-list')

        self.clients[role].run_command(
            'catalog-list',
            params=' --region-id {0}'
                   ' --catalog-name {1}'
                   ' --sort-key {2}'
                   ' --sort-dir {3}'
                   ' --limit {4}'
                   .format('region_id',
                           'catalog_name',
                           'catalog_id',
                           'desc',
                           '1000'))

        catalog_list = output_parser.tables(st_list)[0]['values']
        self.assertTrue(len(catalog_list) >= 1)

        # Check all param
        result = False
        for catalog_info in catalog_list:
            if catalog_info[0] == catalog_id:
                result = True
                break

        self.assertTrue(result)

        return catalog_list

    def _update_catalog(self, role, catalog_id):
        """Update catalog data.
        :param role: running user.
        :param catalog_id: Catalog id.
        :param catalog: catalog.
        """
        st_update = self.clients[role].run_command(
            'catalog-update',
            params=' --catalog-id {0}'
                   ' --region-id {1}'
                   ' --catalog-name {2}'
                   ' --lifetime-start {3}'
                   ' --lifetime-end {4}'
                   .format(catalog_id,
                           'region_id_updated',
                           'catalog_name_updated',
                           '2015-01-01T01:02:03.123456',
                           '2015-11-12T04:05:06.234567'))

        catalog = output_parser.tables(st_update)[0]['values']

        # Check all param
        check_param = {'catalog_id': catalog_id,
                       'region_id': 'region_id_updated',
                       'catalog_name': 'catalog_name_updated',
                       'lifetime_start': '2015-01-01T01:02:03.123456',
                       'lifetime_end': '2015-11-12T04:05:06.234567',
                       }
        self._check_return_param(catalog[0], check_param)

        return catalog

    def _check_return_param(self, return_data, check_param):
        self.assertEqual(return_data[0], check_param['catalog_id'])
        self.assertEqual(return_data[1], check_param['region_id'])
        self.assertEqual(return_data[2], check_param['catalog_name'])
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
    def test_catalog_invalid_show_irregular_no_data(self, role):
        """Test of 'Catalog commands'
        Test the operation of the Show command(Not exist catalog id).
        :param role: running user.
        """
        catalog_id = str(uuid.uuid4())

        self.assertRaises(exceptions.CommandFailed,
                          self.clients[role].run_command,
                          'catalog-show',
                          params=' --catalog-id ' + catalog_id)

    @ddt.data('admin', 'user')
    def test_catalog_list_irregular_params(self, role):
        """Test of 'Catalog commands'
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
                              'catalog-list %s' % arg)

    @ddt.data('user')
    def test_catalog_invalid_create_irregular_no_authority(self, role):
        """Test of 'Catalog commands'
        Test the operation of the Create command(Not exist authority).
        :param role: running user.
        """
        self.assertRaises(exceptions.CommandFailed,
                          self.clients[role].run_command,
                          'catalog-create',
                          params=' --region-id {0}'
                                 ' --catalog-name {1}'
                                 ' --lifetime-start {2}'
                                 ' --lifetime-end {3}'
                                 .format('region_id',
                                         'catalog_name',
                                         '2015-01-01T12:13:14.123456',
                                         '2015-12-13T13:14:15.234567'))

    @ddt.data('admin', 'user')
    def test_catalog_invalid_update_irregular_no_data(self, role):
        """Test of 'Catalog commands'
        Test the operation of the Update command(Not exist catalog id).
        :param role: running user.
        """
        catalog_id = str(uuid.uuid4())

        self.assertRaises(exceptions.CommandFailed,
                          self.clients[role].run_command,
                          'catalog-update',
                          params=' --catalog-id {0}'
                                 ' --region-id {1}'
                                 ' --catalog-name {2}'
                                 ' --lifetime-start {3}'
                                 ' --lifetime-end {4}'
                                 .format(catalog_id, 'a', 'a', 'a', 'a'))

    @ddt.data('admin')
    def test_catalog_invalid_delete_irregular_no_data(self, role):
        """Do a test of 'Catalog commands'
        Test the operation of the Delete command(Not exist catalog id).
        """
        catalog_id = str(uuid.uuid4())

        self.assertRaises(exceptions.CommandFailed,
                          self.clients[role].run_command,
                          'catalog-delete',
                          params=' --catalog-id ' + catalog_id)

    @ddt.data('user')
    def test_catalog_invalid_delete_irregular_no_authority(self, role):
        """Do a test of 'Catalog commands'
        Test the operation of the Delete command(Not exist authority).
        """
        catalog_id = str(uuid.uuid4())

        self.assertRaises(exceptions.CommandFailed,
                          self.clients[role].run_command,
                          'catalog-delete',
                          params=' --catalog-id ' + catalog_id)
